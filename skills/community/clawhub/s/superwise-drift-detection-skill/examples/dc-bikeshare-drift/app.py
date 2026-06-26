"""
app.py
------
Flask endpoint for the DC Bikeshare drift detection example.
Called hourly by the OpenClaw skill scheduler.
"""

import os

from flask import Flask, jsonify

from predict import run_predictions

app = Flask(__name__)


@app.route("/predict")
def predict():
    result = run_predictions()
    return jsonify(result)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
