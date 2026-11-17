import sys
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
import runtime_bootstrap


class RuntimeBootstrapTests(unittest.TestCase):
    def test_preferred_venv_interpreter_path_is_not_collapsed_to_base_python(self):
        with tempfile.TemporaryDirectory() as tmp:
            base_python = Path(tmp) / "base-python"
            base_python.touch()
            venv_python = Path(tmp) / "venv" / "bin" / "python"
            venv_python.parent.mkdir(parents=True)
            venv_python.symlink_to(base_python)

            with patch.dict(os.environ, {runtime_bootstrap.ENV_PREFERRED: str(venv_python)}):
                candidates = runtime_bootstrap._build_candidates()

            self.assertEqual(candidates[0], str(venv_python))

    def test_venv_symlink_is_executed_when_it_has_required_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            base_python = Path(tmp) / "base-python"
            base_python.touch()
            venv_python = Path(tmp) / "venv" / "bin" / "python"
            venv_python.parent.mkdir(parents=True)
            venv_python.symlink_to(base_python)

            with (
                patch.object(runtime_bootstrap.sys, "executable", str(base_python)),
                patch.object(runtime_bootstrap, "_build_candidates", return_value=[str(venv_python)]),
                patch.object(runtime_bootstrap, "_has_modules", side_effect=lambda executable, modules: executable == str(venv_python)),
                patch.object(runtime_bootstrap.os, "execve", side_effect=SystemExit("exec-called")),
                self.assertRaisesRegex(SystemExit, "exec-called"),
            ):
                runtime_bootstrap.ensure_runtime(["ddddocr"])


if __name__ == "__main__":
    unittest.main()
