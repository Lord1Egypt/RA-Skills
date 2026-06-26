"""Consistency checking tools for cross-file validation."""

import re
from pathlib import Path


class ConsistencyChecker:
    """Check consistency across project files."""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)

    def check_character_names(self) -> dict:
        """Check character name consistency across all files.

        Returns:
            Dict with 'ok' (bool) and 'issues' (list of strings).
        """
        issues = []

        # Load official character names from assets
        official_names = self._load_asset_names("characters")

        if not official_names:
            return {"ok": True, "issues": ["未找到角色资产，跳过角色一致性检查。"]}

        # Check all markdown files for undefined characters
        md_files = list(self.project_path.rglob("*.md"))
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            found_names = self._extract_names_from_text(content)

            for name in found_names:
                if name not in official_names and len(name) >= 2:
                    # Might be a nickname or misspelling
                    issues.append(
                        f"{md_file.relative_to(self.project_path)}: "
                        f"发现未定义的角色名 \"{name}\""
                    )

        return {"ok": len(issues) == 0, "issues": issues}

    def check_scene_names(self) -> dict:
        """Check scene name consistency."""
        issues = []
        official_names = self._load_asset_names("scenes")

        if not official_names:
            return {"ok": True, "issues": ["未找到场景资产，跳过场景一致性检查。"]}

        md_files = list(self.project_path.rglob("*.md"))
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            found_names = self._extract_scene_names_from_text(content)

            for name in found_names:
                if name not in official_names and len(name) >= 2:
                    issues.append(
                        f"{md_file.relative_to(self.project_path)}: "
                        f"发现未定义的场景名 \"{name}\""
                    )

        return {"ok": len(issues) == 0, "issues": issues}

    def check_prop_names(self) -> dict:
        """Check prop name consistency."""
        issues = []
        official_names = self._load_asset_names("props")

        if not official_names:
            return {"ok": True, "issues": ["未找到道具资产，跳过道具一致性检查。"]}

        md_files = list(self.project_path.rglob("*.md"))
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            found_names = self._extract_prop_names_from_text(content)

            for name in found_names:
                if name not in official_names and len(name) >= 2:
                    issues.append(
                        f"{md_file.relative_to(self.project_path)}: "
                        f"发现未定义的道具名 \"{name}\""
                    )

        return {"ok": len(issues) == 0, "issues": issues}

    def check_style_drift(self) -> dict:
        """Check if style descriptions are consistent across files.

        Returns:
            Dict with 'ok' and 'issues'.
        """
        issues = []

        # Load project style
        try:
            import json
            with open(self.project_path / "project.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            project_style = data.get("artStyle", "")
        except Exception:
            return {"ok": True, "issues": ["无法读取 project.json，跳过风格检查。"]}

        # Check style references in image generation prompts
        storyboard_files = list((self.project_path / "storyboard").rglob("*.md"))
        for sb_file in storyboard_files:
            content = sb_file.read_text(encoding="utf-8")
            # Simple check: look for style keywords that don't match
            # This is a heuristic check
            if project_style and project_style not in content:
                issues.append(
                    f"{sb_file.relative_to(self.project_path)}: "
                    f"分镜提示词中未包含项目风格 \"{project_style}\""
                )

        return {"ok": len(issues) == 0, "issues": issues}

    def run_all(self) -> dict:
        """Run all consistency checks.

        Returns:
            Dict with overall 'ok' and per-check results.
        """
        results = {
            "characters": self.check_character_names(),
            "scenes": self.check_scene_names(),
            "props": self.check_prop_names(),
            "style": self.check_style_drift(),
        }

        all_ok = all(r["ok"] for r in results.values())
        return {"ok": all_ok, "checks": results}

    def _load_asset_names(self, asset_type: str) -> set[str]:
        """Load official asset names from data.json."""
        data_file = self.project_path / "assets" / "data.json"
        if not data_file.exists():
            return set()

        try:
            import json
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            items = data.get(asset_type, [])
            return {item.get("name", "") for item in items if item.get("name")}
        except Exception:
            return set()

    @staticmethod
    def _extract_names_from_text(text: str) -> set[str]:
        """Extract potential character names from text.

        This is a heuristic using common Chinese naming patterns.
        """
        # Match 2-4 character names after common markers
        patterns = [
            r'[一-鿿]{2,4}(?=[（\(]\s*[^\)）]*[）\)])',  # 角色名（表情）
            r'(?<=\n)[一-鿿]{2,4}(?=\s*[：:])',  # 角色名：台词
        ]

        names = set()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            names.update(matches)

        # Filter out common non-name words
        non_names = {"场景", "时间", "地点", "人物", "道具", "镜头", "画面", "对白", "台词",
                     "动作", "表情", "音效", "背景音乐", "环境音", "转场", "特写"}
        return names - non_names

    @staticmethod
    def _extract_scene_names_from_text(text: str) -> set[str]:
        """Extract potential scene names from text."""
        # Match scene headers or references
        patterns = [
            r'(?<=场景[：:]\s*)[一-鿿\w\s]{2,20}',
            r'(?<=※\s*)[一-鿿\w\s]{2,20}',
        ]

        names = set()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            names.update(m.strip() for m in matches)

        return names

    @staticmethod
    def _extract_prop_names_from_text(text: str) -> set[str]:
        """Extract potential prop names from text."""
        # Match prop references
        patterns = [
            r'(?<=道具[：:]\s*)[一-鿿\w\s]{2,20}',
            r'(?<=【道具[：:]\s*)[一-鿿\w\s]{2,20}(?=】)',
        ]

        names = set()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            names.update(m.strip() for m in matches)

        return names
