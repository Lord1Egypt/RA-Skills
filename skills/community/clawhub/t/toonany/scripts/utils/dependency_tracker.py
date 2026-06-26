"""Dependency tracker for change propagation across pipeline stages."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class DependencyTracker:
    """Track file versions and dependencies in project.json."""

    DEPENDENCY_GRAPH = {
        "storyline.md": [],
        "outline/outline-{ep}.md": ["storyline.md"],
        "assets/data.json": ["outline/outline-{ep}.md"],
        "assets/images/*": ["assets/data.json"],
        "script/script-{ep}.md": ["outline/outline-{ep}.md"],
        "storyboard/storyboard-{ep}.md": ["script/script-{ep}.md"],
        "storyboard/images/*": ["storyboard/storyboard-{ep}.md", "assets/images/*"],
        "video/ep{ep}-*.mp4": ["storyboard/images/*"],
        "audio/ep{ep}/*": ["script/script-{ep}.md"],
        "subtitle/ep{ep}.srt": ["audio/ep{ep}/*"],
        "final/episode{ep}.mp4": ["video/ep{ep}-*.mp4", "audio/ep{ep}/*", "subtitle/ep{ep}.srt"],
    }

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.config_file = self.project_path / "project.json"

    def _load_versions(self) -> dict:
        """Load versions from project.json."""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("versions", {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_versions(self, versions: dict) -> None:
        """Save versions to project.json."""
        with open(self.config_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["versions"] = versions

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def bump_version(self, file_path: str, depends_on: Optional[list[str]] = None) -> None:
        """Bump version for a file.

        Args:
            file_path: Relative path from project root.
            depends_on: List of upstream files this file depends on.
        """
        versions = self._load_versions()

        current = versions.get(file_path, {"version": 0})
        new_version = current.get("version", 0) + 1

        versions[file_path] = {
            "version": new_version,
            "timestamp": datetime.now().isoformat(),
        }

        if depends_on:
            versions[file_path]["depends_on"] = depends_on

        self._save_versions(versions)

    def check_stale(self) -> list[dict]:
        """Check for stale files (downstream files with older versions than upstream).

        Returns:
            List of stale file entries with reason.
        """
        versions = self._load_versions()
        stale = []

        for file_path, info in versions.items():
            depends_on = info.get("depends_on", [])
            current_version = info.get("version", 0)

            for upstream in depends_on:
                upstream_info = versions.get(upstream)
                if not upstream_info:
                    stale.append({
                        "file": file_path,
                        "reason": f"上游文件 {upstream} 不存在",
                    })
                    continue

                upstream_version = upstream_info.get("version", 0)
                if upstream_version > current_version:
                    stale.append({
                        "file": file_path,
                        "reason": f"上游 {upstream} 已更新 (v{upstream_version} > v{current_version})",
                    })

        return stale

    def get_downstream(self, file_path: str) -> list[str]:
        """Get list of downstream files that depend on given file.

        Args:
            file_path: Path of the upstream file.

        Returns:
            List of downstream file paths.
        """
        versions = self._load_versions()
        downstream = []

        for fp, info in versions.items():
            depends_on = info.get("depends_on", [])
            if file_path in depends_on:
                downstream.append(fp)

        return downstream

    def format_stale_report(self, stale: list[dict]) -> str:
        """Format stale files into user-friendly message."""
        if not stale:
            return "所有文件都是最新的。"

        lines = ["以下文件可能已过期，建议重新生成：", ""]
        for item in stale:
            lines.append(f"  - {item['file']}: {item['reason']}")

        return "\n".join(lines)
