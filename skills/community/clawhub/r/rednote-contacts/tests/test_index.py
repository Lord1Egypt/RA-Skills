from __future__ import annotations

import asyncio
import importlib.util
import json
import subprocess
from pathlib import Path

INDEX_PATH = Path(__file__).resolve().parents[1] / "src" / "index.py"
INDEX_SPEC = importlib.util.spec_from_file_location("red_crawler_ops_index", INDEX_PATH)
assert INDEX_SPEC is not None
assert INDEX_SPEC.loader is not None
INDEX_MODULE = importlib.util.module_from_spec(INDEX_SPEC)
INDEX_SPEC.loader.exec_module(INDEX_MODULE)
handler = INDEX_MODULE.handler
build_command = INDEX_MODULE.build_command
run_job_file = INDEX_MODULE._run_job_file
SKILL_DIR = Path(__file__).resolve().parents[1]
MANIFEST_TEXT = (SKILL_DIR / "manifest.yaml").read_text(encoding="utf-8")
SKILL_TEXT = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
CONFIG_EXAMPLE_TEXT = (SKILL_DIR / "config.example.yaml").read_text(
    encoding="utf-8"
)
README_TEXT = (SKILL_DIR.parents[1] / "README.md").read_text(encoding="utf-8")
RED_CRAWLER_PYPROJECT = '[project]\nname = "red-crawler"\n'


def run_handler(input_data, context):
    return asyncio.run(handler(input_data, context))


def test_skill_metadata_contract_matches_runtime():
    output_schema = MANIFEST_TEXT.split("output_schema:", 1)[1]
    assert "name: rednote_contacts" in SKILL_TEXT
    assert '"instructionOnly":false' in SKILL_TEXT
    assert '"remoteRepositoryClone":false' in SKILL_TEXT
    assert "runtime: python" in MANIFEST_TEXT
    assert "entry: src/index.py" in MANIFEST_TEXT
    assert "- bootstrap" in MANIFEST_TEXT
    assert "- crawl_homefeed" in MANIFEST_TEXT
    assert "- install_or_bootstrap" not in MANIFEST_TEXT
    assert "remote_repository_clone: false" in MANIFEST_TEXT
    assert "default_crawl_budget:" in MANIFEST_TEXT
    assert "default_report_days:" in MANIFEST_TEXT
    assert "default_list_limit:" in MANIFEST_TEXT
    assert "command:" in output_schema
    assert "summary:" in output_schema
    assert "job_id:" in output_schema
    assert "job:" in output_schema
    assert "artifacts:" in output_schema
    assert "stdout:" in output_schema
    assert "stderr:" in output_schema
    assert "error_type:" in output_schema
    assert "message:" in output_schema
    assert "suggested_fix:" in output_schema
    assert "metrics:" in output_schema
    assert "next_step:" in output_schema
    assert "error:" in output_schema
    assert "stdout:" in output_schema
    assert "stderr:" in output_schema
    assert "command:" in output_schema
    assert "runner_command:" in CONFIG_EXAMPLE_TEXT
    assert "action: crawl_homefeed" in CONFIG_EXAMPLE_TEXT
    assert "workspace_path: ." in CONFIG_EXAMPLE_TEXT
    assert "require_local_checkout: false" in CONFIG_EXAMPLE_TEXT
    assert "repo_url:" not in CONFIG_EXAMPLE_TEXT
    assert "workspace_parent:" not in CONFIG_EXAMPLE_TEXT
    assert "workspace_name:" not in CONFIG_EXAMPLE_TEXT
    assert "storage_state:" in CONFIG_EXAMPLE_TEXT
    assert "db_path: ./data/red_crawler.db" in CONFIG_EXAMPLE_TEXT
    assert "report_dir: ./reports" in CONFIG_EXAMPLE_TEXT
    assert "output_dir: ./output" in CONFIG_EXAMPLE_TEXT
    assert "cache_dir: ./.cache/red-crawler" in CONFIG_EXAMPLE_TEXT
    assert "heartbeat_dir: ./.openclaw/red-crawler" in CONFIG_EXAMPLE_TEXT
    assert "job_log_dir: ./logs/jobs" in CONFIG_EXAMPLE_TEXT
    assert "run_mode: sync" in CONFIG_EXAMPLE_TEXT
    assert "homefeed_url: https://www.xiaohongshu.com/explore?channel_id=homefeed.fashion_v3" in CONFIG_EXAMPLE_TEXT
    assert "browser_mode: local" in CONFIG_EXAMPLE_TEXT
    assert "proxy:" in CONFIG_EXAMPLE_TEXT
    assert "proxy_list:" in CONFIG_EXAMPLE_TEXT
    assert "rotation_mode: none" in CONFIG_EXAMPLE_TEXT
    assert "rotation_retries: 1" in CONFIG_EXAMPLE_TEXT
    assert "randomize_headers: true" in CONFIG_EXAMPLE_TEXT
    assert "sync_dependencies: false" in CONFIG_EXAMPLE_TEXT
    assert "install_browser: false" in CONFIG_EXAMPLE_TEXT
    assert "- red-crawler" in CONFIG_EXAMPLE_TEXT
    assert "default_crawl_budget: 30" in CONFIG_EXAMPLE_TEXT
    assert "default_report_days: 7" in CONFIG_EXAMPLE_TEXT
    assert "default_list_limit: 20" in CONFIG_EXAMPLE_TEXT


def test_skill_docs_match_storage_state_behavior():
    assert "bootstrap" in SKILL_TEXT
    assert "install_or_bootstrap" not in SKILL_TEXT
    assert "never clones a repository" in SKILL_TEXT
    assert "Install `red-crawler` as a package" in SKILL_TEXT
    assert "Keep the Playwright storage state file local" in SKILL_TEXT
    assert "login` creates an optional Playwright storage state explicitly" in SKILL_TEXT
    assert "crawl_seed" in SKILL_TEXT
    assert "crawl_homefeed` (default when omitted)" in SKILL_TEXT
    assert "collect_nightly" in SKILL_TEXT
    assert "report_weekly" in SKILL_TEXT
    assert "list_contactable" in SKILL_TEXT
    assert "run_mode: background" in SKILL_TEXT
    assert "HEARTBEAT.md" in SKILL_TEXT
    assert "job_status" in SKILL_TEXT
    assert "ack_event" in SKILL_TEXT
    assert "execution-time failures" in SKILL_TEXT
    assert (
        "Early validation or configuration failures may omit `action`, `command`, "
        "`stdout`, and `stderr`"
    ) in SKILL_TEXT
    assert "Run without logging in" in README_TEXT
    assert "crawl-homefeed" in README_TEXT
    assert "opens the user profile, not the note page" in README_TEXT
    assert "List high-quality contactable creators from the SQLite database" in README_TEXT
    assert "Use the OpenClaw skill actions in this order" in README_TEXT
    assert "install_or_bootstrap" not in README_TEXT
    assert "does not clone repositories" in README_TEXT
    assert "bootstrap" in README_TEXT
    assert "login` creates an optional Playwright storage state explicitly" in README_TEXT
    assert "crawl_seed` and `collect_nightly` can run without `--storage-state`" in README_TEXT
    assert "report_weekly` and `list_contactable` run from the SQLite database and do not require `--storage-state`" in README_TEXT
    assert "run_mode: background" in README_TEXT
    assert "HEARTBEAT.md" in README_TEXT
    assert "ack_event" in README_TEXT


def test_install_or_bootstrap_is_not_supported():
    result = run_handler(
        {"action": "install_or_bootstrap"},
        {"config": {"workspace_path": "."}},
    )

    assert result["status"] == "error"
    assert result["error_type"] == "validation_error"
    assert "Unsupported action" in result["message"]
    assert "install_or_bootstrap" not in result["suggested_fix"]


def test_handler_defaults_to_crawl_homefeed_when_action_is_omitted(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "accounts.csv").write_text("id\n", encoding="utf-8")
    (output_dir / "contact_leads.csv").write_text("id\n", encoding="utf-8")
    (output_dir / "run_report.json").write_text("{}", encoding="utf-8")
    commands = []

    def fake_run(argv, cwd, capture_output, text):
        commands.append(argv)
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {"workspace_path": str(tmp_path), "max_accounts": 3},
        {"config": {}},
    )

    assert result["status"] == "success"
    assert result["action"] == "crawl_homefeed"
    assert commands == [
        [
            "red-crawler",
            "crawl-homefeed",
            "--max-accounts",
            "3",
        ]
    ]


def test_background_crawl_returns_job_and_heartbeat(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    popen_calls = []

    class FakePopen:
        pid = 4321

        def __init__(self, argv, **kwargs):
            popen_calls.append((argv, kwargs))

    monkeypatch.setattr(INDEX_MODULE.subprocess, "Popen", FakePopen)

    result = run_handler(
        {
            "action": "crawl_homefeed",
            "workspace_path": str(tmp_path),
            "run_mode": "background",
            "max_accounts": 3,
        },
        {"config": {}},
    )

    assert result["status"] == "accepted"
    assert result["run_mode"] == "background"
    assert result["pid"] == 4321
    assert result["job_id"].startswith("crawl_homefeed_")
    assert len(popen_calls) == 1
    assert popen_calls[0][0][1].endswith("index.py")
    assert popen_calls[0][0][2] == "--run-job"

    job_path = Path(result["artifacts"]["job"])
    job = json.loads(job_path.read_text(encoding="utf-8"))
    assert job["status"] == "running"
    assert job["command"] == "red-crawler crawl-homefeed --max-accounts 3"
    assert job["wrapper_pid"] == 4321

    heartbeat = Path(result["artifacts"]["heartbeat"]).read_text(encoding="utf-8")
    assert "# red-crawler heartbeat" in heartbeat
    assert result["job_id"] in heartbeat
    assert "Pending user updates:\n- none" in heartbeat


def test_job_status_reads_job_and_tails_logs(tmp_path):
    heartbeat_dir = tmp_path / ".openclaw" / "red-crawler"
    job_dir = heartbeat_dir / "jobs"
    log_dir = tmp_path / "logs" / "jobs"
    job_dir.mkdir(parents=True)
    log_dir.mkdir(parents=True)
    stdout_log = log_dir / "job-1.out.log"
    stderr_log = log_dir / "job-1.err.log"
    stdout_log.write_text("one\ntwo\nthree\n", encoding="utf-8")
    stderr_log.write_text("warn\n", encoding="utf-8")
    job = {
        "job_id": "job-1",
        "action": "crawl_homefeed",
        "status": "succeeded",
        "summary": "crawl_homefeed completed successfully.",
        "stdout_log": str(stdout_log),
        "stderr_log": str(stderr_log),
        "artifacts": {"accounts.csv": str(tmp_path / "output" / "accounts.csv")},
    }
    (job_dir / "job-1.json").write_text(json.dumps(job), encoding="utf-8")

    result = run_handler(
        {
            "action": "job_status",
            "workspace_path": str(tmp_path),
            "job_id": "job-1",
            "tail_lines": 2,
        },
        {"config": {}},
    )

    assert result["status"] == "success"
    assert result["action"] == "job_status"
    assert result["job"]["status"] == "succeeded"
    assert result["stdout"] == "two\nthree"
    assert result["stderr"] == "warn"


def test_run_job_file_writes_completion_event_and_heartbeat(tmp_path, monkeypatch):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "accounts.csv").write_text("id\n", encoding="utf-8")
    (output_dir / "contact_leads.csv").write_text("id\n", encoding="utf-8")
    (output_dir / "run_report.json").write_text("{}", encoding="utf-8")
    resolved = {
        "action": "crawl_homefeed",
        "workspace_path": str(tmp_path),
        "output_dir": str(output_dir),
    }
    heartbeat_dir = tmp_path / ".openclaw" / "red-crawler"
    job_path = heartbeat_dir / "jobs" / "job-2.json"
    job = {
        "job_id": "job-2",
        "action": "crawl_homefeed",
        "status": "accepted",
        "argv": ["red-crawler", "crawl-homefeed"],
        "workspace_path": str(tmp_path),
        "stdout_log": str(tmp_path / "logs" / "jobs" / "job-2.out.log"),
        "stderr_log": str(tmp_path / "logs" / "jobs" / "job-2.err.log"),
        "resolved": resolved,
    }
    job_path.parent.mkdir(parents=True)
    job_path.write_text(json.dumps(job), encoding="utf-8")

    class FakePopen:
        pid = 9876

        def __init__(self, argv, **kwargs):
            self.argv = argv

        def wait(self):
            return 0

    monkeypatch.setattr(INDEX_MODULE.subprocess, "Popen", FakePopen)

    assert run_job_file(str(job_path)) == 0
    updated = json.loads(job_path.read_text(encoding="utf-8"))
    assert updated["status"] == "succeeded"
    assert updated["returncode"] == 0
    assert updated["process_pid"] == 9876
    assert updated["artifacts"]["accounts.csv"] == str(output_dir / "accounts.csv")

    events = (heartbeat_dir / "events" / "job-2.jsonl").read_text(encoding="utf-8")
    assert "crawl_homefeed completed successfully." in events
    heartbeat = (heartbeat_dir / "HEARTBEAT.md").read_text(encoding="utf-8")
    assert "Pending user updates:" in heartbeat
    assert "job-2" in heartbeat


def test_ack_event_removes_pending_heartbeat_update(tmp_path):
    heartbeat_dir = tmp_path / ".openclaw" / "red-crawler"
    event_dir = heartbeat_dir / "events"
    event_dir.mkdir(parents=True)
    event = {
        "event_id": "evt-1",
        "job_id": "job-3",
        "level": "info",
        "message": "done",
        "created_at": "2026-04-29T00:00:00+00:00",
    }
    (event_dir / "job-3.jsonl").write_text(
        json.dumps(event, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    result = run_handler(
        {
            "action": "ack_event",
            "workspace_path": str(tmp_path),
            "event_id": "evt-1",
        },
        {"config": {}},
    )

    assert result["status"] == "success"
    assert Path(result["artifacts"]["ack"]).exists()
    heartbeat = Path(result["artifacts"]["heartbeat"]).read_text(encoding="utf-8")
    assert "Pending user updates:\n- none" in heartbeat


def test_bootstrap_does_not_run_setup_or_login_by_default(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    commands = []

    def fake_run(argv, cwd, capture_output, text):
        commands.append(argv)
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "bootstrap",
            "workspace_path": str(tmp_path),
        },
        {"config": {}},
    )

    assert result["status"] == "success"
    assert result["action"] == "bootstrap"
    assert result["artifacts"] == {"workspace_path": str(tmp_path)}
    assert result["metrics"] == {
        "uv_sync_ran": False,
        "playwright_install_ran": False,
    }
    assert result["next_step"] == (
        "Run crawl_homefeed or crawl_seed; login is optional if you want an authenticated storage state."
    )
    assert commands == []


def test_bootstrap_runs_explicit_local_setup_steps(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    commands = []

    def fake_run(argv, cwd, capture_output, text):
        commands.append(argv)
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "bootstrap",
            "workspace_path": str(tmp_path),
            "sync_dependencies": True,
            "install_browser": True,
        },
        {"config": {}},
    )

    assert result["status"] == "success"
    assert result["metrics"] == {
        "uv_sync_ran": True,
        "playwright_install_ran": True,
    }
    assert commands == [
        ["uv", "sync"],
        ["red-crawler", "install-browsers"],
    ]


def test_crawl_seed_requires_seed_url():
    result = run_handler({"action": "crawl_seed"}, {"config": {}})
    assert result["status"] == "error"
    assert result["error_type"] == "validation_error"
    assert "seed_url" in result["message"]


def test_collect_nightly_requires_existing_workspace_without_storage_state():
    result = run_handler(
        {"action": "collect_nightly", "workspace_path": "/tmp/project"},
        {"config": {}},
    )
    assert result["status"] == "error"
    assert result["error_type"] == "configuration_error"
    assert "existing directory" in result["message"]


def test_crawl_seed_does_not_require_storage_state(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "accounts.csv").write_text("id\n", encoding="utf-8")
    (output_dir / "contact_leads.csv").write_text("id\n", encoding="utf-8")
    (output_dir / "run_report.json").write_text("{}", encoding="utf-8")
    commands = []

    def fake_run(argv, cwd, capture_output, text):
        commands.append(argv)
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "crawl_seed",
            "workspace_path": str(tmp_path),
            "seed_url": "https://www.xiaohongshu.com/user/profile/user-001",
        },
        {"config": {}},
    )
    assert result["status"] == "success"
    assert "--storage-state" not in commands[0]


def test_crawl_seed_requires_existing_storage_state_file(tmp_path):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    result = run_handler(
        {
            "action": "crawl_seed",
            "workspace_path": str(tmp_path),
            "storage_state": str(tmp_path / "state.json"),
            "seed_url": "https://www.xiaohongshu.com/user/profile/user-001",
        },
        {"config": {}},
    )
    assert result["status"] == "error"
    assert result["error_type"] == "configuration_error"
    assert "does not exist" in result["message"]
    assert "Run login first" in result["suggested_fix"]


def test_login_requires_storage_state(tmp_path):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    result = run_handler(
        {"action": "login", "workspace_path": str(tmp_path)},
        {"config": {}},
    )
    assert result["status"] == "error"
    assert result["error_type"] == "configuration_error"
    assert "storage_state" in result["message"]


def test_report_weekly_does_not_require_storage_state(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    (report_dir / "weekly-growth-report.json").write_text("{}", encoding="utf-8")
    (report_dir / "contactable_creators.csv").write_text("id\n1\n", encoding="utf-8")
    monkeypatch.setattr(
        INDEX_MODULE.subprocess,
        "run",
        lambda argv, cwd, capture_output, text: subprocess.CompletedProcess(
            argv, 0, stdout="", stderr=""
        ),
    )
    result = run_handler(
        {
            "action": "report_weekly",
            "workspace_path": str(tmp_path),
            "db_path": str(tmp_path / "data.db"),
            "report_dir": str(report_dir),
        },
        {"config": {}},
    )
    assert result["status"] == "success"
    assert result["action"] == "report_weekly"


def test_collect_nightly_uses_default_crawl_budget_from_context_config(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    (report_dir / "daily-run-report.json").write_text("{}", encoding="utf-8")
    (report_dir / "weekly-growth-report.json").write_text("{}", encoding="utf-8")
    (report_dir / "contactable_creators.csv").write_text("id\n1\n", encoding="utf-8")
    (tmp_path / "state.json").write_text("{}", encoding="utf-8")

    def fake_run(argv, cwd, capture_output, text):
        assert argv == [
            "red-crawler",
            "collect-nightly",
            "--storage-state",
            str(tmp_path / "state.json"),
            "--db-path",
            str(tmp_path / "data.db"),
            "--report-dir",
            str(report_dir),
            "--crawl-budget",
            "30",
        ]
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "collect_nightly",
            "workspace_path": str(tmp_path),
            "storage_state": str(tmp_path / "state.json"),
            "db_path": str(tmp_path / "data.db"),
            "report_dir": str(report_dir),
        },
        {"config": {"default_crawl_budget": 30}},
    )

    assert result["status"] == "success"
    assert result["action"] == "collect_nightly"


def test_report_weekly_uses_default_report_days_from_context_config(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    (report_dir / "weekly-growth-report.json").write_text("{}", encoding="utf-8")
    (report_dir / "contactable_creators.csv").write_text("id\n1\n", encoding="utf-8")

    def fake_run(argv, cwd, capture_output, text):
        assert argv == [
            "red-crawler",
            "report-weekly",
            "--db-path",
            str(tmp_path / "data.db"),
            "--report-dir",
            str(report_dir),
            "--days",
            "7",
        ]
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "report_weekly",
            "workspace_path": str(tmp_path),
            "db_path": str(tmp_path / "data.db"),
            "report_dir": str(report_dir),
        },
        {"config": {"default_report_days": 7}},
    )

    assert result["status"] == "success"
    assert result["action"] == "report_weekly"


def test_list_contactable_uses_default_list_limit_from_context_config(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")

    def fake_run(argv, cwd, capture_output, text):
        assert argv == [
            "red-crawler",
            "list-contactable",
            "--db-path",
            str(tmp_path / "data.db"),
            "--limit",
            "20",
            "--format",
            "csv",
        ]
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "list_contactable",
            "workspace_path": str(tmp_path),
            "db_path": str(tmp_path / "data.db"),
        },
        {"config": {"default_list_limit": 20}},
    )

    assert result["status"] == "success"
    assert result["action"] == "list_contactable"


def test_list_contactable_does_not_require_storage_state(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    monkeypatch.setattr(
        INDEX_MODULE.subprocess,
        "run",
        lambda argv, cwd, capture_output, text: subprocess.CompletedProcess(
            argv, 0, stdout="", stderr=""
        ),
    )
    result = run_handler(
        {
            "action": "list_contactable",
            "workspace_path": str(tmp_path),
            "db_path": str(tmp_path / "data.db"),
        },
        {"config": {}},
    )
    assert result["status"] == "success"
    assert result["action"] == "list_contactable"


def test_workspace_path_can_come_from_context_config(tmp_path, monkeypatch):
    monkeypatch.setattr(
        INDEX_MODULE.subprocess,
        "run",
        lambda argv, cwd, capture_output, text: subprocess.CompletedProcess(
            argv, 0, stdout="", stderr=""
        ),
    )
    result = run_handler(
        {"action": "LOGIN", "storage_state": str(tmp_path / "state.json")},
        {"config": {"workspace_path": str(tmp_path)}},
    )
    assert result["status"] == "success"
    assert result["action"] == "login"
    assert result["command"] == f"red-crawler login --save-state {tmp_path / 'state.json'}"


def test_handler_rejects_non_mapping_input(tmp_path):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    result = run_handler(
        "bad-input",
        {"config": {"workspace_path": str(tmp_path)}},
    )
    assert result["status"] == "error"
    assert result["error_type"] == "validation_error"
    assert "mapping" in result["message"]


def test_workspace_path_must_be_existing_directory(tmp_path):
    missing_dir = tmp_path / "missing"
    result = run_handler(
        {
            "action": "login",
            "workspace_path": str(missing_dir),
            "storage_state": str(tmp_path / "state.json"),
        },
        {"config": {}},
    )
    assert result["status"] == "error"
    assert result["error_type"] == "configuration_error"
    assert "existing directory" in result["message"]


def test_local_checkout_requirement_checks_pyproject(tmp_path):
    result = run_handler(
        {
            "action": "bootstrap",
            "workspace_path": str(tmp_path),
            "require_local_checkout": True,
        },
        {"config": {}},
    )
    assert result["status"] == "error"
    assert result["error_type"] == "configuration_error"
    assert "pyproject.toml" in result["message"]


def test_workspace_path_rejects_non_path_like_value():
    result = run_handler(
        {"action": "login", "workspace_path": 123, "storage_state": "/tmp/state.json"},
        {"config": {}},
    )
    assert result["status"] == "error"
    assert result["error_type"] == "configuration_error"
    assert "path-like" in result["message"]


def test_build_login_command_uses_overrides(tmp_path):
    command = build_command(
        {
            "action": "login",
            "workspace_path": str(tmp_path),
            "storage_state": "state.json",
            "login_url": "https://www.xiaohongshu.com/explore",
        }
    )
    assert command == [
        "red-crawler",
        "login",
        "--save-state",
        "state.json",
        "--login-url",
        "https://www.xiaohongshu.com/explore",
    ]


def test_build_command_splits_string_runner_command(tmp_path):
    command = build_command(
        {
            "action": "login",
            "workspace_path": str(tmp_path),
            "storage_state": "state.json",
            "runner_command": "uv run red-crawler",
        }
    )
    assert command[:3] == ["uv", "run", "red-crawler"]
    assert command[3:] == ["login", "--save-state", "state.json"]


def test_build_command_preserves_list_runner_command(tmp_path):
    command = build_command(
        {
            "action": "report_weekly",
            "workspace_path": str(tmp_path),
            "runner_command": ["python", "-m", "red_crawler.cli"],
            "db_path": "data/red_crawler.db",
            "report_dir": "reports",
            "days": 7,
        }
    )
    assert command == [
        "python",
        "-m",
        "red_crawler.cli",
        "report-weekly",
        "--db-path",
        "data/red_crawler.db",
        "--report-dir",
        "reports",
        "--days",
        "7",
    ]


def test_build_crawl_seed_command_uses_overrides(tmp_path):
    command = build_command(
        {
            "action": "crawl_seed",
            "workspace_path": str(tmp_path),
            "storage_state": "state.json",
            "seed_url": "https://www.xiaohongshu.com/user/profile/user-001",
            "output_dir": "output",
            "db_path": "data/red_crawler.db",
            "max_accounts": 15,
            "max_depth": 3,
            "include_note_recommendations": True,
        }
    )
    assert command == [
        "red-crawler",
        "crawl-seed",
        "--seed-url",
        "https://www.xiaohongshu.com/user/profile/user-001",
        "--storage-state",
        "state.json",
        "--max-accounts",
        "15",
        "--max-depth",
        "3",
        "--include-note-recommendations",
        "--db-path",
        "data/red_crawler.db",
        "--output-dir",
        "output",
    ]


def test_build_crawl_seed_command_supports_bright_data_browser(tmp_path):
    command = build_command(
        {
            "action": "crawl_seed",
            "workspace_path": str(tmp_path),
            "storage_state": "state.json",
            "seed_url": "https://www.xiaohongshu.com/user/profile/user-001",
            "browser_mode": "bright-data",
            "browser_auth": "user:pass",
        }
    )

    assert command == [
        "red-crawler",
        "crawl-seed",
        "--seed-url",
        "https://www.xiaohongshu.com/user/profile/user-001",
        "--storage-state",
        "state.json",
        "--browser-mode",
        "bright-data",
        "--browser-auth",
        "user:pass",
    ]


def test_build_crawl_homefeed_command_supports_proxy_rotation(tmp_path):
    command = build_command(
        {
            "action": "crawl_homefeed",
            "workspace_path": str(tmp_path),
            "proxy_list": "proxies.txt",
            "rotation_mode": "session",
            "rotation_retries": 2,
            "randomize_headers": False,
        }
    )

    assert command == [
        "red-crawler",
        "crawl-homefeed",
        "--proxy-list",
        "proxies.txt",
        "--rotation-mode",
        "session",
        "--rotation-retries",
        "2",
        "--no-randomize-headers",
    ]


def test_build_crawl_homefeed_command_uses_cosmetics_homefeed(tmp_path):
    command = build_command(
        {
            "action": "crawl_homefeed",
            "workspace_path": str(tmp_path),
            "homefeed_url": "https://www.xiaohongshu.com/explore?channel_id=homefeed.cosmetics_v3",
            "max_accounts": 8,
            "output_dir": "output",
        }
    )

    assert command == [
        "red-crawler",
        "crawl-homefeed",
        "--homefeed-url",
        "https://www.xiaohongshu.com/explore?channel_id=homefeed.cosmetics_v3",
        "--max-accounts",
        "8",
        "--output-dir",
        "output",
    ]


def test_build_collect_nightly_command_uses_overrides(tmp_path):
    command = build_command(
        {
            "action": "collect_nightly",
            "workspace_path": str(tmp_path),
            "storage_state": "state.json",
            "db_path": "data/red_crawler.db",
            "report_dir": "reports",
            "cache_dir": ".cache/red-crawler",
            "crawl_budget": 42,
            "search_term_limit": 5,
            "startup_jitter_minutes": 10,
            "slot_name": "nightly",
        }
    )
    assert command == [
        "red-crawler",
        "collect-nightly",
        "--storage-state",
        "state.json",
        "--db-path",
        "data/red_crawler.db",
        "--report-dir",
        "reports",
        "--cache-dir",
        ".cache/red-crawler",
        "--crawl-budget",
        "42",
        "--search-term-limit",
        "5",
        "--startup-jitter-minutes",
        "10",
        "--slot-name",
        "nightly",
    ]


def test_build_report_weekly_command_uses_overrides(tmp_path):
    command = build_command(
        {
            "action": "report_weekly",
            "workspace_path": str(tmp_path),
            "db_path": "data/red_crawler.db",
            "report_dir": "reports",
            "days": 14,
        }
    )
    assert command == [
        "red-crawler",
        "report-weekly",
        "--db-path",
        "data/red_crawler.db",
        "--report-dir",
        "reports",
        "--days",
        "14",
    ]


def test_build_list_contactable_command_uses_defaults_and_overrides(tmp_path):
    command = build_command(
        {
            "action": "list_contactable",
            "workspace_path": str(tmp_path),
            "db_path": "data/red_crawler.db",
            "min_relevance_score": 0.7,
            "limit": 25,
        }
    )
    assert command == [
        "red-crawler",
        "list-contactable",
        "--db-path",
        "data/red_crawler.db",
        "--min-relevance-score",
        "0.7",
        "--limit",
        "25",
        "--format",
        "csv",
    ]


def test_handler_returns_structured_success_for_report_weekly(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    weekly_report = report_dir / "weekly-growth-report.json"
    weekly_report.write_text("{}", encoding="utf-8")
    creators_csv = report_dir / "contactable_creators.csv"
    creators_csv.write_text("id\n1\n", encoding="utf-8")

    def fake_run(argv, cwd, capture_output, text):
        assert argv == [
            "red-crawler",
            "report-weekly",
            "--db-path",
            str(tmp_path / "data.db"),
            "--report-dir",
            str(report_dir),
            "--days",
            "7",
        ]
        assert cwd == tmp_path
        assert capture_output is True
        assert text is True
        return subprocess.CompletedProcess(argv, 0, stdout="weekly report ready", stderr="")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "report_weekly",
            "workspace_path": str(tmp_path),
            "db_path": str(tmp_path / "data.db"),
            "report_dir": str(report_dir),
            "days": 7,
        },
        {"config": {}},
    )

    assert result["status"] == "success"
    assert result["action"] == "report_weekly"
    assert result["command"] == (
        f"red-crawler report-weekly --db-path {tmp_path / 'data.db'} "
        f"--report-dir {report_dir} --days 7"
    )
    assert result["summary"] == "report_weekly completed successfully."
    assert result["artifacts"] == {
        "weekly-growth-report.json": str(weekly_report),
        "contactable_creators.csv": str(creators_csv),
    }
    assert result["stdout"] == "weekly report ready"
    assert result["stderr"] == ""


def test_handler_finds_relative_report_artifacts_under_workspace(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    weekly_report = report_dir / "weekly-growth-report.json"
    weekly_report.write_text("{}", encoding="utf-8")
    creators_csv = report_dir / "contactable_creators.csv"
    creators_csv.write_text("id\n1\n", encoding="utf-8")

    monkeypatch.setattr(
        INDEX_MODULE.subprocess,
        "run",
        lambda argv, cwd, capture_output, text: subprocess.CompletedProcess(
            argv, 0, stdout="ok", stderr=""
        ),
    )

    result = run_handler(
        {
            "action": "report_weekly",
            "workspace_path": str(tmp_path),
            "db_path": "data/red_crawler.db",
            "report_dir": "reports",
        },
        {"config": {}},
    )

    assert result["status"] == "success"
    assert result["artifacts"] == {
        "weekly-growth-report.json": str(weekly_report),
        "contactable_creators.csv": str(creators_csv),
    }


def test_handler_uses_default_output_dir_for_crawl_seed_artifacts(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    accounts_csv = output_dir / "accounts.csv"
    accounts_csv.write_text("id\n1\n", encoding="utf-8")
    contact_leads_csv = output_dir / "contact_leads.csv"
    contact_leads_csv.write_text("id\n1\n", encoding="utf-8")
    run_report_json = output_dir / "run_report.json"
    run_report_json.write_text("{}", encoding="utf-8")
    (tmp_path / "state.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        INDEX_MODULE.subprocess,
        "run",
        lambda argv, cwd, capture_output, text: subprocess.CompletedProcess(
            argv, 0, stdout="ok", stderr=""
        ),
    )

    result = run_handler(
        {
            "action": "crawl_seed",
            "workspace_path": str(tmp_path),
            "storage_state": str(tmp_path / "state.json"),
            "seed_url": "https://www.xiaohongshu.com/user/profile/user-001",
        },
        {"config": {}},
    )

    assert result["status"] == "success"
    assert result["artifacts"] == {
        "accounts.csv": str(accounts_csv),
        "contact_leads.csv": str(contact_leads_csv),
        "run_report.json": str(run_report_json),
    }


def test_handler_uses_default_report_dir_for_weekly_artifacts(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    weekly_report = report_dir / "weekly-growth-report.json"
    weekly_report.write_text("{}", encoding="utf-8")
    creators_csv = report_dir / "contactable_creators.csv"
    creators_csv.write_text("id\n1\n", encoding="utf-8")

    monkeypatch.setattr(
        INDEX_MODULE.subprocess,
        "run",
        lambda argv, cwd, capture_output, text: subprocess.CompletedProcess(
            argv, 0, stdout="ok", stderr=""
        ),
    )

    result = run_handler(
        {
            "action": "report_weekly",
            "workspace_path": str(tmp_path),
            "db_path": str(tmp_path / "data.db"),
        },
        {"config": {}},
    )

    assert result["status"] == "success"
    assert result["artifacts"] == {
        "weekly-growth-report.json": str(weekly_report),
        "contactable_creators.csv": str(creators_csv),
    }


def test_handler_maps_non_zero_exit_to_execution_error(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")

    def fake_run(argv, cwd, capture_output, text):
        return subprocess.CompletedProcess(argv, 2, stdout="", stderr="boom")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "report_weekly",
            "workspace_path": str(tmp_path),
            "db_path": str(tmp_path / "data.db"),
            "report_dir": str(tmp_path / "reports"),
        },
        {"config": {}},
    )

    assert result["status"] == "error"
    assert result["error_type"] == "execution_error"
    assert result["command"] == (
        f"red-crawler report-weekly --db-path {tmp_path / 'data.db'} "
        f"--report-dir {tmp_path / 'reports'}"
    )
    assert "exit code 2" in result["message"]
    assert result["stderr"] == "boom"
    assert "Inspect stderr" in result["suggested_fix"]


def test_handler_maps_subprocess_start_failure_to_execution_error(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")

    def fake_run(argv, cwd, capture_output, text):
        raise FileNotFoundError("red-crawler not found")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "report_weekly",
            "workspace_path": str(tmp_path),
            "db_path": str(tmp_path / "data.db"),
            "report_dir": str(tmp_path / "reports"),
        },
        {"config": {}},
    )

    assert result["status"] == "error"
    assert result["error_type"] == "execution_error"
    assert "failed to start" in result["message"]
    assert "red-crawler not found" in result["message"]
    assert result["command"] == (
        f"red-crawler report-weekly --db-path {tmp_path / 'data.db'} "
        f"--report-dir {tmp_path / 'reports'}"
    )
    assert "runner command is installed" in result["suggested_fix"]


def test_handler_returns_artifact_error_for_missing_crawl_seed_outputs(
    tmp_path, monkeypatch
):
    (tmp_path / "pyproject.toml").write_text(RED_CRAWLER_PYPROJECT, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "accounts.csv").write_text("id\n1\n", encoding="utf-8")
    (tmp_path / "state.json").write_text("{}", encoding="utf-8")

    def fake_run(argv, cwd, capture_output, text):
        return subprocess.CompletedProcess(argv, 0, stdout="done", stderr="")

    monkeypatch.setattr(INDEX_MODULE.subprocess, "run", fake_run)

    result = run_handler(
        {
            "action": "crawl_seed",
            "workspace_path": str(tmp_path),
            "storage_state": str(tmp_path / "state.json"),
            "seed_url": "https://www.xiaohongshu.com/user/profile/user-001",
            "output_dir": str(output_dir),
        },
        {"config": {}},
    )

    assert result["status"] == "error"
    assert result["error_type"] == "artifact_error"
    assert "contact_leads.csv" in result["message"]
    assert "run_report.json" in result["message"]
    assert result["command"] == (
        "red-crawler crawl-seed --seed-url "
        "https://www.xiaohongshu.com/user/profile/user-001 "
        f"--storage-state {tmp_path / 'state.json'} --output-dir {output_dir}"
    )
    assert "Verify the CLI completed" in result["suggested_fix"]
