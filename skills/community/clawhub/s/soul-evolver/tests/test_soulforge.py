"""
SoulForge Unit Tests
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soulforge.config import SoulForgeConfig
from soulforge.memory_reader import MemoryReader, MemoryEntry
from soulforge.analyzer import PatternAnalyzer, DiscoveredPattern
from soulforge.evolver import SoulEvolver


def test_config_defaults():
    """Test configuration defaults."""
    config = SoulForgeConfig()
    assert config.workspace.endswith(".openclaw/workspace")
    assert config.trigger_threshold == 3
    assert config.get("backup_enabled") == True
    assert "SOUL.md" in [Path(f).name for f in config.target_files]
    print("✓ test_config_defaults passed")


def test_config_overrides():
    """Test configuration overrides."""
    config = SoulForgeConfig(overrides={
        "workspace": "/tmp/test-workspace",
        "trigger_threshold": 5,
    })
    assert config.workspace == "/tmp/test-workspace"
    assert config.trigger_threshold == 5
    print("✓ test_config_overrides passed")


def test_memory_entry_creation():
    """Test MemoryEntry dataclass."""
    entry = MemoryEntry(
        source="memory/2026-04-05.md",
        source_type="daily_log",
        category="conversation",
        content="Test content",
        timestamp="2026-04-05",
        importance=0.8,
    )
    assert entry.source == "memory/2026-04-05.md"
    assert entry.source_type == "daily_log"
    assert entry.content == "Test content"
    print("✓ test_memory_entry_creation passed")


def test_memory_reader_daily_logs():
    """Test reading daily memory logs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create memory directory
        memory_dir = Path(tmpdir) / "memory"
        memory_dir.mkdir()

        # Create test file
        test_file = memory_dir / "2026-04-05.md"
        test_file.write_text("# 2026-04-05\n\nTest conversation content here.")

        config = SoulForgeConfig(overrides={"workspace": tmpdir})
        reader = MemoryReader(tmpdir, config)
        entries = reader.read_all()

        assert len(entries) >= 1
        entry = entries[0]
        assert entry.source_type == "daily_log"
        print("✓ test_memory_reader_daily_logs passed")


def test_memory_reader_learnings():
    """Test reading learnings directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create learnings directory
        learnings_dir = Path(tmpdir) / ".learnings"
        learnings_dir.mkdir()

        # Create LEARNINGS.md
        learnings_file = learnings_dir / "LEARNINGS.md"
        learnings_file.write_text("""# Learnings

## correction

Some correction content here.

---

## insight

Some insight about the user.

---
""")

        config = SoulForgeConfig(overrides={"workspace": tmpdir})
        reader = MemoryReader(tmpdir, config)
        entries = reader.read_all()

        # Should have entries from learnings
        assert len(entries) >= 1
        categories = [e.category for e in entries]
        assert "correction" in categories or "insight" in categories
        print("✓ test_memory_reader_learnings passed")


def test_pattern_to_markdown_block():
    """Test DiscoveredPattern markdown formatting."""
    pattern = DiscoveredPattern(
        pattern_id="test_001",
        target_file="SOUL.md",
        update_type="SOUL",
        category="behavior",
        summary="User prefers numbered lists",
        content="User不喜欢看长文本选项，给选项时列序号让直接挑。",
        confidence=0.9,
        evidence_count=4,
        source_entries=["memory/2026-04-04.md", "memory/2026-04-05.md"],
    )

    block = pattern.to_markdown_block()
    assert "SoulForge Update" in block
    assert "User prefers numbered lists" in block
    assert "behavior" in block
    assert "4" in block  # evidence count
    print("✓ test_pattern_to_markdown_block passed")


def test_evolver_duplicate_filter():
    """Test that evolver filters duplicates."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = SoulForgeConfig(overrides={"workspace": tmpdir})
        evolver = SoulEvolver(tmpdir, config)

        # Existing content
        existing = "User prefers numbered lists\nMore content"

        pattern = DiscoveredPattern(
            pattern_id="test_001",
            target_file="SOUL.md",
            update_type="SOUL",
            category="behavior",
            summary="User prefers numbered lists",
            content="User不喜欢看长文本选项，给选项时列序号。",
            confidence=0.9,
            evidence_count=4,
            source_entries=["memory/2026-04-05.md"],
        )

        filtered = evolver._filter_duplicates([pattern], existing)
        assert len(filtered) == 0  # Should be filtered out
        print("✓ test_evolver_duplicate_filter passed")


def test_evolver_no_duplicate():
    """Test that evolver allows new patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = SoulForgeConfig(overrides={"workspace": tmpdir})
        evolver = SoulEvolver(tmpdir, config)

        existing = "Some existing content"
        pattern = DiscoveredPattern(
            pattern_id="test_001",
            target_file="SOUL.md",
            update_type="SOUL",
            category="behavior",
            summary="New pattern not in file",
            content="This is brand new information.",
            confidence=0.9,
            evidence_count=4,
            source_entries=["memory/2026-04-05.md"],
        )

        filtered = evolver._filter_duplicates([pattern], existing)
        assert len(filtered) == 1  # Should pass through
        print("✓ test_evolver_no_duplicate passed")


def test_evolver_dry_run():
    """Test evolver dry run mode."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = SoulForgeConfig(overrides={"workspace": tmpdir, "dry_run": True})
        evolver = SoulEvolver(tmpdir, config)

        # Create target file
        target_file = Path(tmpdir) / "SOUL.md"
        target_file.write_text("# SOUL.md\n\nExisting content.")

        pattern = DiscoveredPattern(
            pattern_id="test_001",
            target_file="SOUL.md",
            update_type="SOUL",
            category="behavior",
            summary="Test pattern",
            content="Test content to add.",
            confidence=0.9,
            evidence_count=4,
            source_entries=["memory/2026-04-05.md"],
        )

        results = evolver.apply_updates([pattern], dry_run=True)

        assert results["dry_run"] == True
        assert results["patterns_applied"] == 1
        # File should NOT be modified
        assert target_file.read_text() == "# SOUL.md\n\nExisting content."
        print("✓ test_evolver_dry_run passed")


def test_memory_reader_empty_workspace():
    """Test MemoryReader with no sources."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = SoulForgeConfig(overrides={"workspace": tmpdir})
        reader = MemoryReader(tmpdir, config)
        entries = reader.read_all()
        assert len(entries) == 0
        print("✓ test_memory_reader_empty_workspace passed")


def test_config_to_dict():
    """Test config serialization."""
    config = SoulForgeConfig(overrides={"workspace": "/test", "dry_run": True})
    d = config.to_dict()
    assert d["workspace"] == "/test"
    assert d["dry_run"] == True
    print("✓ test_config_to_dict passed")


def run_all_tests():
    """Run all tests."""
    print("Running SoulForge tests...")
    print("=" * 50)

    tests = [
        test_config_defaults,
        test_config_overrides,
        test_memory_entry_creation,
        test_memory_reader_daily_logs,
        test_memory_reader_learnings,
        test_pattern_to_markdown_block,
        test_evolver_duplicate_filter,
        test_evolver_no_duplicate,
        test_evolver_dry_run,
        test_memory_reader_empty_workspace,
        test_config_to_dict,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
