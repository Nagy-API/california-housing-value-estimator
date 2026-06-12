from pathlib import Path
import sqlite3

import joblib
import pandas as pd
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

MODEL_PATH = ROOT_DIR / "model" / "housing_price_model.joblib"
DB_DIR = ROOT_DIR / "database"
DB_PATH = DB_DIR / "predictions.db"

app = FastAPI(title="California Housing Value Estimator")

model = joblib.load(MODEL_PATH)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


def init_db():
    DB_DIR.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                longitude REAL NOT NULL,
                latitude REAL NOT NULL,
                housing_median_age REAL NOT NULL,
                total_rooms REAL NOT NULL,
                total_bedrooms REAL NOT NULL,
                population REAL NOT NULL,
                households REAL NOT NULL,
                median_income REAL NOT NULL,
                ocean_proximity TEXT NOT NULL,
                predicted_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()


def save_prediction(form_data, predicted_price):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO predictions (
                longitude,
                latitude,
                housing_median_age,
                total_rooms,
                total_bedrooms,
                population,
                households,
                median_income,
                ocean_proximity,
                predicted_price
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            form_data["longitude"],
            form_data["latitude"],
            form_data["housing_median_age"],
            form_data["total_rooms"],
            form_data["total_bedrooms"],
            form_data["population"],
            form_data["households"],
            form_data["median_income"],
            form_data["ocean_proximity"],
            predicted_price
        ))

        conn.commit()


def get_recent_predictions(limit=10):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                longitude,
                latitude,
                housing_median_age,
                total_rooms,
                total_bedrooms,
                population,
                households,
                median_income,
                ocean_proximity,
                predicted_price,
                created_at
            FROM predictions
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

    predictions = []

    for row in rows:
        item = dict(row)
        item["formatted_price"] = f"${item['predicted_price']:,.0f}"
        predictions.append(item)

    return predictions


def clear_prediction_history():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions")
        conn.commit()


def render_home(
    request: Request,
    prediction=None,
    formatted_prediction=None,
    form_data=None,
    error=None
):
    recent_predictions = get_recent_predictions()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "prediction": prediction,
            "formatted_prediction": formatted_prediction,
            "form_data": form_data or {},
            "error": error,
            "recent_predictions": recent_predictions
        }
    )


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return render_home(request)


@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    longitude: float = Form(...),
    latitude: float = Form(...),
    housing_median_age: float = Form(...),
    total_rooms: float = Form(...),
    total_bedrooms: float = Form(...),
    population: float = Form(...),
    households: float = Form(...),
    median_income: float = Form(...),
    ocean_proximity: str = Form(...)
):
    form_data = {
        "longitude": longitude,
        "latitude": latitude,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income,
        "ocean_proximity": ocean_proximity
    }

    if total_rooms <= 0 or total_bedrooms <= 0 or population <= 0 or households <= 0:
        return render_home(
            request,
            form_data=form_data,
            error="Rooms, bedrooms, population, and households must be greater than zero."
        )

    if total_bedrooms > total_rooms:
        return render_home(
            request,
            form_data=form_data,
            error="Total bedrooms cannot be greater than total rooms."
        )

    if median_income <= 0:
        return render_home(
            request,
            form_data=form_data,
            error="Median income must be greater than zero."
        )

    input_data = pd.DataFrame([form_data])

    prediction = float(model.predict(input_data)[0])
    formatted_prediction = f"${prediction:,.0f}"

    save_prediction(form_data, prediction)

    return render_home(
        request,
        prediction=round(prediction, 2),
        formatted_prediction=formatted_prediction,
        form_data=form_data
    )


@app.post("/clear-history")
def clear_history():
    clear_prediction_history()
    return RedirectResponse(url="/", status_code=303)


@app.get("/health")
def health():
    return {"status": "ok"}