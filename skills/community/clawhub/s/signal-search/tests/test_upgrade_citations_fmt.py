import os

import vault

_SRC = [
    {"url": "https://e.com/a", "title": "A 文", "source_type": "web"},
    {
        "url": "https://e.com/b",
        "title": "B 文",
        "source_type": "academic",
        "citation": {
            "key": "arxiv-b",
            "doi": "10.1/b",
            "authors": "X",
            "year": "2024",
            "source": "arxiv",
        },
    },
]


def test_citations_formats(tmp_path):
    cases = [
        ("bibtex", "citations.bib", "@misc"),
        ("md", "references.md", "[A 文]"),
        ("ris", "references.ris", "TY  - GEN"),
        ("csl", "references.csl", '"URL"'),
        ("noteexpress", "references.ne", "#:@文献"),
    ]
    for fmt, fn, marker in cases:
        p = vault.write_citations(str(tmp_path), _SRC, fmt)
        assert os.path.isfile(p)
        txt = open(p, encoding="utf-8").read()
        assert marker in txt and "https://e.com/a" in txt
    # DOI → @article
    bib = open(os.path.join(str(tmp_path), "citations.bib"), encoding="utf-8").read()
    assert "@article{arxiv-b" in bib
