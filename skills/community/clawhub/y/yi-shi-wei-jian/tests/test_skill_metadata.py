from __future__ import annotations

import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class SkillMetadataTestCase(unittest.TestCase):
    def test_skill_json_matches_slug(self) -> None:
        metadata = json.loads((REPO_ROOT / "skill.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["slug"], "yi-shi-wei-jian")
        self.assertEqual(metadata["repository_name"], "LearnFromHistory-skill")
        self.assertEqual(metadata["entry"], "SKILL.md")
        self.assertEqual(metadata["license"], "MIT")
        self.assertEqual(metadata["homepage"], "https://github.com/GreatXiaoRY/LearnFromHistory-skill")

    def test_skill_md_contains_frontmatter(self) -> None:
        content = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: yi-shi-wei-jian", content)
        self.assertIn("homepage: https://github.com/GreatXiaoRY/LearnFromHistory-skill", content)
        self.assertIn("user-invocable: true", content)
        self.assertIn('"slug":"yi-shi-wei-jian"', content)

    def test_skill_description_keeps_trigger_surface(self) -> None:
        content = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)[1]
        description = next(line for line in frontmatter.splitlines() if line.startswith("description:"))
        required_markers = [
            "请用/使用/调用",
            "以史为鉴",
            "借古鉴今",
            "历史类比",
            "沙盘推演",
            "organization/business/team",
            "reform",
            "internal conflict",
            "unstable alliance",
            "control-right",
            "leadership/personnel",
        ]
        for marker in required_markers:
            self.assertIn(marker, description)

    def test_release_files_exist(self) -> None:
        self.assertTrue((REPO_ROOT / "LICENSE").exists())
        self.assertTrue((REPO_ROOT / ".github" / "workflows" / "ci.yml").exists())
        self.assertTrue((REPO_ROOT / "data" / "user_cases.json").exists())
        self.assertTrue((REPO_ROOT / "examples" / "case_submission_template.json").exists())
        self.assertTrue((REPO_ROOT / "prompts" / "add_case_intake.md").exists())
        self.assertTrue((REPO_ROOT / "scripts" / "add_case.py").exists())
        self.assertTrue((REPO_ROOT / "src" / "case_store.py").exists())


if __name__ == "__main__":
    unittest.main()
