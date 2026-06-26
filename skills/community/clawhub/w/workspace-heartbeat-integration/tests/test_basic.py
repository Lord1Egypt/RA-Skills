"""
Unit tests for workspace-heartbeat-integration
"""

import os
import sys
import json
import tempfile
from datetime import datetime
from pathlib import Path

# Add source to path
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "source"))

from integration import HeartbeatIntegration


def test_heartbeat_integration_basic():
    """Test basic initialization and config loading."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["WORKSPACE"] = tmpdir  # Override workspace for testing
        integration = HeartbeatIntegration()
        assert integration.workspace is not None
        print("✅ Basic initialization OK")


def test_ensure_today_log():
    """Test today's log creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        memory_dir = tmp / "memory"
        memory_dir.mkdir()
        state_file = memory_dir / "heartbeat-state.json"
        state_file.write_text("{}")

        # Patch paths
        integration = HeartbeatIntegration()
        integration.workspace = tmp
        integration.memory_dir = memory_dir
        integration.state_file = state_file

        log_path = integration.ensure_today_log()
        assert log_path.exists()
        content = log_path.read_text()
        assert "学习日志" in content
        print("✅ Today log creation OK")


def test_append_work_log():
    """Test appending work log entries."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        memory_dir = tmp / "memory"
        memory_dir.mkdir()
        state_file = memory_dir / "heartbeat-state.json"
        state_file.write_text("{}")

        integration = HeartbeatIntegration()
        integration.workspace = tmp
        integration.memory_dir = memory_dir
        integration.state_file = state_file

        log_path = integration.append_work_log("learning", "Test skill development")
        content = log_path.read_text()
        assert "Test skill development" in content
        print("✅ Work log append OK")


def test_sync():
    """Test heartbeat sync."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        memory_dir = tmp / "memory"
        memory_dir.mkdir()
        state_file = memory_dir / "heartbeat-state.json"
        state_file.write_text('{"lastChecks": {}}')

        integration = HeartbeatIntegration()
        integration.workspace = tmp
        integration.memory_dir = memory_dir
        integration.state_file = state_file

        state = integration.sync(dry_run=True)
        assert "lastChecks" in state
        print("✅ Sync (dry run) OK")


def test_generate_report():
    """Test report generation."""
    import integration
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        memory_dir = tmp / "memory"
        memory_dir.mkdir()
        state_file = memory_dir / "heartbeat-state.json"
        state_file.write_text('{"lastChecks": {"hourly": 1234567890}, "notes": "Test"}')

        # Patch TASK_BOARD to a temp file with some content
        task_board = tmp / "TASK_BOARD.md"
        task_board.write_text("## 🚧 开发中\n... content ...\n")
        integration.TASK_BOARD = task_board

        integration_obj = integration.HeartbeatIntegration()
        integration_obj.workspace = tmp
        integration_obj.memory_dir = memory_dir
        integration_obj.state_file = state_file

        report = integration_obj.generate_report(output_format="text")
        assert "Heartbeat Report" in report
        assert "Last Checks" in report  # Section header
        print("✅ Report generation OK")


if __name__ == "__main__":
    print("🧪 Running workspace-heartbeat-integration tests...\n")
    test_heartbeat_integration_basic()
    test_ensure_today_log()
    test_append_work_log()
    test_sync()
    test_generate_report()
    print("\n✅ All tests passed!")