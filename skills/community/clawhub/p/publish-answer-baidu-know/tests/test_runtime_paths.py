# -*- coding: utf-8 -*-
"""util.runtime_paths：技能根、DB 路径、数据目录均落在隔离数据根下。"""
from __future__ import annotations

import os
import unittest

from _support import IsolatedDataRoot, get_skill_root

_FAKE_REAL_ROOT = r"D:\jiangchang-data"


def _legacy_env_key(suffix: str) -> str:
    return "CL" + "AW_" + suffix


class TestRuntimePaths(unittest.TestCase):
    def test_paths_under_isolated_root(self) -> None:
        win_default = r"D:\jiangchang-data"
        with IsolatedDataRoot() as tmp:
            import importlib

            import util.runtime_paths as rp

            importlib.reload(rp)

            skill_root = rp.get_skill_root()
            self.assertTrue(os.path.isdir(skill_root))
            self.assertTrue(os.path.isfile(os.path.join(skill_root, "SKILL.md")))

            db_path = rp.get_db_path()
            self.assertTrue(os.path.normpath(db_path).startswith(os.path.normpath(tmp)))
            self.assertNotIn(win_default, db_path)

            data_dir = rp.get_skill_data_dir()
            self.assertTrue(os.path.normpath(data_dir).startswith(os.path.normpath(tmp)))
            self.assertIn("_test", data_dir.replace("\\", "/"))
            self.assertNotIn(win_default, data_dir)

            self.assertEqual(get_skill_root(), skill_root)

    def test_isolation_overrides_prefixed_real_data_root(self) -> None:
        """先设假数据根，再进入隔离；get_db_path 必须落在 tempdir。"""
        saved = {
            k: os.environ.get(k)
            for k in ("JIANGCHANG_DATA_ROOT", "JIANGCHANG_USER_ID")
        }
        try:
            os.environ["JIANGCHANG_DATA_ROOT"] = _FAKE_REAL_ROOT
            with IsolatedDataRoot() as tmp:
                import importlib

                import util.runtime_paths as rp

                importlib.reload(rp)
                db_path = rp.get_db_path()
                norm_db = os.path.normcase(os.path.normpath(db_path))
                norm_tmp = os.path.normcase(os.path.normpath(tmp))
                self.assertTrue(norm_db.startswith(norm_tmp), msg=f"db_path={db_path!r} tmp={tmp!r}")
                norm_fake = os.path.normcase(os.path.normpath(_FAKE_REAL_ROOT))
                self.assertFalse(
                    norm_db.startswith(norm_fake),
                    msg=f"db_path must not be under fake root: {db_path!r}",
                )
        finally:
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

    def test_legacy_env_vars_do_not_override_canonical(self) -> None:
        with IsolatedDataRoot() as tmp:
            os.environ[_legacy_env_key("DATA_ROOT")] = _FAKE_REAL_ROOT
            os.environ[_legacy_env_key("USER_ID")] = "legacy-user"
            import importlib

            import util.runtime_paths as rp

            importlib.reload(rp)
            data_dir = rp.get_skill_data_dir()
            self.assertTrue(os.path.normpath(data_dir).startswith(os.path.normpath(tmp)))
            self.assertIn("_test", data_dir.replace("\\", "/"))


if __name__ == "__main__":
    unittest.main()
