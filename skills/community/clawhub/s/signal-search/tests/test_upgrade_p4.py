"""P4 升级测试：D3 结构化引用字段（金融/GitHub 源 citation）+ D6 收口（代码侧，文档侧见 README/SKILL）。"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SYSCR = os.path.join(HERE, "..", "scripts")
if SYSCR not in sys.path:
    sys.path.insert(0, SYSCR)

import finance as finance_mod
import github as github_mod
import vault as vault_mod


# ---------- D3 金融源结构化 citation ----------
def test_finance_doc_citation():
    q_data = {
        "data": {"f58": "测试股", "f43": "10", "f60": "9", "f168": "1", "f170": "20", "f116": "100"}
    }
    doc = finance_mod._build_doc(
        "600519", "1.600519", "https://quote.eastmoney.com/sh600519.html", q_data, None, None
    )
    cit = doc.get("citation", {})
    assert cit.get("stock_code") == "600519"
    assert cit.get("key") == "eastmoney-600519"
    assert cit.get("source") == "eastmoney-push2"


# ---------- D3 GitHub 源结构化 citation ----------
def test_github_doc_citation():
    data = {
        "items": [
            {
                "full_name": "owner/repo",
                "description": "d",
                "stargazers_count": 5,
                "language": "Py",
                "html_url": "https://github.com/owner/repo",
            }
        ]
    }
    docs = github_mod._build_docs(data)
    cit = docs[0].get("citation", {})
    assert cit.get("repo") == "owner/repo"
    assert cit.get("key") == "github-owner-repo"
    assert cit.get("source") == "github-api"


# ---------- D3 BibTeX 优先用结构化 key / 字段 ----------
def test_bibtex_uses_structured_citation():
    sources = [
        {
            "url": "https://github.com/owner/repo",
            "text": "x",
            "citation": {"key": "github-owner-repo", "repo": "owner/repo", "source": "github-api"},
        }
    ]
    bib = vault_mod._citation_bibtex(sources)
    assert "github-owner-repo" in bib  # 用结构化 key，而非 src1
    assert "repo=owner/repo" in bib  # 结构化字段写入 note
    assert "@misc" in bib


def test_bibtex_fallback_when_no_citation():
    sources = [{"url": "https://e.com/plain", "text": "x"}]
    bib = vault_mod._citation_bibtex(sources)
    assert "src1" in bib  # 无 citation 退化为 srcN 顺序键
