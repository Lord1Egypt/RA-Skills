#!/usr/bin/env python3
"""Tests for session-continuity skill checkpoint system."""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add scripts dir to path for import
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import checkpoint


def test_save_and_list():
    """Test saving a checkpoint and listing it."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock workspace
        os.environ["OPENCLAW_WORKSPACE"] = tmpdir
        checkpoint.WORKSPACE = Path(tmpdir)
        checkpoint.CHECKPOINT_DIR = Path(tmpdir) / "memory" / "checkpoints"

        checkpoint.save_checkpoint("test-task", "Test task summary")
        checkpoint.save_checkpoint("another-task", "Another task")

        # List should show both
        old_stdout = sys.stdout
        sys.stdout = io.StringIO() if hasattr(sys, "StringIO") else None
        # Just verify no error
        checkpoint.list_checkpoints()
        sys.stdout = old_stdout


def test_checkpoint_file_format():
    """Verify checkpoint file contains required fields."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["OPENCLAW_WORKSPACE"] = tmpdir
        checkpoint.WORKSPACE = Path(tmpdir)
        checkpoint.CHECKPOINT_DIR = Path(tmpdir) / "memory" / "checkpoints"

        checkpoint.save_checkpoint("format-test", "Format test task")

        cp_file = checkpoint.CHECKPOINT_DIR / "format-test.md"
        content = cp_file.read_text()

        assert "# Checkpoint: format-test" in content
        assert "**Created:**" in content
        assert "**Task:** Format test task" in content
        assert "## Progress" in content
        assert "## Next Action" in content
        assert "## Blockers" in content


def test_delete_checkpoint():
    """Test deleting a checkpoint."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["OPENCLAW_WORKSPACE"] = tmpdir
        checkpoint.WORKSPACE = Path(tmpdir)
        checkpoint.CHECKPOINT_DIR = Path(tmpdir) / "memory" / "checkpoints"

        checkpoint.save_checkpoint("to-delete", "Will be deleted")
        assert checkpoint.checkpoint_exists("to-delete")

        checkpoint.delete_checkpoint("to-delete")
        assert not checkpoint.checkpoint_exists("to-delete")


def test_cannot_delete_autosave():
    """Autosave cannot be deleted via delete command."""
    try:
        checkpoint.delete_checkpoint("autosave")
        assert False, "Should have exited with error"
    except SystemExit:
        pass


if __name__ == "__main__":
    import io
    test_save_and_list()
    test_checkpoint_file_format()
    test_delete_checkpoint()
    test_cannot_delete_autosave()
    print("✅ All tests passed")