const form = document.getElementById("predictionForm");
const button = document.getElementById("predictBtn");
const sampleBtn = document.getElementById("sampleBtn");

if (form) {
    form.addEventListener("submit", function () {
        button.classList.add("loading");
        button.textContent = "Estimating...";
    });
}

if (sampleBtn) {
    sampleBtn.addEventListener("click", function () {
        const sampleData = {
            longitude: -122.23,
            latitude: 37.88,
            housing_median_age: 41,
            total_rooms: 880,
            total_bedrooms: 129,
            population: 322,
            households: 126,
            median_income: 8.3252,
            ocean_proximity: "NEAR BAY"
        };

        fillForm(sampleData);
    });
}

function fillForm(data) {
    Object.keys(data).forEach((key) => {
        const field = document.querySelector(`[name="${key}"]`);
        if (field) {
            field.value = data[key];
        }
    });

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

document.querySelectorAll(".details-btn").forEach((button) => {
    button.addEventListener("click", function () {
        const targetId = this.dataset.target;
        const detailsRow = document.getElementById(targetId);

        if (!detailsRow) return;

        detailsRow.classList.toggle("open");

        if (detailsRow.classList.contains("open")) {
            this.textContent = "Hide";
        } else {
            this.textContent = "Details";
        }
    });
});

document.querySelectorAll(".use-btn").forEach((button) => {
    button.addEventListener("click", function () {
        const data = {
            longitude: this.dataset.longitude,
            latitude: this.dataset.latitude,
            housing_median_age: this.dataset.housing_median_age,
            total_rooms: this.dataset.total_rooms,
            total_bedrooms: this.dataset.total_bedrooms,
            population: this.dataset.population,
            households: this.dataset.households,
            median_income: this.dataset.median_income,
            ocean_proximity: this.dataset.ocean_proximity
        };

        fillForm(data);
    });
});