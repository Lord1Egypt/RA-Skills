import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.parse_data import qc_parse_data
from tools.reliability_analyze import qc_reliability_analyze

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "reliability_sample.csv")


def test_reliability_weibull():
    schema = qc_parse_data(DATA_PATH)
    assert "_file_path" in schema
    result = qc_reliability_analyze(schema, "time", "censor")

    assert "best_fit" in result
    assert result["best_fit"] in ("Weibull", "Lognormal", "Exponential")
    assert "aicc_comparison" in result
    assert len(result["aicc_comparison"]) >= 1
    assert "parameters" in result
    assert "metrics" in result
    assert "probability_plot_data" in result

    params = result["parameters"]
    if result["best_fit"] == "Weibull":
        assert "beta" in params
        assert "eta" in params
    elif result["best_fit"] == "Lognormal":
        assert "mu" in params
        assert "sigma" in params
    elif result["best_fit"] == "Exponential":
        assert "lambda" in params

    metrics = result["metrics"]
    assert "b10_life" in metrics
    assert "b50_life" in metrics
    assert "mttf" in metrics

    pp = result["probability_plot_data"]
    assert "times" in pp
    assert "censor" in pp
    assert "fit_line" in pp


def test_reliability_metrics():
    schema = qc_parse_data(DATA_PATH)
    result = qc_reliability_analyze(schema, "time", "censor")

    metrics = result["metrics"]
    assert metrics["b10_life"] > 0
    assert metrics["b50_life"] > 0
    assert metrics["mttf"] > 0


def test_small_sample_warning():
    schema = qc_parse_data(DATA_PATH)
    result = qc_reliability_analyze(schema, "time", "censor")
    # 30 samples, no warning expected
    assert result.get("warning") is None


if __name__ == "__main__":
    test_reliability_weibull()
    test_reliability_metrics()
    test_small_sample_warning()
    print("All reliability tests passed!")
