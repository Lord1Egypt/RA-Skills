import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENV_PYTHON = ROOT / ".venv" / "bin" / "python"
RUNNER = [str(VENV_PYTHON if VENV_PYTHON.exists() else sys.executable), "-m", "yumnb"]


def run_cmd(args, cwd=None):
    env = dict(**__import__('os').environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(ROOT) if not existing else f"{ROOT}:{existing}"
    return subprocess.run(
        RUNNER + args,
        cwd=cwd or ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def test_help_runs():
    result = run_cmd(["--help"])
    assert result.returncode == 0, result.stderr
    assert "ingest" in result.stdout
    assert "auto" in result.stdout


def test_ingest_text_creates_note(tmp_path):
    result = run_cmd([
        "--config", str(ROOT / "config.yaml"),
        "ingest", "hello world from smoke test", "--title", "smoke-text"
    ], cwd=ROOT)
    assert result.returncode == 0, result.stderr
    folder_line = next(line for line in result.stdout.splitlines() if line.startswith("FOLDER:"))
    folder = Path(folder_line.split("FOLDER:", 1)[1].strip())
    assert folder.exists()
    assert (folder / "source" / "raw.txt").exists()
    assert (folder / "info.json").exists()


def test_ppt_builds_from_minimal_deck(tmp_path):
    deck = {
        "title": "Smoke Deck",
        "subtitle": "test",
        "slides": [
            {"type": "title", "title": "Smoke Deck", "subtitle": "test"},
            {"type": "bullets", "title": "Bullets", "bullets": ["one", "two"]},
            {"type": "summary", "title": "Done", "text": "ok"},
        ],
    }
    deck_path = tmp_path / "deck.json"
    out_path = tmp_path / "deck.pptx"
    deck_path.write_text(json.dumps(deck, ensure_ascii=False), encoding="utf-8")

    result = run_cmd(["ppt", str(deck_path), "--output", str(out_path)])
    assert result.returncode == 0, result.stderr
    assert out_path.exists()
    assert out_path.stat().st_size > 0


def test_auto_mode_error_is_human_when_provider_not_ready(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "output_dir: ./notes\n"
        "ai:\n"
        "  provider: openai\n"
        "  openai:\n"
        "    model: gpt-4o-mini\n",
        encoding="utf-8",
    )
    result = run_cmd(["--config", str(cfg), "auto", "hello smoke auto", "--title", "smoke-auto"], cwd=tmp_path)
    assert result.returncode != 0
    combined = (result.stdout or "") + "\n" + (result.stderr or "")
    assert "auto mode cannot continue because AI provider 'openai' is not ready" in combined
    assert "switch ai.provider to 'none'" in combined


def test_publish_with_openclaw_deliver_dry_run_records_results(tmp_path):
    folder = tmp_path / "note"
    (folder / "source").mkdir(parents=True)
    (folder / "info.json").write_text(
        json.dumps({"title": "Smoke Delivery", "kind": "text", "input": "hello"}, ensure_ascii=False),
        encoding="utf-8",
    )
    (folder / "summary.md").write_text(
        "# Smoke Delivery\n\n## 🎯 One-line summary\n\nIt works.\n",
        encoding="utf-8",
    )
    (folder / "talkshow.mp3").write_bytes(b"fake-mp3")
    (folder / "deck.pptx").write_bytes(b"fake-pptx")

    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "deliver:\n"
        "  provider: openclaw\n"
        "  openclaw:\n"
        "    channel: discord\n"
        "    target: '123456'\n"
        "    dry_run: true\n"
        "  files: [talkshow.mp3]\n",
        encoding="utf-8",
    )

    result = run_cmd(["--config", str(cfg), "publish", str(folder)], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    links = json.loads((folder / "links.json").read_text(encoding="utf-8"))
    assert "deliver_results" in links
    assert len(links["deliver_results"]) >= 1
    assert any(item.get("kind") == "text" for item in links["deliver_results"])
