# -*- coding: utf-8 -*-
"""adapter profile / 环境开关策略：默认不触碰真实 API 与真实 RPA。"""
from __future__ import annotations

import os
import unittest

from jiangchang_skill_core import config

from adapter_test_utils import (
    ALLOWED_TEST_TARGETS,
    FakeAdapter,
    assert_no_real_network_env,
    get_test_target,
    should_skip_profile,
)


def _save_env(keys: tuple[str, ...]) -> dict[str, str | None]:
    return {k: os.environ.get(k) for k in keys}


def _restore_env(saved: dict[str, str | None]) -> None:
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    config.reset_cache()


_ENV_KEYS = ("OPENCLAW_TEST_TARGET",)


class TestAdapterProfilePolicy(unittest.TestCase):
    def tearDown(self) -> None:
        config.reset_cache()

    def test_get_test_target_defaults_to_unit(self) -> None:
        saved = _save_env(_ENV_KEYS)
        try:
            for k in _ENV_KEYS:
                os.environ.pop(k, None)
            config.reset_cache()
            self.assertEqual(get_test_target(), "unit")
        finally:
            _restore_env(saved)

    def test_get_test_target_invalid_raises(self) -> None:
        saved = _save_env(_ENV_KEYS)
        try:
            for k in _ENV_KEYS:
                os.environ.pop(k, None)
            os.environ["OPENCLAW_TEST_TARGET"] = "not_a_valid_target"
            config.reset_cache()
            with self.assertRaises(ValueError):
                get_test_target()
        finally:
            _restore_env(saved)

    def test_allowed_targets_contains_expected(self) -> None:
        self.assertTrue({"unit", "mock", "simulator_api", "real_api"}.issubset(ALLOWED_TEST_TARGETS))

    def test_simulator_api_runs_when_target_matches(self) -> None:
        saved = _save_env(_ENV_KEYS)
        try:
            os.environ["OPENCLAW_TEST_TARGET"] = "simulator_api"
            config.reset_cache()
            skip, _ = should_skip_profile("simulator_api")
            self.assertFalse(skip)
        finally:
            _restore_env(saved)

    def test_unit_target_skips_simulator_and_real_profiles(self) -> None:
        saved = _save_env(_ENV_KEYS)
        try:
            for k in _ENV_KEYS:
                os.environ.pop(k, None)
            config.reset_cache()
            self.assertEqual(get_test_target(), "unit")
            for prof in ("simulator_api", "simulator_rpa", "real_api", "real_rpa"):
                skip, reason = should_skip_profile(prof)
                self.assertTrue(skip, msg=f"{prof}: {reason}")
            skip_mock, _ = should_skip_profile("mock")
            self.assertFalse(skip_mock)
        finally:
            _restore_env(saved)

    def test_real_api_runs_when_target_matches(self) -> None:
        saved = _save_env(_ENV_KEYS)
        try:
            os.environ["OPENCLAW_TEST_TARGET"] = "real_api"
            config.reset_cache()
            skip, _ = should_skip_profile("real_api", write=True)
            self.assertFalse(skip)
        finally:
            _restore_env(saved)

    def test_real_rpa_runs_when_target_matches(self) -> None:
        saved = _save_env(_ENV_KEYS)
        try:
            os.environ["OPENCLAW_TEST_TARGET"] = "real_rpa"
            config.reset_cache()
            skip, _ = should_skip_profile("real_rpa", write=True)
            self.assertFalse(skip)
        finally:
            _restore_env(saved)

    def test_fake_adapter_modes(self) -> None:
        self.assertEqual(FakeAdapter("success").call({"a": 1})["success"], True)
        with self.assertRaises(TimeoutError):
            FakeAdapter("timeout").call({})
        bad = FakeAdapter("invalid_response").call({})
        self.assertNotIsInstance(bad, dict)
        with self.assertRaises(PermissionError):
            FakeAdapter("unauthorized").call({})

    def test_assert_no_real_network_env(self) -> None:
        saved = _save_env(_ENV_KEYS)
        try:
            os.environ.pop("OPENCLAW_TEST_TARGET", None)
            config.reset_cache()
            assert_no_real_network_env()
        finally:
            _restore_env(saved)


if __name__ == "__main__":
    unittest.main()
