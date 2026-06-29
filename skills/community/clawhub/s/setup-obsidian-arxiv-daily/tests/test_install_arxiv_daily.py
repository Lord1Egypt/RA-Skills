import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = SKILL_ROOT / "scripts" / "install_arxiv_daily.py"


def load_installer():
    if not INSTALLER_PATH.exists():
        raise AssertionError(f"Installer is missing: {INSTALLER_PATH}")
    spec = importlib.util.spec_from_file_location(
        "install_arxiv_daily",
        INSTALLER_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InstallArxivDailyTests(unittest.TestCase):
    def setUp(self):
        self.installer = load_installer()

    def test_dry_run_lists_files_without_creating_project(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory) / "Vault"
            vault.mkdir()

            result = self.installer.install(
                vault=vault,
                project_name="arxiv-daily",
                dry_run=True,
                force=False,
            )

            self.assertFalse((vault / "arxiv-daily").exists())
            relative_paths = {path.as_posix() for path in result.files}
            self.assertIn("config.yaml", relative_paths)
            self.assertIn("scripts/arxiv_daily.py", relative_paths)
            self.assertIn("templates/paper.md", relative_paths)

    def test_packaged_files_exclude_caches_and_runtime_content(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)

            result = self.installer.install(
                vault,
                "arxiv-daily",
                dry_run=True,
                force=False,
            )

            for path in result.files:
                self.assertNotIn("__pycache__", path.parts)
                self.assertNotEqual(path.suffix.lower(), ".pyc")
                self.assertNotIn(path.parts[0], {"papers", "daily", "archive", "logs"})

    def test_clean_install_copies_assets_and_creates_empty_runtime_directories(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory) / "Vault"
            vault.mkdir()

            result = self.installer.install(
                vault=vault,
                project_name="research-feed",
                dry_run=False,
                force=False,
            )

            destination = vault / "research-feed"
            self.assertEqual(result.destination, destination.resolve())
            self.assertTrue((destination / "config.yaml").is_file())
            self.assertTrue((destination / "dashboard.md").is_file())
            self.assertTrue(
                (destination / "scripts" / "arxiv_daily.py").is_file()
            )
            for runtime_directory in ("papers", "daily", "archive", "logs"):
                self.assertTrue((destination / runtime_directory).is_dir())

    def test_custom_project_name_rewrites_dashboard_paths_and_commands(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory) / "Vault"
            vault.mkdir()

            self.installer.install(vault, "research-feed", False, False)

            dashboard = (vault / "research-feed" / "dashboard.md").read_text(
                encoding="utf-8"
            )
            self.assertIn('FROM "research-feed/papers"', dashboard)
            self.assertIn(r".\research-feed\scripts\arxiv_daily.ps1", dashboard)
            self.assertNotIn(r".\arxiv-daily\scripts\arxiv_daily.ps1", dashboard)

    def test_existing_project_is_rejected_without_force(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory) / "Vault"
            destination = vault / "arxiv-daily"
            destination.mkdir(parents=True)

            with self.assertRaises(FileExistsError):
                self.installer.install(
                    vault=vault,
                    project_name="arxiv-daily",
                    dry_run=False,
                    force=False,
                )

    def test_force_updates_assets_and_preserves_generated_content(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory) / "Vault"
            vault.mkdir()
            self.installer.install(vault, "arxiv-daily", False, False)
            destination = vault / "arxiv-daily"
            sentinel = destination / "papers" / "keep.md"
            sentinel.write_text("keep", encoding="utf-8")
            config = destination / "config.yaml"
            config.write_text("stale", encoding="utf-8")

            self.installer.install(vault, "arxiv-daily", False, True)

            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
            self.assertNotEqual(config.read_text(encoding="utf-8"), "stale")

    def test_invalid_project_names_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            for project_name in ("", ".", "..", "a/b", r"a\b", " C: "):
                with self.subTest(project_name=project_name):
                    with self.assertRaises(ValueError):
                        self.installer.install(
                            vault,
                            project_name,
                            dry_run=True,
                            force=False,
                        )

    def test_missing_vault_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing_vault = Path(temporary_directory) / "missing"

            with self.assertRaises(FileNotFoundError):
                self.installer.install(
                    missing_vault,
                    "arxiv-daily",
                    dry_run=True,
                    force=False,
                )

    def test_symlinked_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault = root / "Vault"
            outside = root / "outside"
            vault.mkdir()
            outside.mkdir()
            destination = vault / "arxiv-daily"
            try:
                destination.symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Directory symlinks are unavailable")

            with self.assertRaises(ValueError):
                self.installer.install(
                    vault,
                    "arxiv-daily",
                    dry_run=False,
                    force=True,
                )

    def test_redirected_destination_component_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault = root / "Vault"
            destination = vault / "arxiv-daily"
            outside_scripts = root / "outside-scripts"
            destination.mkdir(parents=True)
            outside_scripts.mkdir()
            scripts_path = destination / "scripts"
            if os.name == "nt":
                result = subprocess.run(
                    [
                        "cmd",
                        "/c",
                        "mklink",
                        "/J",
                        str(scripts_path),
                        str(outside_scripts),
                    ],
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    self.skipTest("Directory junctions are unavailable")
            else:
                scripts_path.symlink_to(outside_scripts, target_is_directory=True)

            try:
                with self.assertRaises(ValueError):
                    self.installer.install(
                        vault,
                        "arxiv-daily",
                        dry_run=False,
                        force=True,
                    )
            finally:
                if scripts_path.is_symlink():
                    scripts_path.unlink(missing_ok=True)
                elif scripts_path.exists():
                    os.rmdir(scripts_path)


if __name__ == "__main__":
    unittest.main()
