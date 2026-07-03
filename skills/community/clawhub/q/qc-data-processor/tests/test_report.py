import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.report_generate import qc_report_generate, ascii_control_chart, ascii_histogram, ascii_probability_plot, ascii_pareto


def test_daily_template():
    result = {"rows": 100, "statistics": {"cpk": 1.33}, "alarms": []}
    output = qc_report_generate(result, "daily", {"product": "Test", "date": "2024-01-01"})
    assert "品质日报" in output
    assert "Test" in output
    assert "2024-01-01" in output
    assert "检验概况" in output


def test_weekly_template():
    result = {"statistics": {"cpk": 1.33, "ppk": 1.25, "sigma_level": 3.99}, "alarms": []}
    output = qc_report_generate(result, "weekly", {"product": "Test", "week": "W01"})
    assert "品质周报" in output
    assert "Test" in output
    assert "W01" in output
    assert "Cpk" in output


def test_8d_template():
    result = {}
    output = qc_report_generate(result, "8d", {"customer": "ACME", "date": "2024-01-01"})
    assert "8D 客诉报告" in output
    assert "ACME" in output
    assert "D1 团队" in output
    assert "D8 团队确认" in output


def test_reliability_template():
    result = {
        "best_fit": "Weibull",
        "parameters": {"beta": 1.85, "eta": 1245},
        "metrics": {"b10_life": 687, "b50_life": 1134, "mttf": 1105},
        "n_samples": 30,
        "n_failures": 22,
    }
    output = qc_report_generate(result, "reliability", {"product": "Widget"})
    assert "可靠性鉴定报告" in output
    assert "Widget" in output
    assert "Weibull" in output
    assert "687" in output


def test_ascii_control_chart():
    chart_data = {
        "subgroups": [1, 2, 3, 4, 5],
        "xbar_values": [10.2, 10.0, 10.4, 10.1, 10.3],
        "r_values": [0.7, 0.4, 0.5, 0.3, 0.6],
        "ucl_x_line": 10.8, "lcl_x_line": 9.6, "cl_x_line": 10.2,
        "ucl_r_line": 1.2, "lcl_r_line": 0.0, "cl_r_line": 0.5,
    }
    output = ascii_control_chart(chart_data)
    assert "Xbar Chart" in output
    assert "R Chart" in output


def test_ascii_histogram():
    values = [10.1, 10.2, 10.0, 10.3, 10.1, 10.5, 9.9, 10.2, 10.4, 10.0,
              10.3, 9.8, 10.1, 10.2, 10.5, 9.7, 10.0, 10.3, 10.1, 10.4]
    output = ascii_histogram(values)
    assert "Histogram" in output


def test_ascii_probability_plot():
    pp_data = {
        "times": [423.0, 512.0, 687.0],
        "benard_ranks": [0.1, 0.5, 0.9],
        "censor": [1, 1, 1],
        "fit_line": [[400.0, 0.05], [800.0, 0.5]],
    }
    output = ascii_probability_plot(pp_data)
    assert "Probability Plot" in output


def test_ascii_pareto():
    labels = ["DefectA", "DefectB", "DefectC"]
    values = [50, 30, 20]
    output = ascii_pareto(labels, values, top_n=3)
    assert "Pareto Chart" in output
    assert "DefectA" in output


def test_invalid_template():
    output = qc_report_generate({}, "nonexistent")
    assert "Error" in output or "not found" in output


if __name__ == "__main__":
    test_daily_template()
    test_weekly_template()
    test_8d_template()
    test_reliability_template()
    test_ascii_control_chart()
    test_ascii_histogram()
    test_ascii_probability_plot()
    test_ascii_pareto()
    test_invalid_template()
    print("All report tests passed!")
