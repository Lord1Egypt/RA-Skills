import json

from uexx_client import request_json


def main() -> None:
    guide = request_json("/api/v1/public/api-guide")
    catalog = guide.get("data_catalog", [])
    summary = guide.get("catalog_summary", {})
    print(json.dumps({"summary": summary, "data_catalog": catalog}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
