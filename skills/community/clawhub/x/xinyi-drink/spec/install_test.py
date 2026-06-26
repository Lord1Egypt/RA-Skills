from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class InstallScriptTest(unittest.TestCase):
    def test_install_script_excludes_pycache_directories(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            home_dir = tmp_path / "home"
            home_dir.mkdir()
            (home_dir / ".agents").mkdir()

            result = subprocess.run(
                ["sh", str(skill_root / "install.sh")],
                cwd=skill_root,
                env={
                    **dict(__import__("os").environ),
                    "HOME": str(home_dir),
                },
                capture_output=True,
                check=True,
                text=True,
            )

            installed_root = home_dir / ".agents" / "skills" / "xinyi-drink"
            self.assertTrue(installed_root.exists())
            self.assertTrue((installed_root / "skill.json").exists())
            self.assertTrue((installed_root / "references" / "response-examples.md").exists())
            self.assertFalse(any(installed_root.rglob("__pycache__")))
            self.assertIn("已安装 xinyi-drink 到", result.stdout)
            self.assertIn("安装完成后，推荐固定展示这四个问题：", result.stdout)
            self.assertIn("领取Skill用户大礼包", result.stdout)
            self.assertIn("查询及分析个人历史订单", result.stdout)
            self.assertIn("查询菜单及饮品热量", result.stdout)
            self.assertIn("查询门店及等候时长", result.stdout)
            self.assertNotIn("给我推荐一杯适合当下午茶的饮品", result.stdout)
            self.assertIn("隐私提示", result.stdout)
            self.assertIn("本机缓存已确认领取成功后，不能更换手机号重复领取", result.stdout)
            self.assertIn("领取结果以服务端响应为准", result.stdout)
            self.assertIn("最终用户回答不要主动解释内部领取规则", result.stdout)
            self.assertNotIn("活动周期", result.stdout)
            self.assertNotIn("领取尝试过多", result.stdout)
            self.assertIn("XINYI_API_BASE_URL", result.stdout)
            self.assertIn("~/.xinyi-drink/state.json", result.stdout)
            self.assertNotIn("告知小程序绑定的手机号", result.stdout)

    def test_install_script_maps_openclaw_to_openclaw_skills_dir(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            home_dir = tmp_path / "home"
            home_dir.mkdir()

            result = subprocess.run(
                ["sh", str(skill_root / "install.sh"), "--dry-run", "--platform", "openclaw"],
                cwd=skill_root,
                env={
                    **dict(__import__("os").environ),
                    "HOME": str(home_dir),
                },
                capture_output=True,
                check=True,
                text=True,
            )

            self.assertIn(
                str(home_dir / ".openclaw" / "skills" / "xinyi-drink"),
                result.stdout,
            )

    def test_install_script_maps_hermes_to_hermes_skills_dir(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            home_dir = tmp_path / "home"
            home_dir.mkdir()

            result = subprocess.run(
                ["sh", str(skill_root / "install.sh"), "--dry-run", "--platform", "hermes"],
                cwd=skill_root,
                env={
                    **dict(__import__("os").environ),
                    "HOME": str(home_dir),
                },
                capture_output=True,
                check=True,
                text=True,
            )

            self.assertIn(
                str(home_dir / ".hermes" / "skills" / "xinyi-drink"),
                result.stdout,
            )

    def test_install_script_accepts_platform_case_insensitively(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            home_dir = tmp_path / "home"
            home_dir.mkdir()

            result = subprocess.run(
                ["sh", str(skill_root / "install.sh"), "--dry-run", "--platform", "LobsterAI"],
                cwd=skill_root,
                env={
                    **dict(__import__("os").environ),
                    "HOME": str(home_dir),
                },
                capture_output=True,
                check=True,
                text=True,
            )

            self.assertIn(
                str(home_dir / ".agents" / "skills" / "xinyi-drink"),
                result.stdout,
            )

    def test_install_script_backs_up_existing_installation_before_overwrite(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            home_dir = tmp_path / "home"
            home_dir.mkdir()
            (home_dir / ".agents").mkdir()

            env = {
                **dict(__import__("os").environ),
                "HOME": str(home_dir),
            }
            subprocess.run(
                ["sh", str(skill_root / "install.sh")],
                cwd=skill_root,
                env=env,
                capture_output=True,
                check=True,
                text=True,
            )
            installed_root = home_dir / ".agents" / "skills" / "xinyi-drink"
            marker = installed_root / "local-marker.txt"
            marker.write_text("previous install", encoding="utf-8")

            result = subprocess.run(
                ["sh", str(skill_root / "install.sh")],
                cwd=skill_root,
                env=env,
                capture_output=True,
                check=True,
                text=True,
            )

            backups = sorted((home_dir / ".agents" / "skills").glob("xinyi-drink.backup.*"))
            self.assertTrue(backups)
            self.assertTrue((backups[-1] / "local-marker.txt").exists())
            self.assertIn("已备份旧版本到", result.stdout)

    def test_cursor_install_targets_repo_root_when_run_from_skill_dir(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            copied_skill_root = tmp_path / "skill"
            shutil.copytree(skill_root, copied_skill_root)

            subprocess.run(
                ["sh", str(copied_skill_root / "install.sh"), "--platform", "cursor"],
                cwd=copied_skill_root,
                capture_output=True,
                check=True,
                text=True,
            )

            self.assertTrue((tmp_path / ".cursor" / "rules" / "xinyi-drink").exists())
            self.assertFalse((copied_skill_root / ".cursor" / "rules" / "xinyi-drink").exists())

    def test_check_installed_reports_drift_without_overwriting(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            home_dir = tmp_path / "home"
            home_dir.mkdir()
            installed_root = home_dir / ".agents" / "skills" / "xinyi-drink"
            installed_root.mkdir(parents=True)
            (installed_root / "SKILL.md").write_text("old install", encoding="utf-8")

            result = subprocess.run(
                ["sh", str(skill_root / "install.sh"), "--platform", "codex", "--check-installed"],
                cwd=skill_root,
                env={
                    **dict(__import__("os").environ),
                    "HOME": str(home_dir),
                },
                capture_output=True,
                check=False,
                text=True,
            )

            self.assertEqual(result.returncode, 4)
            self.assertIn("已安装版本与当前源码不一致", result.stdout)
            self.assertEqual((installed_root / "SKILL.md").read_text(encoding="utf-8"), "old install")


if __name__ == "__main__":
    unittest.main()
