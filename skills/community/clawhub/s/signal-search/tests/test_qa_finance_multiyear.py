"""金融源：财报多年序列（C1）。

锁定回归：finance.fetch 在 f10 返回多期数据时，财报 doc 须输出
「最新一期摘要 + 近年（年度）序列」，覆盖多年趋势分析；年报取报告期 12-31 的最近 5 个。
不依赖抖动网络（monkeypatch _f10_get）。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/scripts")

import finance


def _multi_rows():
    """构造 9 个报告期：5 个年报(2020-2024) + 2025Q1 + 2024 三个季报。"""
    base = {  # 年报数据（元 / 百分数）
        "SECURITY_CODE": "600519",
        "SECURITY_NAME_ABBR": "贵州茅台",
        "BASIC_EPS": 0.0,
        "WEIGHTAVG_ROE": 0.0,
        "PARENT_BIPS": 0.0,
    }
    annual = [
        ("2024-12-31 00:00:00", 1.741e11, 15.66, 8.62e10, 15.38, 68.64, 34.46),
        ("2023-12-31 00:00:00", 1.476e11, 19.01, 7.47e10, 19.16, 59.49, 34.19),
        ("2022-12-31 00:00:00", 1.241e11, 16.87, 6.27e10, 19.55, 49.93, 30.26),
        ("2021-12-31 00:00:00", 1.062e11, 11.88, 5.25e10, 12.34, 41.76, 29.90),
        ("2020-12-31 00:00:00", 9.49e10, 11.10, 4.67e10, 13.33, 37.17, 31.41),
    ]
    rows = []
    for rd, inc, iy, npv, ny, eps, roe in annual:
        rows.append(
            {
                **base,
                "REPORTDATE": rd,
                "TOTAL_OPERATE_INCOME": inc,
                "YSTZ": iy,
                "PARENT_NETPROFIT": npv,
                "SJLTZ": ny,
                "BASIC_EPS": eps,
                "WEIGHTAVG_ROE": roe,
            }
        )
    rows.append(
        {
            **base,
            "REPORTDATE": "2025-03-31 00:00:00",
            "TOTAL_OPERATE_INCOME": 51443450583.77,
            "YSTZ": 10.67,
            "PARENT_NETPROFIT": 26847474238.76,
            "SJLTZ": 11.56,
            "BASIC_EPS": 21.38,
            "WEIGHTAVG_ROE": 12.34,
        }
    )
    for rd in ("2024-09-30 00:00:00", "2024-06-30 00:00:00", "2024-03-31 00:00:00"):
        rows.append(
            {
                **base,
                "REPORTDATE": rd,
                "TOTAL_OPERATE_INCOME": 1.2e11,
                "YSTZ": 17.0,
                "PARENT_NETPROFIT": 6.0e10,
                "SJLTZ": 15.0,
                "BASIC_EPS": 47.0,
                "WEIGHTAVG_ROE": 28.0,
            }
        )
    return rows


def _fake_f10(rows):
    def _get(url, timeout=12):
        # 对齐 _f10_get 返回签名：(status, parsed_dict)
        return 200, {"success": True, "result": {"data": rows}}

    return _get


def test_finance_report_multiyear_series(monkeypatch):
    monkeypatch.setattr(finance, "_f10_get", _fake_f10(_multi_rows()))
    docs, warns = finance.fetch("600519 分析最近5年财报", cfg={}, web_fetch=None)
    rdoc = next((d for d in docs if d.get("source_type") == "finance_report"), None)
    assert rdoc is not None, f"应产出财报 doc，docs={[d['source_type'] for d in docs]}"
    text = rdoc["text"]
    # 最新一期摘要（2025Q1）
    assert "最新报告期: 2025-03-31" in text
    assert "营业收入: 514.43 亿元" in text
    # 近年年度序列：5 个年报行
    for y in ("2024-12-31", "2023-12-31", "2022-12-31", "2021-12-31", "2020-12-31"):
        assert y in text, f"年度序列应含 {y}"
    year_lines = [ln for ln in text.splitlines() if ln.startswith("- 20")]
    assert len(year_lines) == 5, f"应恰好 5 个年度行，实际 {len(year_lines)}：{year_lines}"
    # 季报(非12-31)不应出现在年度序列
    assert "2024-09-30" not in text or "- 2024-09-30" not in text
    assert "snippet" in rdoc and rdoc["snippet"]


def test_finance_report_annual_only_filter(monkeypatch):
    """非年报报告期(如 03-31/09-30)不进入年度序列。"""
    rows = [
        {
            "SECURITY_CODE": "600519",
            "SECURITY_NAME_ABBR": "贵州茅台",
            "REPORTDATE": "2025-03-31 00:00:00",
            "TOTAL_OPERATE_INCOME": 5.0e10,
            "YSTZ": 10.0,
            "PARENT_NETPROFIT": 2.6e10,
            "SJLTZ": 11.0,
            "BASIC_EPS": 21.0,
            "WEIGHTAVG_ROE": 12.0,
            "PARENT_BIPS": 180.0,
        },
    ]
    monkeypatch.setattr(finance, "_f10_get", _fake_f10(rows))
    docs, _ = finance.fetch("600519 财报", cfg={}, web_fetch=None)
    rdoc = next((d for d in docs if d.get("source_type") == "finance_report"), None)
    assert rdoc is not None
    year_lines = [ln for ln in rdoc["text"].splitlines() if ln.startswith("- 20")]
    assert year_lines == [], f"单季数据不应产生年度行，实际 {year_lines}"
