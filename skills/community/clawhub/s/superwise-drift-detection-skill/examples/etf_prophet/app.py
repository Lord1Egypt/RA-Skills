"""
examples/etf_prophet/app.py
----------------------------
Flask web server exposing the Prophet model predictions endpoint.

Deploy to Render using render.yaml in this folder.
The skill's INFERENCE_ENDPOINT_URL should be set to:
    https://your-app.onrender.com/predict

Endpoints:
    GET /predict   — run predictions and return JSON (called by skill.py)
    GET /health    — health check for Render
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from predict import run_predictions

load_dotenv()
app = Flask(__name__)


@app.route("/predict")
def predict():
    """Run Prophet predictions and return records in the format expected by skill.py."""
    try:
        result = run_predictions()
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port)
