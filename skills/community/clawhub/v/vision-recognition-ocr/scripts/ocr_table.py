import json
import sys
from typing import Any, Dict

from _baidu_image_classify import build_image_payload
from _baidu_ocr import call_ocr, to_bool_str


def ocr_table(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = build_image_payload(payload)
    data["cell_contents"] = to_bool_str(payload.get("cell_contents"), default=False)
    data["return_excel"] = to_bool_str(payload.get("return_excel"), default=False)
    return call_ocr("table", data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ocr_table.py '<JSON>'")
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)

    try:
        result = ocr_table(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
