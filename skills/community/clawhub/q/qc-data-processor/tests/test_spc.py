import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.parse_data import qc_parse_data
from tools.spc_analyze import qc_spc_analyze

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "spc_sample.csv")


def test_spc_xbar_r():
    schema = qc_parse_data(DATA_PATH)
    assert "_file_path" in schema
    result = qc_spc_analyze(schema, "measurement", subgroup_size=5, chart_type="Xbar-R")

    assert result["chart_type"] == "Xbar-R"
    stats = result["statistics"]
    assert "xbar_bar" in stats
    assert "r_bar" in stats
    assert "capability_available" in stats
    assert stats["capability_available"] is True
    assert "cp" in stats
    assert "cpk" in stats
    assert stats["cpk"] > 0.5  # should be decent Cpk

    # Verify Cpk formula output
    for key in ["ucl_xbar", "lcl_xbar", "ucl_r", "lcl_r"]:
        assert key in stats

    assert "alarms" in result

    cd = result["chart_data"]
    assert len(cd["xbar_values"]) > 0
    assert len(cd["r_values"]) > 0


def test_spc_imr():
    schema = qc_parse_data(DATA_PATH)
    result = qc_spc_analyze(schema, "measurement", chart_type="I-MR")

    assert result["chart_type"] == "I-MR"
    stats = result["statistics"]
    assert "x_bar" in stats
    assert "mr_bar" in stats
    assert "ucl_x" in stats
    assert "lcl_x" in stats


def test_capability_indices():
    schema = qc_parse_data(DATA_PATH)
    result = qc_spc_analyze(schema, "measurement")

    stats = result["statistics"]
    assert stats["capability_available"] is True
    assert "cp" in stats
    assert "cpk" in stats
    assert "pp" in stats
    assert "ppk" in stats
    assert "sigma_level" in stats

    # With USL=12, LSL=8, mean ~10.2, std ~0.24
    # Cp ≈ (12-8)/(6*0.24) ≈ 2.78
    assert 2.0 < stats["cp"] < 5.0
    # Sigma level ≈ 3 * Cpk
    assert abs(stats["sigma_level"] - 3 * stats["cpk"]) < 0.1


def test_western_electric_rules():
    schema = qc_parse_data(DATA_PATH)
    result = qc_spc_analyze(schema, "measurement")
    assert isinstance(result["alarms"], list)


if __name__ == "__main__":
    test_spc_xbar_r()
    test_spc_imr()
    test_capability_indices()
    test_western_electric_rules()
    print("All SPC tests passed!")
