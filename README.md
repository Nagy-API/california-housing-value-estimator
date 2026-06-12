# California Housing Value Estimator

A machine learning regression project that predicts California housing values using district-level housing data.

The goal of this project is to practice a complete machine learning workflow, starting from data preprocessing and model evaluation, then saving the final pipeline and using it inside a simple FastAPI web application.

---

## Screenshots

> If the screenshots do not appear on GitHub, make sure the image names inside the `assets` folder match these paths exactly. GitHub is case-sensitive.

### Home Page

![Home Page](./assets/Home_Page.png)

### Prediction Result and History

![Prediction Result and History](./assets/prediction-history.png)

---

## Project Overview

This project uses the California Housing dataset to predict `median_house_value`.

The final web app allows the user to:

- Enter housing district features
- Generate a predicted property value
- Keep form values after prediction
- Try a sample input
- Clear the form
- Save previous predictions locally
- View prediction history
- Show full input details for each prediction
- Reuse previous inputs in the form

---

## Tech Stack

- Python
- pandas
- NumPy
- scikit-learn
- FastAPI
- Jinja2
- SQLite
- HTML
- CSS
- JavaScript
- joblib

---

## Project Structure

```text
Housing Price Prediction/
│
├── app/
│   ├── main.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
│
├── assets/
│   ├── Home_Page.png
│   └── prediction-history.png
│
├── data/
│   └── housing.csv
│
├── database/
│   └── .gitkeep
│
├── model/
│   └── .gitkeep
│
├── notebook/
│   └── Housing Price Prediction.ipynb
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Machine Learning Workflow

The notebook includes the following steps:

1. Loading and inspecting the dataset
2. Splitting the data into training and testing sets
3. Building preprocessing pipelines
4. Training a baseline model using `DummyRegressor`
5. Training Linear Regression
6. Analyzing model errors
7. Training Decision Tree and Random Forest models
8. Testing simple feature engineering ideas
9. Using cross-validation for model comparison
10. Tuning the final Random Forest model
11. Saving the final pipeline with `joblib`

---

## Models Tried

| Model | Notes |
|---|---|
| DummyRegressor | Used as a simple baseline |
| Linear Regression | Better than baseline, but limited |
| Decision Tree Regressor | Improved test error but overfit the training data |
| Random Forest Regressor | Best model before tuning |
| Tuned Random Forest | Final selected model |

---

## Final Model Performance

The final selected model was a tuned Random Forest Regressor.

| Metric | Test Score |
|---|---:|
| MAE | ~31.4K |
| RMSE | ~48.5K |
| R² Score | ~0.821 |

The tuned Random Forest gave the best overall performance compared to the other models.

---

## Error Analysis Summary

During the analysis, I found that Linear Regression was pulling predictions toward the average value.

It tended to:

- Overpredict cheaper houses
- Underpredict expensive houses
- Struggle with houses near the capped target value of `500001`

Random Forest handled nonlinear patterns better and gave stronger results.

---

## Web App Features

The FastAPI app includes:

- Prediction form
- Preserved inputs after prediction
- Clear form button
- Sample input button
- Basic form validation
- SQLite prediction history
- Recent predictions table
- Details button for each prediction
- Use Again button to refill the form with previous inputs
- Custom dark dashboard UI

---

## Model File

The trained model file is not included in this repository because it can be generated from the notebook.

To create the model file, run the notebook:

```text
notebook/Housing Price Prediction.ipynb
```

After running the training and saving steps, the notebook will generate:

```text
model/housing_price_model.joblib
```

The FastAPI app needs this file before running the prediction page.

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "Housing Price Prediction"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Generate the model file

Open and run the notebook:

```text
notebook/Housing Price Prediction.ipynb
```

This creates:

```text
model/housing_price_model.joblib
```

### 5. Run the FastAPI app

```bash
uvicorn app.main:app --reload
```

### 6. Open the app

```text
http://127.0.0.1:8000
```

---

## API Health Check

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## Notes

- The SQLite database file is generated at runtime and should not be pushed to GitHub.
- The trained model file is generated from the notebook and should not be pushed if it is too large.
- The final app uses the original feature set because Random Forest performed better without the engineered features in cross-validation.
- Screenshot paths must match the actual image file names exactly.

---

## Future Improvements

Possible future improvements:

- Add pagination or filters for prediction history
- Add export-to-CSV for saved predictions
- Add feature importance visualization
- Add better model explainability
- Deploy the app online
- Add Docker support
- Add automated tests

---

## Author

Built as an end-to-end machine learning practice project.
