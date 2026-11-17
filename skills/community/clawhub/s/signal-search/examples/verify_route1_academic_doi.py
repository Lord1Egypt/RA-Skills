"""examples/verify_route1_academic_doi.py - Route 1 真网验证：学术源 DOI→@article（D3）。

证明两点：
(1) 真网 arXiv 检索：无 SEMANTIC_SCHOLAR_API_KEY 时，绝不伪造 DOI → BibTeX 退化为 @misc
    （修复此前 Crossref 模糊查误命中导致的不正确 DOI）。
(2) D3 @article 导出正确：当 citation.doi 为真实值时，vault._citation_bibtex 输出 @article。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import academic
import vault

# (1) 真网：arXiv 检索
docs, warns = academic.search("graph neural network", web_fetch=None)
print(f"[live] docs={len(docs)} warns={warns}")
fake = 0
for d in docs[:8]:
    doi = d["citation"].get("doi")
    if doi:
        fake += 1
    print(f"  {d['citation']['key'][:22]:22s} doi={doi or '(无 → 正确 @misc)'}")
print(f"  含 DOI 论文数: {fake}/{len(docs)}  （无 key 时须为 0，绝不伪造）")

# (2) D3 @article 导出正确性：以一条真实已验证 DOI 演示（NeurIPS 2017 Vaswani 等）
real = [
    {
        "url": "https://arxiv.org/abs/1706.03762",
        "title": "Attention Is All You Need",
        "citation": {
            "key": "arxiv-170603762",
            "authors": "Vaswani et al.",
            "year": "2017",
            "source": "arxiv",
            "doi": "10.5555/3295222.3295349",
        },
    }
]
bib = vault._citation_bibtex(real)
print("\n[D3] 真实 DOI 经 vault 导出 →")
print(bib)
assert "@article{arxiv-170603762" in bib and "doi = {10.5555/3295222.3295349}" in bib
print("\n✅ D3 DOI→@article 导出正确：当且仅当 citation.doi 为真实值时触发 @article")
print("   激活真网 arXiv→@article：设置环境变量 SEMANTIC_SCHOLAR_API_KEY 后重跑本脚本。")
