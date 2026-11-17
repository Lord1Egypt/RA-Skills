from pathlib import Path
import json
import sys

def clamp(value, min_value=0, max_value=10):
    return max(min_value, min(max_value, value))


def calculate_complexity(project_data, stack_data, key_files_data):
    total_files = project_data.get("total_files", 0)
    total_directories = project_data.get("total_directories", 0)

    languages = project_data.get("languages", {})
    technology_stack = stack_data.get("technology_stack", [])
    key_files = key_files_data.get("key_files", [])

    # 1. 项目规模
    size_score = min(total_files / 100, 10)

    # 2. 目录层级/模块数量
    structure_score = min(total_directories / 20, 10)

    # 3. 技术栈广度
    stack_score = min(len(technology_stack) * 1.2, 10)

    # 4. 语言数量
    language_score = min(len(languages) * 2, 10)

    # 5. 关键模块数量
    key_file_score = min(len(key_files), 10)

    final_score = (
        size_score * 0.30
        + structure_score * 0.20
        + stack_score * 0.25
        + language_score * 0.10
        + key_file_score * 0.15
    )

    final_score = round(clamp(final_score), 1)

    if final_score < 3:
        level = "简单"
    elif final_score < 5:
        level = "中等"
    elif final_score < 7:
        level = "偏复杂"
    elif final_score < 9:
        level = "复杂"
    else:
        level = "非常复杂"

    return {
        "score": final_score,
        "level": level,
        "dimensions": {
            "size": round(size_score, 1),
            "structure": round(structure_score, 1),
            "technology_stack": round(stack_score, 1),
            "languages": round(language_score, 1),
            "key_files": round(key_file_score, 1),
        }
    }


def main():
    if len(sys.argv) < 2:
        print("用法：python complexity.py xray-data.json")
        return

    data_path = Path(sys.argv[1])

    data = json.loads(
        data_path.read_text(encoding="utf-8")
    )

    result = calculate_complexity(
        data["project"],
        data["stack"],
        data["key_files"]
    )

    print(json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    ))


if __name__ == "__main__":
    main()