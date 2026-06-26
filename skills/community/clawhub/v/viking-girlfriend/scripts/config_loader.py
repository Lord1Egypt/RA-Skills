"""
config_loader.py — Sigrid's Multi-Format Data Loader
=====================================================

Loads and validates JSON, JSONL, YAML, Markdown, TXT, CSV, and PDF
from the viking_girlfriend_skill/data/ directory.

All loaded data is cached in memory after first load.
Never modifies base data files — read-only.

Norse framing: Mímir's Well holds all knowledge. This module is the bucket
that draws from it — robust, patient, never spilling.
"""

from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

logger = logging.getLogger(__name__)


@dataclass
class LoadResult:
    """Result of a data file load operation."""

    path: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    format_detected: str = "unknown"


class ConfigLoader:
    """Loads all data formats from the skill's data directory.

    Huginn scouts ahead — if a file cannot be read one way, he tries another.
    Cache keeps Muninn from flying the same path twice.
    """

    SUPPORTED_EXTENSIONS = {
        ".json", ".jsonl", ".yaml", ".yml", ".md", ".txt", ".csv"
    }

    def __init__(self, data_root: Union[str, Path]) -> None:
        self.data_root = Path(data_root).resolve()
        self._cache: Dict[str, Any] = {}

        if not self.data_root.exists():
            logger.warning(
                "Data root does not exist: %s — will return empty on all loads",
                self.data_root,
            )

    # ─── Public API ───────────────────────────────────────────────────────────

    def load(self, relative_path: str, use_cache: bool = True) -> LoadResult:
        """Load a file by path relative to data_root. Returns a LoadResult."""
        cache_key = relative_path.lower().strip()

        if use_cache and cache_key in self._cache:
            return LoadResult(
                path=relative_path, success=True,
                data=self._cache[cache_key], format_detected="cached",
            )

        full_path = self.data_root / relative_path
        result = self._load_file(full_path)

        if result.success and use_cache:
            self._cache[cache_key] = result.data

        return result

    def load_all_in_dir(
        self, relative_dir: str = "", extensions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Load all supported files in a subdirectory. Returns filename → data map."""
        target = self.data_root / relative_dir if relative_dir else self.data_root
        ext_filter = set(extensions or self.SUPPORTED_EXTENSIONS)
        results: Dict[str, Any] = {}

        if not target.is_dir():
            logger.warning("Directory not found: %s", target)
            return results

        for file_path in sorted(target.iterdir()):
            if file_path.is_file() and file_path.suffix.lower() in ext_filter:
                result = self._load_file(file_path)
                if result.success:
                    results[file_path.name] = result.data
                else:
                    logger.warning("Failed loading %s: %s", file_path.name, result.error)

        return results

    def get_cached(self, relative_path: str) -> Optional[Any]:
        """Return cached data for a path, or None if not yet loaded."""
        return self._cache.get(relative_path.lower().strip())

    def clear_cache(self) -> None:
        """Flush the cache — Muninn forgets, ready to learn again."""
        self._cache.clear()
        logger.debug("ConfigLoader cache cleared")

    # ─── Format dispatchers ───────────────────────────────────────────────────

    def _load_file(self, path: Path) -> LoadResult:
        """Dispatch to the correct loader based on file extension."""
        if not path.exists():
            return LoadResult(path=str(path), success=False, error="File not found")
        if not path.is_file():
            return LoadResult(path=str(path), success=False, error="Not a file")

        ext = path.suffix.lower()
        loaders = {
            ".json": self._load_json,
            ".jsonl": self._load_jsonl,
            ".yaml": self._load_yaml,
            ".yml": self._load_yaml,
            ".md": self._load_text,
            ".txt": self._load_text,
            ".csv": self._load_csv,
            ".pdf": self._load_pdf,
        }

        loader = loaders.get(ext, self._load_text)
        try:
            return loader(path)
        except Exception as exc:
            logger.error("Unhandled error loading %s: %s", path, exc)
            return LoadResult(path=str(path), success=False, error=str(exc))

    def _load_json(self, path: Path) -> LoadResult:
        """Load a JSON file — the most structured of all the runes."""
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return LoadResult(path=str(path), success=True, data=data, format_detected="json")
        except json.JSONDecodeError as exc:
            # Attempt recovery: strip BOM or trailing commas if present
            return self._load_json_recovering(path, original_error=str(exc))
        except Exception as exc:
            return LoadResult(path=str(path), success=False, error=str(exc))

    def _load_json_recovering(self, path: Path, original_error: str) -> LoadResult:
        """Second-attempt JSON load: strip BOM, try relaxed parsing."""
        try:
            raw = path.read_text(encoding="utf-8-sig").strip()
            data = json.loads(raw)
            logger.warning("Loaded %s with BOM stripping", path.name)
            return LoadResult(
                path=str(path), success=True, data=data, format_detected="json_recovered"
            )
        except Exception:
            return LoadResult(path=str(path), success=False, error=original_error)

    def _load_jsonl(self, path: Path) -> LoadResult:
        """Load a JSONL file as a list of records — each line a separate rune."""
        records: List[Any] = []
        errors: List[str] = []
        try:
            with open(path, "r", encoding="utf-8") as fh:
                for line_num, line in enumerate(fh, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError as exc:
                        errors.append(f"line {line_num}: {exc}")
        except Exception as exc:
            return LoadResult(path=str(path), success=False, error=str(exc))

        if errors:
            logger.warning("%s had %d parse errors: %s", path.name, len(errors), errors[:3])

        return LoadResult(
            path=str(path), success=True, data=records, format_detected="jsonl"
        )

    def _load_yaml(self, path: Path) -> LoadResult:
        """Load a YAML file — the saga written in the old tongue."""
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            return LoadResult(path=str(path), success=True, data=data, format_detected="yaml")
        except yaml.YAMLError as exc:
            return LoadResult(path=str(path), success=False, error=str(exc))
        except Exception as exc:
            return LoadResult(path=str(path), success=False, error=str(exc))

    def _load_text(self, path: Path) -> LoadResult:
        """Load a plain text or Markdown file as a string."""
        try:
            content = path.read_text(encoding="utf-8")
            fmt = "markdown" if path.suffix.lower() == ".md" else "text"
            return LoadResult(path=str(path), success=True, data=content, format_detected=fmt)
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1 if UTF-8 fails — old scrolls use older runes
                content = path.read_text(encoding="latin-1")
                return LoadResult(
                    path=str(path), success=True, data=content, format_detected="text_latin1"
                )
            except Exception as exc:
                return LoadResult(path=str(path), success=False, error=str(exc))
        except Exception as exc:
            return LoadResult(path=str(path), success=False, error=str(exc))

    def _load_csv(self, path: Path) -> LoadResult:
        """Load a CSV file as a list of dicts (header row → keys)."""
        try:
            rows: List[Dict[str, str]] = []
            with open(path, "r", encoding="utf-8", newline="") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    rows.append(dict(row))
            return LoadResult(path=str(path), success=True, data=rows, format_detected="csv")
        except Exception as exc:
            return LoadResult(path=str(path), success=False, error=str(exc))

    def _load_pdf(self, path: Path) -> LoadResult:
        """Load a PDF file as raw text. Requires pypdf or pdfminer if available."""
        try:
            import pypdf  # type: ignore
            reader = pypdf.PdfReader(str(path))
            pages = [page.extract_text() or "" for page in reader.pages]
            text = "\n\n".join(pages)
            return LoadResult(path=str(path), success=True, data=text, format_detected="pdf")
        except ImportError:
            pass

        try:
            from pdfminer.high_level import extract_text  # type: ignore
            text = extract_text(str(path))
            return LoadResult(path=str(path), success=True, data=text, format_detected="pdf")
        except ImportError:
            return LoadResult(
                path=str(path),
                success=False,
                error="No PDF library available (install pypdf or pdfminer.six)",
            )
        except Exception as exc:
            return LoadResult(path=str(path), success=False, error=str(exc))


# ─── Convenience helpers ──────────────────────────────────────────────────────

def make_config_loader(skill_root: Union[str, Path]) -> ConfigLoader:
    """Create a ConfigLoader pointed at the skill's data/ directory."""
    data_dir = Path(skill_root) / "data"
    return ConfigLoader(data_root=data_dir)
