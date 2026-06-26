#!/usr/bin/env python3
"""
hair-cam-anno: dataset.jsonl 生成工具

将视频标注结果汇总为符合 VL 模型微调要求的 dataset.jsonl 格式。
"""

import argparse
import json
import os
import sys
from pathlib import Path


SYSTEM_PROMPT = """你是一个安防摄像头视频内容解析专家。你的任务是分析安防摄像头拍摄的视频，输出结构化的场景描述。

## 分析步骤

1. 观察视频中的环境（室内/户外，具体位置）
2. 识别出现的人物（数量、性别、年龄段：婴儿/儿童/老人/成人）
3. 识别出现的动物（猫、狗等）
4. 分析人物/动物的行为动作和姿态
5. 评估是否存在安全风险
6. 生成简练的一句话描述

## 输出格式

你必须输出一个严格的JSON对象，包含以下字段：

```json
{
  "title": "场景标题",
  "subtitle": "场景副标题（具体行为描述）",
  "description": "详细描述（包含环境、人物外貌特征、行为动作及姿态，至少50字）",
  "labels": ["从下方标签列表中选择匹配的标签"],
  "risk": {
    "level": "none/low/medium/high",
    "description": "风险描述，如无风险则为'当前场景无异常风险'"
  },
  "simple_description": "简练描述（不超过20个汉字）"
}
```

## labels 字段可选标签范围

从以下标签中选择所有匹配项：

- `system_suggest_0`: No match.（无匹配场景）
- `system_suggest_1`: Someone appears.（有人出现）
- `system_suggest_2`: Multiple people appear.（多人出现）
- `system_suggest_3`: Child or infant appears.（儿童或婴儿出现）
- `system_suggest_4`: Elderly person appears.（老人出现）
- `system_suggest_5`: Animal appears.（动物出现）
- `system_suggest_6`: Suspicious behavior detected.（可疑行为）
- `system_suggest_7`: Person lying down.（有人躺卧）
- `system_suggest_8`: Person running.（有人在跑）
- `system_suggest_9`: Person climbing.（有人在攀爬）
- `system_suggest_10`: Fall detected.（检测到摔倒）
- `system_suggest_11`: Delivery person detected.（检测到快递员/外卖员）
- `system_suggest_12`: Family interaction.（家人互动）
- `system_suggest_13`: Household chore.（做家务）
- `system_suggest_14`: Package/parcel detected.（检测到快递包裹）

## 约束条件

- 所有字段均不能为空
- `simple_description` 不超过20个汉字
- `labels` 必须从上述标签列表中选择
- `risk.level` 必须是 none/low/medium/high 之一
- `description` 要尽量详细，包含家庭中环境、人、宠外貌特征、行为及姿态
- 着重婴儿儿童看护、老人关照、成人日常行为"""


# Valid labels set
VALID_LABELS = {
    "system_suggest_0", "system_suggest_1", "system_suggest_2",
    "system_suggest_3", "system_suggest_4", "system_suggest_5",
    "system_suggest_6", "system_suggest_7", "system_suggest_8",
    "system_suggest_9", "system_suggest_10", "system_suggest_11",
    "system_suggest_12", "system_suggest_13", "system_suggest_14",
}

VALID_RISK_LEVELS = {"none", "low", "medium", "high"}


def validate_annotation(annotation: dict) -> list[str]:
    """验证单条标注数据，返回错误列表。"""
    errors = []
    
    # Check required fields
    required = ["title", "subtitle", "description", "labels", "risk", "simple_description"]
    for field in required:
        if field not in annotation:
            errors.append(f"缺少字段: {field}")
        elif not annotation[field]:
            errors.append(f"字段为空: {field}")
    
    # Validate labels
    if "labels" in annotation:
        if not isinstance(annotation["labels"], list):
            errors.append("labels 必须是数组")
        else:
            for label in annotation["labels"]:
                if label not in VALID_LABELS:
                    errors.append(f"无效标签: {label}")
    
    # Validate risk
    if "risk" in annotation and isinstance(annotation["risk"], dict):
        level = annotation["risk"].get("level", "")
        if level not in VALID_RISK_LEVELS:
            errors.append(f"无效风险等级: {level}")
        if "description" not in annotation["risk"] or not annotation["risk"]["description"]:
            errors.append("risk.description 不能为空")
    
    # Validate simple_description length
    if "simple_description" in annotation and len(annotation["simple_description"]) > 20:
        errors.append(f"simple_description 超过20字: {len(annotation['simple_description'])}字")
    
    # Validate description length
    if "description" in annotation and len(annotation["description"]) < 50:
        errors.append(f"description 不足50字: {len(annotation['description'])}字")
    
    return errors


def build_jsonl_entry(video_rel_path: str, annotation: dict) -> dict:
    """构建一条 dataset.jsonl 记录。"""
    assistant_content = json.dumps(annotation, ensure_ascii=False, indent=2)
    return {
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "assistant",
                "content": assistant_content
            }
        ],
        "images": [video_rel_path]
    }


def main():
    parser = argparse.ArgumentParser(description="dataset.jsonl 生成工具")
    parser.add_argument("--annotations", required=True, help="标注结果JSON文件（annotations.json）")
    parser.add_argument("--video-dir", required=True, help="视频目录（用于计算相对路径）")
    parser.add_argument("--output", required=True, help="输出 dataset.jsonl 路径")
    parser.add_argument("--validate", action="store_true", default=True, help="验证标注数据（默认开启）")
    args = parser.parse_args()
    
    with open(args.annotations, "r", encoding="utf-8") as f:
        annotations = json.load(f)
    
    records = []
    total = len(annotations)
    errors_all = 0
    
    for i, item in enumerate(annotations):
        video_name = item["video"]
        annotation = item["annotation"]
        
        # Compute relative path
        video_rel_path = os.path.join("data", video_name)
        
        # Validate
        if args.validate:
            errs = validate_annotation(annotation)
            if errs:
                errors_all += 1
                print(f"  ⚠ {video_name}: {errs}")
                # Still include but note issues
        
        entry = build_jsonl_entry(video_rel_path, annotation)
        records.append(entry)
    
    # Write JSONL
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"\n生成完成: {args.output}")
    print(f"  总计: {total} 条")
    if errors_all:
        print(f"  ⚠ 有 {errors_all} 条存在验证问题")
    else:
        print(f"  ✅ 全部通过验证")


if __name__ == "__main__":
    main()
