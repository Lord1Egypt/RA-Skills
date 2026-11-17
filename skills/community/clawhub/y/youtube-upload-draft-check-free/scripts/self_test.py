#!/usr/bin/env python3
"""Independent offline tests; no browser, sibling skill, or absolute-path dependency."""
import json
import subprocess
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "scripts" / "check_draft.py"

def run(name):
    output = subprocess.check_output([sys.executable, str(CHECKER), str(ROOT / "fixtures" / name)], text=True)
    return json.loads(output)

def main():
    manifest = (ROOT / 'manifest.yaml').read_text()
    assert re.search(r'^version: \d+\.\d+\.\d+$', manifest, re.M)
    for section in ('tags', 'trigger_words', 'triggers'):
        block = re.search(r'^'+section+r':\n((?:  - .+\n)+)', manifest, re.M)
        assert block and len(block.group(1).splitlines()) >= 3, f'block-list metadata missing: {section}'
    for file in ('manifest.yaml', 'agents/openai.yaml'):
        metadata = (ROOT / file).read_text()
        for field in ('display_name', 'short_description', 'default_prompt', 'icon_small', 'icon_large'):
            match = re.search(r'^  '+field+r': "([^"\n]+)"$', metadata, re.M)
            assert match, f'quoted interface field missing: {field}'
            value = match.group(1)
            if field == 'short_description': assert 25 <= len(value) <= 64
            if field == 'default_prompt': assert '$youtube-upload-draft-check-free' in value
            if field.startswith('icon_'):
                target = (ROOT / value).resolve()
                assert target.is_relative_to(ROOT.resolve()) and target.is_file()
    success = run("success-page.json")
    assert success["ok"] and success["mode"] == "offline-fixture"
    assert success["missing"] == ["description", "captions"]
    assert all(row["source"] for row in success["rows"])
    unverifiable = run("unverifiable-fields-page.json")
    assert unverifiable["ok"]
    by_field = {row["field"]: row for row in unverifiable["rows"]}
    assert by_field["description"] == {
        "field": "description", "value": None, "status": "无法核验", "source": None
    }
    assert by_field["captions"]["status"] == "无法核验"
    assert "description" not in unverifiable["missing"]
    failure = run("failure-ambiguous-draft.json")
    assert not failure["ok"] and "稿件选择不明确" in failure["stop_reason"]
    print("PASS: offline checklist, unverifiable-field, and ambiguous-draft stop branches verified")

if __name__ == "__main__":
    main()
