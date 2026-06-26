#!/usr/bin/env python3
"""
对话提取脚本
从小说文件中提取对话内容
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
NOVEL_DIR = BASE_DIR.parent / "novel_data" / "txt"
OUTPUT_DIR = (
    r"d:\projects\wanxiang-scroll\references\chapter-12-book-analysis\dialogues"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

DIALOGUE_PATTERNS = [
    (r'"([^"]+)"', "双引号"),
    (r'"([^"]+)"', "中文双引号"),
    (r"「([^」]+)」", "日文引号"),
    (r"『([^』]+)』", "日文双引号"),
    (r"【([^】]+)】", "方括号"),
    (r"（([^）]+)）", "中文圆括号"),
    (r"\(([^)]+)\)", "英文圆括号"),
    (r"〈([^〉]+)〉", "尖括号"),
    (r"《([^》]+)》", "书名号"),
    (r"\[([^\]]+)\]", "英文方括号"),
]


def extract_dialogues(filepath, max_chars=100000):
    """从文件中提取对话"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(max_chars)
    except:
        return {}

    dialogues = defaultdict(list)
    for pattern, name in DIALOGUE_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            for match in matches:
                text = match.strip()
                if len(text) >= 2 and len(text) <= 500:
                    dialogues[name].append(text)
    return dict(dialogues)


def analyze_dialogue_style(dialogues):
    """分析对话风格"""
    if not dialogues:
        return {}

    style_info = {
        "total_count": 0,
        "by_type": {},
        "avg_length": 0,
        "sample_dialogues": [],
        "common_patterns": [],
    }

    all_dialogues = []
    for dtype, dlist in dialogues.items():
        style_info["by_type"][dtype] = len(dlist)
        style_info["total_count"] += len(dlist)
        all_dialogues.extend(dlist)

    if all_dialogues:
        style_info["avg_length"] = sum(len(d) for d in all_dialogues) // len(
            all_dialogues
        )
        style_info["sample_dialogues"] = all_dialogues[:20]

        short_dialogues = [d for d in all_dialogues if len(d) <= 10]
        question_dialogues = [d for d in all_dialogues if "?" in d or "？" in d]
        exclamation_dialogues = [d for d in all_dialogues if "!" in d or "！" in d]

        style_info["common_patterns"] = {
            "short_count": len(short_dialogues),
            "question_count": len(question_dialogues),
            "exclamation_count": len(exclamation_dialogues),
            "short_samples": short_dialogues[:10],
            "question_samples": question_dialogues[:10],
            "exclamation_samples": exclamation_dialogues[:10],
        }

    return style_info


def clean_novel_name(filename):
    """清理小说文件名"""
    name = filename.replace(".txt", "")
    name = re.sub(r"_\d+$", "", name)
    name = re.sub(r"_Unicode$", "", name)
    name = re.sub(r"_作者.*", "", name)
    name = re.sub(r"⊙.*", "", name)
    name = re.sub(r"_tags_.*", "", name)
    return name.strip()


def main():
    print("开始提取对话信息...")
    files = list(Path(NOVEL_DIR).glob("*.txt"))
    print(f"总文件数: {len(files)}")

    all_dialogues = {}
    all_styles = {}

    for i, filepath in enumerate(files):
        if i % 100 == 0:
            print(f"处理进度: {i}/{len(files)} ({i*100//len(files)}%)")

        try:
            dialogues = extract_dialogues(str(filepath))
            if dialogues:
                name = clean_novel_name(filepath.name)
                all_dialogues[name] = dialogues
                style = analyze_dialogue_style(dialogues)
                all_styles[name] = style
        except Exception as e:
            continue

    print("\n保存对话数据...")
    dialogues_file = os.path.join(OUTPUT_DIR, "all_dialogues.json")
    with open(dialogues_file, "w", encoding="utf-8") as f:
        json.dump(all_dialogues, f, ensure_ascii=False, indent=2)

    styles_file = os.path.join(OUTPUT_DIR, "dialogue_styles.json")
    with open(styles_file, "w", encoding="utf-8") as f:
        json.dump(all_styles, f, ensure_ascii=False, indent=2)

    print("\n生成口语化学习报告...")
    total_dialogues = sum(s["total_count"] for s in all_styles.values())
    avg_length = (
        sum(s["avg_length"] for s in all_styles.values()) // len(all_styles)
        if all_styles
        else 0
    )

    type_stats = defaultdict(int)
    for s in all_styles.values():
        for t, c in s.get("by_type", {}).items():
            type_stats[t] += c

    all_samples = []
    for s in all_styles.values():
        all_samples.extend(s.get("sample_dialogues", []))

    report = f"""# 口语化对话学习报告

> 分析日期：2026-04-18
> 分析小说数：{len(all_styles)}

---

## 一、总体统计

| 统计项 | 数量 |
|--------|------|
| **分析小说数** | {len(all_styles)} |
| **总对话数** | {total_dialogues} |
| **平均对话长度** | {avg_length}字符 |

---

## 二、对话类型统计

| 类型 | 数量 | 占比 |
|------|------|------|
"""

    for t, c in sorted(type_stats.items(), key=lambda x: -x[1]):
        pct = c * 100 // total_dialogues if total_dialogues > 0 else 0
        report += f"| **{t}** | {c} | {pct}% |\n"

    report += f"""
---

## 三、对话样本示例

### 3.1 短对话示例（≤10字符）
"""

    short_samples = []
    for s in all_styles.values():
        if "common_patterns" in s and "short_samples" in s["common_patterns"]:
            short_samples.extend(s["common_patterns"]["short_samples"])

    for i, sample in enumerate(short_samples[:50], 1):
        report += f"{i}. {sample}\n"

    report += f"""
### 3.2 疑问句示例
"""

    question_samples = []
    for s in all_styles.values():
        if "common_patterns" in s and "question_samples" in s["common_patterns"]:
            question_samples.extend(s["common_patterns"]["question_samples"])

    for i, sample in enumerate(question_samples[:50], 1):
        report += f"{i}. {sample}\n"

    report += f"""
### 3.3 感叹句示例
"""

    exclamation_samples = []
    for s in all_styles.values():
        if "common_patterns" in s and "exclamation_samples" in s["common_patterns"]:
            exclamation_samples.extend(s["common_patterns"]["exclamation_samples"])

    for i, sample in enumerate(exclamation_samples[:50], 1):
        report += f"{i}. {sample}\n"

    report += f"""
---

## 四、口语化特点分析

### 4.1 常见口语表达
1. **语气词使用**：呢、啊、吧、嘛、哦、呀
2. **疑问句式**：吗？、呢？、吧？
3. **感叹句式**：！、！！
4. **省略句**：主语省略、谓语省略

### 4.2 对话风格分类
1. **日常对话**：轻松、口语化
2. **正式对话**：书面化、规范
3. **情感对话**：感叹多、语气词多
4. **战斗对话**：短句多、命令式

---

## 五、数据文件

- **完整对话数据**：[all_dialogues.json](./all_dialogues.json)
- **风格分析数据**：[dialogue_styles.json](./dialogue_styles.json)

---

*本报告由对话提取脚本自动生成*
"""

    report_file = os.path.join(OUTPUT_DIR, "dialogue_learning_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n分析完成!")
    print(f"总对话数: {total_dialogues}")
    print(f"结果保存到: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
