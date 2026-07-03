import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.parse_data import qc_parse_data


def test_parse_csv():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "spc_sample.csv")
    result = qc_parse_data(data_path)
    assert result["file"] == "spc_sample.csv"
    assert result["rows"] == 125
    assert result["pipeline"] == "spc"
    assert len(result["columns"]) > 0

    col_types = {c["name"]: c["type"] for c in result["columns"]}
    assert col_types.get("measurement") == "measurement"
    assert col_types.get("usl") == "spec_upper"
    assert col_types.get("lsl") == "spec_lower"
    assert col_types.get("batch") == "batch"

    assert "control_chart" in result["suggestions"]
    chart = result["suggestions"]["control_chart"]
    assert chart in ("Xbar-R", "Xbar-S", "I-MR")


def test_parse_csv_reliability():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "reliability_sample.csv")
    result = qc_parse_data(data_path)
    assert result["pipeline"] == "reliability"
    assert result["rows"] == 30

    col_types = {c["name"]: c["type"] for c in result["columns"]}
    assert col_types.get("time") == "time"
    assert col_types.get("censor") == "censor"


def test_parse_measurement_stats():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "spc_sample.csv")
    result = qc_parse_data(data_path)
    for col in result["columns"]:
        if col["type"] == "measurement":
            assert "mean" in col
            assert "std" in col
            assert "min" in col
            assert "max" in col
            assert 8.0 <= col["mean"] <= 12.0


if __name__ == "__main__":
    test_parse_csv()
    test_parse_csv_reliability()
    test_parse_measurement_stats()
    print("All parse tests passed!")
