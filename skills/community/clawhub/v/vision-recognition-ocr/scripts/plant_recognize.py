import json
import sys
from typing import Any, Dict

from _baidu_image_classify import build_image_payload, call_image_classify, clamp_int


def plant_recognize(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = build_image_payload(payload)
    data["top_num"] = clamp_int(payload.get("top_num"), 6, 1, 20)
    data["baike_num"] = clamp_int(payload.get("baike_num"), 0, 0, 1)
    return call_image_classify("plant", data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 plant_recognize.py '<JSON>'")
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)

    try:
        result = plant_recognize(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
