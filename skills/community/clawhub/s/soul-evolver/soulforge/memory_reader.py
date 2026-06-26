"""
SoulForge Memory Reader
Reads memory files from multiple sources: daily logs, learnings, hawk-bridge vector store.
"""

import os
import json
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    """A single memory entry from any source."""
    source: str          # File path or source name
    source_type: str     # "daily_log" | "learning" | "error" | "feature_req" | "hawk_bridge"
    category: str        # "correction" | "insight" | "decision" | "preference" | "error" | etc.
    content: str         # The actual content
    timestamp: Optional[str] = None
    importance: float = 0.5  # 0.0 - 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"[{self.source_type}] {self.content[:100]}"


class MemoryReader:
    """
    Reads memory entries from various sources in the workspace.

    Sources:
    - memory/YYYY-MM-DD.md: Daily conversation logs
    - .learnings/LEARNINGS.md: Corrections, insights, knowledge gaps
    - .learnings/ERRORS.md: Command failures
    - .learnings/FEATURE_REQUESTS.md: User requests
    - hawk-bridge vector store (optional): Semantic memory
    """

    def __init__(self, workspace: str, config):
        """
        Initialize memory reader.

        Args:
            workspace: Path to workspace directory
            config: SoulForgeConfig instance
        """
        self.workspace = Path(workspace)
        self.config = config
        self._entries: List[MemoryEntry] = []

    def read_all(self) -> List[MemoryEntry]:
        """
        Read all memory sources and return unified list of entries.

        Returns:
            List of MemoryEntry objects sorted by timestamp (newest first)
        """
        self._entries = []

        # Read daily memory logs
        self._read_daily_logs()

        # Read learnings
        self._read_learnings()

        # Read hawk-bridge if available
        if self.config.get("hawk_bridge_enabled", True):
            self._read_hawk_bridge()

        # Sort by timestamp (newest first)
        self._entries.sort(
            key=lambda e: e.timestamp or "1970-01-01",
            reverse=True
        )

        logger.info(f"Read {len(self._entries)} memory entries from all sources")
        return self._entries

    def _read_daily_logs(self) -> None:
        """Read memory/*.md daily logs."""
        memory_dir = self.workspace / "memory"
        if not memory_dir.exists():
            logger.debug(f"Memory directory not found: {memory_dir}")
            return

        for md_file in sorted(memory_dir.glob("*.md"), reverse=True):
            try:
                content = md_file.read_text(encoding="utf-8")
                # Skip the template/BOOTSTRAP files
                if md_file.name in ["BOOTSTRAP.md"]:
                    continue
                entry = MemoryEntry(
                    source=str(md_file.relative_to(self.workspace)),
                    source_type="daily_log",
                    category="conversation",
                    content=self._extract_text_content(content),
                    timestamp=md_file.stem,  # YYYY-MM-DD
                    importance=0.6,
                    metadata={"file": str(md_file.name)}
                )
                self._entries.append(entry)
            except Exception as e:
                logger.warning(f"Failed to read {md_file}: {e}")

    def _read_learnings(self) -> None:
        """Read .learnings/ directory files."""
        learnings_dir = self.workspace / ".learnings"
        if not learnings_dir.exists():
            logger.debug(f"Learnings directory not found: {learnings_dir}")
            return

        # LEARNINGS.md - corrections, insights, knowledge gaps
        learnings_file = learnings_dir / "LEARNINGS.md"
        if learnings_file.exists():
            self._parse_learnings_md(learnings_file)

        # ERRORS.md - command failures
        errors_file = learnings_dir / "ERRORS.md"
        if errors_file.exists():
            self._parse_errors_md(errors_file)

        # FEATURE_REQUESTS.md
        features_file = learnings_dir / "FEATURE_REQUESTS.md"
        if features_file.exists():
            self._parse_feature_requests_md(features_file)

    def _parse_learnings_md(self, file_path: Path) -> None:
        """Parse LEARNINGS.md format."""
        try:
            content = file_path.read_text(encoding="utf-8")
            # Split by --- separators
            sections = content.split("\n---\n")
            for section in sections:
                if not section.strip() or section.startswith("#"):
                    continue
                # Extract category from ## header
                lines = section.strip().split("\n")
                category = "insight"
                for line in lines:
                    if line.startswith("## "):
                        # Extract category keyword
                        header = line[3:].lower()
                        if "correction" in header:
                            category = "correction"
                        elif "knowledge_gap" in header:
                            category = "knowledge_gap"
                        elif "best_practice" in header:
                            category = "best_practice"
                        elif "insight" in header:
                            category = "insight"
                        break

                # Get content text
                text_content = self._extract_text_content(section)
                if text_content.strip():
                    entry = MemoryEntry(
                        source=str(file_path.relative_to(self.workspace)),
                        source_type="learning",
                        category=category,
                        content=text_content,
                        importance=0.8 if category == "correction" else 0.6,
                        metadata={}
                    )
                    self._entries.append(entry)
        except Exception as e:
            logger.warning(f"Failed to parse {file_path}: {e}")

    def _parse_errors_md(self, file_path: Path) -> None:
        """Parse ERRORS.md format."""
        try:
            content = file_path.read_text(encoding="utf-8")
            sections = content.split("\n---\n")
            for section in sections:
                if not section.strip() or section.startswith("#"):
                    continue
                text_content = self._extract_text_content(section)
                if text_content.strip():
                    entry = MemoryEntry(
                        source=str(file_path.relative_to(self.workspace)),
                        source_type="error",
                        category="error",
                        content=text_content,
                        importance=0.9,
                        metadata={}
                    )
                    self._entries.append(entry)
        except Exception as e:
            logger.warning(f"Failed to parse {file_path}: {e}")

    def _parse_feature_requests_md(self, file_path: Path) -> None:
        """Parse FEATURE_REQUESTS.md format."""
        try:
            content = file_path.read_text(encoding="utf-8")
            sections = content.split("\n---\n")
            for section in sections:
                if not section.strip() or section.startswith("#"):
                    continue
                text_content = self._extract_text_content(section)
                if text_content.strip():
                    entry = MemoryEntry(
                        source=str(file_path.relative_to(self.workspace)),
                        source_type="feature_request",
                        category="feature_request",
                        content=text_content,
                        importance=0.5,
                        metadata={}
                    )
                    self._entries.append(entry)
        except Exception as e:
            logger.warning(f"Failed to parse {file_path}: {e}")

    def _read_hawk_bridge(self) -> None:
        """
        Read from hawk-bridge LanceDB vector store.
        This is optional - gracefully skip if not available.
        """
        try:
            import sys
            hawk_path = self.config.get("hawk_bridge_path")
            if not hawk_path:
                # Try common locations
                for candidate in [
                    self.workspace.parent / "context-hawk" / "hawk",
                    Path("~/.openclaw/workspace/context-hawk/hawk").expanduser(),
                ]:
                    if candidate.exists():
                        hawk_path = str(candidate)
                        break

            if not hawk_path or not Path(hawk_path).exists():
                logger.debug("hawk-bridge path not found, skipping vector memory")
                return

            sys.path.insert(0, hawk_path)

            # Try to read from LanceDB
            db_path = self.config.get("hawk_db_path", "~/.hawk/lancedb")
            table_name = self.config.get("hawk_table_name", "hawk_memories")

            import lancedb
            db = lancedb.connect(str(Path(db_path).expanduser()))
            if table_name in db.table_names():
                table = db.open_table(table_name)
                # Get recent entries (last 50)
                count = min(table.count_rows(), 50)
                if count > 0:
                    logger.info(f"Read {count} entries from hawk-bridge vector store")
                    # Note: LanceDB returns records in arbitrary order
                    # We can't easily get them all, so we'll just note count
        except ImportError:
            logger.debug("lancedb not available, skipping hawk-bridge vector store")
        except Exception as e:
            logger.warning(f"Failed to read hawk-bridge: {e}")

    def _extract_text_content(self, markdown_text: str) -> str:
        """
        Extract plain text content from markdown, removing headers, code blocks, etc.
        """
        lines = markdown_text.split("\n")
        result_lines = []
        in_code_block = False

        for line in lines:
            # Toggle code block state
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # Skip content inside code blocks
            if in_code_block:
                continue

            # Skip headers
            if line.strip().startswith("#"):
                continue

            # Skip markdown list markers but keep content
            stripped = line.strip()
            if stripped.startswith("- ") or stripped.startswith("* "):
                stripped = stripped[2:]
            elif stripped.startswith("##") or stripped.startswith("**"):
                continue

            # Clean up bold/italic markers
            stripped = stripped.replace("**", "").replace("*", "").replace("__", "")

            # Skip lines that are just metadata/key-value pairs
            if ":" in stripped and not len(stripped) > 100:
                # Likely a metadata line, skip
                if any(stripped.startswith(k) for k in ["Source:", "Tags:", "Area:", "Pattern-Key:"]):
                    continue

            if stripped.strip():
                result_lines.append(stripped.strip())

        return " ".join(result_lines)

    def get_entries_by_category(self, category: str) -> List[MemoryEntry]:
        """Get all entries matching a specific category."""
        return [e for e in self._entries if e.category == category]

    def get_recent_entries(self, days: int = 7) -> List[MemoryEntry]:
        """Get entries from the last N days."""
        from datetime import datetime, timedelta
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return [e for e in self._entries if e.timestamp and e.timestamp >= cutoff]

    def summarize(self) -> Dict[str, Any]:
        """Get a summary of all memory sources."""
        return {
            "total_entries": len(self._entries),
            "by_source_type": self._count_by("source_type"),
            "by_category": self._count_by("category"),
            "sources": list(set(e.source for e in self._entries)),
        }

    def _count_by(self, attr: str) -> Dict[str, int]:
        """Count entries by a specific attribute."""
        counts = {}
        for entry in self._entries:
            key = getattr(entry, attr, "unknown")
            counts[key] = counts.get(key, 0) + 1
        return counts
