"""Wave1 收尾回归测试：D1 L3 回调透传 / D2 东财字段归一化 / D3 clean_links 蜜罐。

这些用例锁定三类上线前缺陷的修复，防止回归。网络层一律 monkeypatch，不触真网。
"""

import os
import sys

import connector
import extract
import orchestrate

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


# ---------------- D1: L3 并行路径必须透传"调用方注入"回调 ----------------
def test_l3_threads_callbacks(monkeypatch):
    """research/orchestrate 在 L3 模式下，注入的 web_fetch/doi_resolver/github_token
    必须一路透传到 connector.load，不能静默丢弃。"""
    captured = {}

    def fake_load(
        q,
        freshness="中",
        constraints=None,
        cfg=None,
        web_fetch=None,
        doi_resolver=None,
        github_token=None,
        **kw,
    ):
        captured.update(web_fetch=web_fetch, doi_resolver=doi_resolver, github_token=github_token)
        return []

    monkeypatch.setattr(connector, "load", fake_load)
    wf = object()
    dr = object()
    gh = "ghp_xyz"
    orchestrate.retrieve(
        "大模型 调研 对比",
        {"required_tier": "L3"},
        cfg={},
        web_fetch=wf,
        doi_resolver=dr,
        github_token=gh,
    )
    assert captured.get("web_fetch") is wf, "web_fetch 未透传到 connector.load"
    assert captured.get("doi_resolver") is dr, "doi_resolver 未透传到 connector.load"
    assert captured.get("github_token") == gh, "github_token 未透传到 connector.load"


# ---------------- D2: 东财 push2 ×100 字段归一化 ----------------
def test_finance_price_normalization():
    """push2 价格(f43/f60)与换手率(f168)为 ×100 整型，必须 ÷100 还原；
    不能显示成'最新价: 134300'。f170/f116 口径未确认，按原始值展示（不臆造 ÷100）。"""
    q_data = {
        "data": {
            "f58": "测试股",
            "f43": "168500",
            "f60": "166600",
            "f168": "35",
            "f170": "2850",
            "f116": "2116800000000",
        }
    }
    import finance

    doc = finance._build_doc(
        "600519", "1.600519", "https://quote.eastmoney.com/sh600519.html", q_data, None, None
    )
    assert "1685.00 元" in doc["text"], doc["text"]
    assert "1666.00 元" in doc["text"], doc["text"]
    assert "0.35%" in doc["text"], doc["text"]
    # 口径未确认字段：按原始值展示，不应被错误 ÷100
    assert "2850" in doc["text"]
    assert "2116800000000" in doc["text"]


# ---------------- D3: clean_links 不能被 overflow:hidden 误杀 ----------------
def test_clean_links_keeps_overflow_hidden():
    """'overflow:hidden' 是正常 CSS，不应被判为蜜罐；仅 display:none/visibility:hidden/[hidden] 才算。"""
    html = (
        "<html><body>"
        '<div style="overflow:hidden"><a href="https://real.example.com/a">合法</a></div>'
        '<div style="display:none"><a href="https://hidden.example.com/x">蜜罐</a></div>'
        '<a href="https://visible.example.com/ok">正常</a>'
        "</body></html>"
    )
    links = extract.clean_links(html)
    assert "https://real.example.com/a" in links, "overflow:hidden 合法外链被误杀"
    assert "https://visible.example.com/ok" in links
    assert "https://hidden.example.com/x" not in links, "display:none 蜜罐未被剔除"


def test_clean_links_hidden_attribute():
    """HTML [hidden] 属性（非样式）也应判为蜜罐。"""
    html = '<a href="https://hidden.example.com/x" hidden>蜜罐</a>'
    links = extract.clean_links(html)
    assert "https://hidden.example.com/x" not in links
