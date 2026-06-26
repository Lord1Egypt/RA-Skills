import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core import SoulMemorySystem
from modules.vector_search import VectorSearch


def test_extract_memory_payload_removes_wrappers_and_fences(tmp_path):
    system = SoulMemorySystem(workspace_path=str(tmp_path))

    raw = """User: Please update the graph.
Assistant: We updated the live graph page.
```bash
rm -rf /tmp/nope
```
"""

    extracted = system._extract_memory_payload(raw)

    assert "We updated the live graph page." in extracted
    assert "User:" not in extracted
    assert "Assistant:" not in extracted
    assert "```" not in extracted
    assert "rm -rf" not in extracted


def test_add_memory_skips_exact_duplicate_entries(tmp_path):
    system = SoulMemorySystem(workspace_path=str(tmp_path))

    content = "[C] User prefers concise replies"
    first = system.add_memory(content)
    second = system.add_memory(content)

    assert first == second

    files = list((Path(tmp_path) / "memory").glob("*.md"))
    assert len(files) == 1
    text = files[0].read_text(encoding="utf-8")
    assert text.count("User prefers concise replies") == 1


def test_add_memory_skips_non_durable_smalltalk(tmp_path):
    system = SoulMemorySystem(workspace_path=str(tmp_path))

    system.add_memory("Thanks for the update.")

    files = list((Path(tmp_path) / "memory").glob("*.md"))
    assert files == []


def test_search_auto_tunes_parameters_for_recent_queries(tmp_path):
    system = SoulMemorySystem(workspace_path=str(tmp_path))
    system.indexed = True

    captured = {}

    def fake_search(query, top_k=5, min_score=0.0):
        captured['query'] = query
        captured['top_k'] = top_k
        captured['min_score'] = min_score
        return []

    system.vector_search.search = fake_search
    system.search("上次你幫我做咗乜", top_k=10, min_score=0.2)

    assert captured['top_k'] == 3
    assert captured['min_score'] >= 1.8


def test_vector_search_prefers_newer_memory_when_scores_tie():
    vs = VectorSearch()

    vs.add_segment({
        "content": "User prefers dark mode",
        "source": "memory/2026-04-10.md",
        "line_number": 1,
        "priority": "I",
    })
    vs.add_segment({
        "content": "User likes dark mode",
        "source": "memory/2026-04-12.md",
        "line_number": 1,
        "priority": "I",
    })

    results = vs.search("dark mode", top_k=2)

    assert len(results) == 2
    assert results[0].source.endswith("2026-04-12.md")
