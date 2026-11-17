import json
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from metrics_input import build_metrics_payload, load_metrics_json_arg


def test_build_metrics_payload_structured():
    payload = build_metrics_payload(
        metrics_text="备注",
        metrics_data={
            "summary": {"roas": "1.4"},
            "campaigns": [{"name": "Test"}],
        },
    )
    assert payload["metrics_data"]["summary"]["roas"] == "1.4"
    # metrics 仅保留用户原始文本，结构化展开由服务端单层合并（避免重复）
    assert payload["metrics"] == "备注"
    assert "roas: 1.4" not in payload["metrics"]


def test_load_metrics_json_arg_invalid():
    with pytest.raises(json.JSONDecodeError):
        load_metrics_json_arg("not-json")
