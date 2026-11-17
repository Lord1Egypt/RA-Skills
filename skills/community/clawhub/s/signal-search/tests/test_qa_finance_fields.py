"""金融源：K线/资金流补 fields1/fields2 字段后解析正确（不依赖抖动网络）。

锁定回归：finance.fetch 在 push2 返回带 klines 时，_build_doc 须产出非空
近半年日K 与主力资金流，且涨跌幅取自正确字段(f59=p[8])。
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/scripts")

import finance


def _fake_curl(urls_seen):
    def _curl(url, headers=None, cfg=None, timeout=12):
        urls_seen.append(url)
        if "kline" in url and "fflow" not in url:
            # push2his kline：fields1/fields2 须出现在 URL 中
            body = json.dumps(
                {
                    "rc": 0,
                    "data": {
                        "code": "600519",
                        "klines": [
                            "2026-08-10,1700.0,1680.0,1710.0,1670.0,1000000,1.7e9,2.3,1.20,18.5,0.30",  # noqa: E501
                            "2026-08-11,1680.0,1650.0,1690.0,1640.0,1200000,2.0e9,2.9,-1.79,-30.0,0.35",  # noqa: E501
                            "2026-08-12,1650.0,1666.0,1675.0,1645.0,900000,1.5e9,1.7,0.97,16.0,0.26",  # noqa: E501
                        ],
                    },
                }
            )
            return 200, body, None
        if "fflow" in url:
            # 资金流：fields1/fields2 须出现在 URL 中
            body = json.dumps(
                {
                    "rc": 0,
                    "data": {
                        "code": "600519",
                        "klines": [
                            "2026-08-11,358946672.0,-280123.0,-358666544.0,241370384.0,117576288.0,8.20,-0.01,-8.20,5.52,2.69",  # noqa: E501
                            "2026-08-12,400000000.0,-100000.0,-399000000.0,200000000.0,99900000.0,7.10,0.02,-7.10,4.10,2.10",  # noqa: E501
                        ],
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


def test_finance_kline_and_fundflow_parsed(monkeypatch):
    urls = []
    monkeypatch.setattr("scrape._fetch_system_curl", _fake_curl(urls))
    docs, warns = finance.fetch("600519 近半年股价波动和主力净流入", cfg={}, web_fetch=None)
    assert docs, f"应返回金融源文档，warnings={warns}"
    text = docs[0]["text"]
    # 近半年日K 应有 3 行（mock 给了 3 条）
    assert "近半年日K" in text
    assert "2026-08-12" in text, "K线日期应出现"
    assert "1.20" in text or "0.97" in text, "涨跌幅应为正确字段 f59"
    # 主力资金流
    assert "主力资金流" in text
    assert "主力净流入" in text
    # URL 携带 fields 参数（修复点）
    assert any(
        "fields1=" in u and "fields2=" in u for u in urls
    ), "K线/资金流 URL 须带 fields1/fields2"
