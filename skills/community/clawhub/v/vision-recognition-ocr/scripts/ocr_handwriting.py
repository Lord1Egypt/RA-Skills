import json
import sys
from typing import Any, Dict

from _baidu_image_classify import build_image_payload
from _baidu_ocr import call_ocr, to_bool_str


def ocr_handwriting(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = build_image_payload(payload)
    data["detect_direction"] = to_bool_str(payload.get("detect_direction"), default=False)
    data["probability"] = to_bool_str(payload.get("probability"), default=False)
    data["detect_alteration"] = to_bool_str(payload.get("detect_alteration"), default=False)
    # keep same naming style as your sample code
    data["eng_granularity"] = payload.get("eng_granularity", "word")
    return call_ocr("handwriting", data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ocr_handwriting.py '<JSON>'")
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)

    try:
        result = ocr_handwriting(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
