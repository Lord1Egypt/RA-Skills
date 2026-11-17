import json
import re
from pathlib import Path

import common

REPO = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def test_versions_agree():
    plugin = load(".claude-plugin/plugin.json")
    market = load(".claude-plugin/marketplace.json")
    versions = {common.__version__, plugin["version"], market["metadata"]["version"], market["plugins"][0]["version"]}
    assert len(versions) == 1 and re.fullmatch(r"\d+\.\d+\.\d+", common.__version__)


def test_manifest_shape():
    plugin = load(".claude-plugin/plugin.json")
    market = load(".claude-plugin/marketplace.json")
    assert plugin["name"] == "vibe-ledger" == market["plugins"][0]["name"]
    assert market["plugins"][0]["source"] == "./"
    assert plugin["description"] and len(plugin["description"]) < 600


def test_readme_and_license_exist():
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert "vl.py start" in readme and "MIT" in (REPO / "LICENSE").read_text(encoding="utf-8")


def test_readmes_link_each_other_and_show_their_own_screenshots():
    en = (REPO / "README.md").read_text(encoding="utf-8")
    zh = (REPO / "README_CN.md").read_text(encoding="utf-8")
    assert 'href="README_CN.md"' in en and 'href="README.md"' in zh
    for text in (en, zh):
        for img in __import__("re").findall(r'src="(docs/[^"]+)"', text):
            assert (REPO / img).is_file(), img
    assert "docs/assets/map-zh.png" in zh and "docs/assets/map.png" in en
    assert "/plugin install vibe-ledger@vibe-ledger" in en and "/plugin install vibe-ledger@vibe-ledger" in zh
