document.getElementById("prediction-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const jsonData = {};

    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    const resultDiv = document.getElementById("prediction-result");
    resultDiv.textContent = "⏳ Predicting...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jsonData)
        });

        const result = await response.json();

        if (result.error) {
            resultDiv.textContent = "❗ Error: " + result.error;
            resultDiv.classList.add("error");
        } else {
            resultDiv.textContent = result.prediction;
            resultDiv.classList.remove("error");
        }
    } catch (err) {
        resultDiv.textContent = "❗ Request failed: " + err.message;
        resultDiv.classList.add("error");
    }
});