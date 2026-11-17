"""金融源：财报明细（f10 业绩报表）在命中财报意图词时追加独立 doc。

锁定回归：finance.fetch 在查询含「财报/营收/利润」等词且 f10 返回数据时，
须产出 source_type=finance_report 的 doc，含营业收入/归母净利润/每股收益，
且 f10 接口 URL 命中东财 datacenter-web 域名。不依赖抖动网络（monkeypatch）。
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/scripts")

import finance


def _fake_curl(urls_seen):
    def _curl(url, headers=None, cfg=None, timeout=12):
        urls_seen.append(url)
        if "datacenter-web.eastmoney.com" in url:
            # f10 业绩报表
            body = json.dumps(
                {
                    "success": True,
                    "result": {
                        "data": [
                            {
                                "SECURITY_CODE": "600519",
                                "SECURITY_NAME_ABBR": "贵州茅台",
                                "REPORTDATE": "2025-03-31 00:00:00",
                                "TOTAL_OPERATE_INCOME": 51443450583.77,
                                "YSTZ": 10.6673989111,
                                "PARENT_NETPROFIT": 26847474238.76,
                                "SJLTZ": 11.56,
                                "BASIC_EPS": 21.38,
                                "WEIGHTAVG_ROE": 12.34,
                                "PARENT_BIPS": 180.5,
                            },
                        ]
                    },
                }
            )
            return 200, body, None
        # 行情 stock/get
        body = json.dumps(
            {
                "rc": 0,
                "data": {
                    "f43": "166600",
                    "f44": "0",
                    "f45": "0",
                    "f46": "0",
                    "f57": "600519",
                    "f58": "贵州茅台",
                    "f60": "166600",
                    "f116": "1694223093019.29",
                    "f117": "0",
                    "f168": "35",
                    "f169": "0",
                    "f170": "92.00",
                },
            }
        )
        return 200, body, None

    return _curl


def test_finance_report_appended_on_keyword(monkeypatch):
    urls = []
    monkeypatch.setattr("scrape._fetch_system_curl", _fake_curl(urls))
    docs, warns = finance.fetch("600519 最新财报和营收利润", cfg={}, web_fetch=None)
    # 应有行情 doc + 财报 doc
    types = [d.get("source_type") for d in docs]
    assert "finance" in types, f"应有行情 doc，types={types}"
    assert "finance_report" in types, f"应追加财报 doc，types={types} warns={warns}"
    rdoc = next(d for d in docs if d["source_type"] == "finance_report")
    text = rdoc["text"]
    assert "营业收入" in text and "514.43 亿元" in text, "营收应格式化展示"
    assert "归母净利润" in text and "268.47 亿元" in text
    assert "基本每股收益: 21.38" in text
    assert "2025-03-31" in text, "报告期应出现"
    assert any("datacenter-web.eastmoney.com" in u for u in urls), "应打 f10 财报接口"


def test_finance_report_skipped_without_keyword(monkeypatch):
    urls = []
    monkeypatch.setattr("scrape._fetch_system_curl", _fake_curl(urls))
    docs, _ = finance.fetch("600519 近半年股价波动", cfg={}, web_fetch=None)
    types = [d.get("source_type") for d in docs]
    assert "finance_report" not in types, "无财报词不应追加财报 doc"
    assert any("datacenter-web.eastmoney.com" not in u for u in urls)


def test_finance_report_web_fetch_fallback(monkeypatch):
    """f10 JSON 被拦截且无数据 → 注入 web_fetch 时退化抓 f10 页面返回 doc。"""

    def _curl_block(url, headers=None, cfg=None, timeout=12):
        if "datacenter-web.eastmoney.com" in url:
            return 200, json.dumps({"success": False, "result": {"data": []}}), None
        return (
            200,
            json.dumps(
                {
                    "rc": 0,
                    "data": {
                        "f43": "166600",
                        "f58": "贵州茅台",
                        "f60": "166600",
                        "f116": "1",
                        "f168": "35",
                        "f170": "92",
                    },
                }
            ),
            None,
        )

    def _wf(url):
        return "<html>茅台 f10 财报页原始内容</html>"

    monkeypatch.setattr("scrape._fetch_system_curl", _curl_block)
    docs, warns = finance.fetch("600519 财报", cfg={}, web_fetch=_wf)
    rdoc = next((d for d in docs if d.get("source_type") == "finance_report"), None)
    assert (
        rdoc is not None
    ), f"web_fetch 兜底应产出财报 doc，docs={[d['source_type'] for d in docs]}"
    assert "原始页未结构化" in rdoc["text"]
    assert "茅台 f10 财报页原始内容" in rdoc["text"]
