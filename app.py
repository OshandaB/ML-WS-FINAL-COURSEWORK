from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("model/bank-marketing.joblib")
feature_names = joblib.load("model/bank_features.pkl") 

# Define default values
default_values = {
    'contact': 'cellular',
    'month': 'nov',
    'day_of_week': 'thu',
    'campaign': 2,
    'pdays': 1,
    'previous': 0,
    'poutcome': 'success',
    'emp.var.rate': -1.1,
    'cons.price.idx': 94.767,
    'cons.conf.idx': -50.8,
    'euribor3m': 4.857,
    'nr.employed': 4963.6,
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        user_input = {
            "age": int(data["age"]),
            "job": data["job"],
            "marital": data["marital"],
            "education": data["education"],
            "default": data["default"],
            "housing": data["housing"],
            "loan": data["loan"],
        }

        user_input.update(default_values)

        client_df = pd.DataFrame([user_input])

        for col in feature_names:
            if col not in client_df.columns:
                client_df[col] = 0

        client_df = client_df[feature_names]

        prediction_result = model.predict(client_df)
        prediction = "✅ Subscribed" if prediction_result == 1 else "❌ Not Subscribed"

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
