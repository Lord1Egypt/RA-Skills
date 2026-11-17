from pathlib import Path
import json
import sys

from scan_repo import scan_repository
from detect_stack import detect_stack


def run_xray(root: Path):
    repo_data = scan_repository(root)
    stack_data = detect_stack(root)

    result = {
        "project": repo_data,
        "stack": stack_data,
    }

    return result


def main():
    target = Path(
        sys.argv[1] if len(sys.argv) > 1 else "."
    ).resolve()

    result = run_xray(target)

    output_path = Path("xray-data.json")

    output_path.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(f"X-ray 扫描完成")
    print(f"目标项目：{target}")
    print(f"数据文件：{output_path.resolve()}")


if __name__ == "__main__":
    main()