import re
from pathlib import Path

import ledger
import probes
import vl

REPO = Path(__file__).resolve().parents[1]
SKILL = (REPO / "SKILL.md").read_text(encoding="utf-8")
REFS = {p.name: p.read_text(encoding="utf-8") for p in (REPO / "references").glob("*.md")}


def test_frontmatter():
    m = re.match(r"^---\nname: vibe-ledger\ndescription: (.+?)\n---\n", SKILL, re.S)
    assert m and len(m.group(1)) < 1024


def test_every_subcommand_named_in_skill_exists():
    parser_cmds = {"start", "merge", "check", "render", "shot", "retention"}
    named = set(re.findall(r"vl\.py (\w+)", SKILL))
    assert named and named <= parser_cmds
    assert {"start", "check", "render", "shot"} <= named


def test_every_reference_named_exists():
    named = set(re.findall(r"references/([\w-]+\.md)", SKILL + "".join(REFS.values())))
    assert named and named <= set(REFS)


def test_references_cover_the_code_vocabulary():
    text = "".join(REFS.values())
    vocab = (list(ledger.STATUSES) + list(ledger.QUESTIONS) + list(ledger.TYPES) + list(ledger.SUBJECTS)
             + list(ledger.LANES) + list(ledger.NODE_KINDS) + [m.NAME for m in probes._modules()])
    missing = [w for w in vocab if f"`{w}`" not in text]
    assert not missing, missing


def test_skill_stays_short():
    assert len(SKILL.splitlines()) < 120


def test_worked_example_in_the_guide_is_a_valid_ledger():
    import json
    block = re.search(r"`{3}json\n(.+?)\n`{3}", REFS["extraction-guide.md"], re.S).group(1)
    ledger.validate(json.loads(block))


def test_explain_guide_example_is_valid_and_named_in_skill():
    import json

    import explain
    block = re.search(r"`{3}json\n(.+?)\n`{3}", REFS["explain-guide.md"], re.S).group(1)
    explain.validate(json.loads(block))
    assert "references/explain-guide.md" in SKILL and "explain.json" in SKILL and "vl.py merge" in SKILL


def test_explain_guide_states_the_checked_limits():
    import explain
    import graph
    text = REFS["explain-guide.md"]
    assert f"±{explain.TOLERANCE}" in text and f"at most {graph.EXPLAIN_MAX}" in text
    assert f"more than {graph.EXPLAIN_CHUNK} files" in text


def test_paths_section_names_the_action_key():
    section = REFS["extraction-guide.md"].split("## 7.")[1].split("\n## ")[0]
    assert '"action"' in section and '"steps"' in section


def test_explain_guide_example_has_journeys_and_skill_names_them():
    import json
    block = re.search(r"`{3}json\n(.+?)\n`{3}", REFS["explain-guide.md"], re.S).group(1)
    assert len(json.loads(block)["journeys"]) >= 1 and "journeys" in SKILL


def test_skill_names_the_route_section_in_both_languages():
    from ledger_report.i18n import STR
    assert STR["zh"]["g_journeys"] in SKILL and STR["en"]["g_journeys"] in SKILL
