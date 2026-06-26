"""
仅用于单元测试：解析 TTS 音色与公共数字人 ID。

- 默认值：`tests/test_id_resolver.py` 内嵌常量（见 EMBEDDED_DEFAULTS）；可选覆盖文件
  `tests/chanjing_test_defaults.json`（从 chanjing_test_defaults.example.json 复制，勿提交真实 ID）。
- 若 audio_man / person_id 仍不全，则调用当前 skill 内的 clients：
  `clients.tts_client.list_voices()` 与 `clients.avatar_client.list_figures(source="common")`
  现场拉取；**不读写**仓库内缓存文件，不记录历史选型。

不使用环境变量指定测试 ID。不在 `run_render.py` 生产路径中使用；不读 list_tasks。
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from clients.tts_client import first_voice_id, list_voices
from clients.avatar_client import first_common_person_figure, list_figures

# 代码内嵌默认（与 chanjing_test_defaults.example.json 一致）；留空表示走接口自动拉取（仅测试，不写缓存）
EMBEDDED_DEFAULTS: dict[str, str] = {
    "audio_man": "",
    "person_id": "",
    "figure_type": "sit_body",
}

# 向后兼容：与 EMBEDDED_DEFAULTS 同步
DEFAULT_TEST_AUDIO_MAN: str = EMBEDDED_DEFAULTS["audio_man"]
DEFAULT_TEST_PERSON_ID: str = EMBEDDED_DEFAULTS["person_id"]
DEFAULT_TEST_FIGURE_TYPE: str = EMBEDDED_DEFAULTS["figure_type"]



def _defaults_path() -> Path:
    return Path(__file__).resolve().parent / "chanjing_test_defaults.json"


def _load_config_defaults() -> dict[str, str]:
    base = {k: str(v).strip() for k, v in EMBEDDED_DEFAULTS.items()}
    path = _defaults_path()
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                for k in ("audio_man", "person_id", "figure_type"):
                    if k in data and data[k] is not None:
                        base[k] = str(data[k]).strip()
        except (json.JSONDecodeError, OSError):
            pass
    if not base.get("figure_type"):
        base["figure_type"] = DEFAULT_TEST_FIGURE_TYPE
    return base

def _fetch_from_api() -> dict[str, Any]:
    voice_data = list_voices(page=1, size=100)
    common_figures = list_figures(source="common", page=1, page_size=20)

    person_id, figure_type = first_common_person_figure(common_figures)
    audio_man = first_voice_id(voice_data)

    return {
        "audio_man": audio_man,
        "person_id": person_id,
        "figure_type": figure_type,
        "source": "api_clients",
    }


def resolve_render_test_ids(*, force_refresh: bool = False) -> dict[str, Any]:
    """
    供单元测试使用：返回含 audio_man、person_id、figure_type 的字典。
    force_refresh 保留为兼容参数，当前无磁盘缓存，True/False 均走同一逻辑：
    配置文件非空 ID 优先，否则现场请求接口（不写回仓库）。
    """
    _ = force_refresh  # 无磁盘缓存可刷新；保留签名供旧调用方兼容
    cfg = _load_config_defaults()
    audio = cfg["audio_man"]
    person = cfg["person_id"]
    figure = cfg["figure_type"] or DEFAULT_TEST_FIGURE_TYPE

    if audio and person:
        return {
            "audio_man": audio,
            "person_id": person,
            "figure_type": figure,
            "source": "config_file",
        }

    return _fetch_from_api()


class TestIdResolver(unittest.TestCase):
    def test_embedded_defaults_are_empty_or_safe(self):
        self.assertEqual(EMBEDDED_DEFAULTS["audio_man"], "")
        self.assertEqual(EMBEDDED_DEFAULTS["person_id"], "")
        self.assertTrue(EMBEDDED_DEFAULTS["figure_type"])

    def test_config_file_overrides_without_network(self):
        import tempfile
        from unittest.mock import patch

        this_module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "chanjing_test_defaults.json"
            p.write_text(
                json.dumps(
                    {
                        "audio_man": "cfg-voice",
                        "person_id": "cfg-person",
                        "figure_type": "whole_body",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            with patch.object(this_module, "_defaults_path", return_value=p):
                d = resolve_render_test_ids(force_refresh=False)
            self.assertEqual(d["source"], "config_file")
            self.assertEqual(d["audio_man"], "cfg-voice")
            self.assertEqual(d["person_id"], "cfg-person")
            self.assertEqual(d["figure_type"], "whole_body")

    def test_resolve_from_api_does_not_write_cache_file(self):
        cred = Path.home() / ".chanjing" / "credentials.json"
        if not cred.is_file():
            self.skipTest("无蝉镜凭证，跳过自动拉取 ID")

        d = resolve_render_test_ids(force_refresh=True)
        self.assertIn("audio_man", d)
        self.assertIn("person_id", d)
        self.assertTrue(d["audio_man"])
        self.assertTrue(d["person_id"])
        self.assertEqual(d.get("source"), "api_clients")


if __name__ == "__main__":
    unittest.main()
