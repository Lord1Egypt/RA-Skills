#!/usr/bin/env python3
"""
TCM Wellness Skill - 记忆系统初始化脚本
自动创建记忆目录结构、模板文件和配置文件。

用法：
    python init_memory.py [--user <匿名ID>] [--force]

参数：
    --user  指定用户匿名ID，为其创建完整档案模板
    --force 强制重建整个记忆目录（警告：会清除已有数据）
"""

import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path


def get_memory_root():
    """获取记忆根目录路径"""
    return Path(__file__).parent.parent / "memory"


def create_directory_structure(root: Path, force: bool = False):
    """创建记忆目录结构"""
    dirs = [
        root / "blocks",
        root / "long_term",
        root / "reflections",
        root / "evolution",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ 目录: {d.relative_to(root.parent.parent)}")


def create_config(root: Path, force: bool = False):
    """创建记忆系统配置文件"""
    config_path = root / "config.json"
    if config_path.exists() and not force:
        print("  ⏭️  配置文件已存在，跳过")
        return

    config = {
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "memory_root": str(root),
        "max_blocks_per_user": 100,
        "max_index_entries": 500,
        "max_reflections": 20,
        "retention": {
            "high_blocks_days": 180,
            "medium_blocks_days": 90,
            "low_blocks_days": 30,
            "high_index_days": -1,
            "medium_index_days": 365,
            "low_index_days": 180,
        },
        "reflection": {
            "auto_trigger_blocks": 10,
            "interval_days": 30,
            "session_end_threshold": 3,
        },
        "evolution": {
            "pattern_min_occurrences": 5,
            "feedback_tracking": True,
        },
    }

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 配置文件: config.json")


def create_reflection_meta(root: Path, force: bool = False):
    """创建反思元数据文件"""
    meta_path = root / "reflections" / "meta.md"
    if meta_path.exists() and not force:
        print("  ⏭️  反思元数据已存在，跳过")
        return

    meta = {
        "last_reflection": None,
        "total_reflections": 0,
        "auto_trigger_threshold": 10,
        "reflection_interval_days": 30,
        "users_reflected": [],
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 反思元数据: reflections/meta.md")


def create_evolution_templates(root: Path, force: bool = False):
    """创建进化日志模板"""
    templates = {
        "evolution/pattern_discoveries.md": "# 模式发现记录\n\n<!-- 格式: ## YYYY-MM-DD\n- **用户**: <匿名ID>\n- **模式**: <描述>\n- **应对**: <调整策略> -->\n\n",
        "evolution/knowledge_updates.md": "# 知识修正记录\n\n<!-- 格式: ## YYYY-MM-DD\n- **问题**: <描述>\n- **修正**: <修正内容>\n- **影响范围**: <受影响的参考文档> -->\n\n",
        "evolution/prescription_effectiveness.md": "# 方剂反馈追踪\n\n<!-- 格式: ## YYYY-MM-DD\n- **方剂**: <方名>\n- **用户**: <匿名ID>\n- **证型**: <证型>\n- **反馈**: <有效/无效/部分有效>\n- **备注**: <补充说明> -->\n\n",
    }

    for rel_path, content in templates.items():
        full_path = root / rel_path
        if full_path.exists() and not force:
            print(f"  ⏭️  {rel_path} 已存在，跳过")
            continue
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ 进化日志: {rel_path}")


def create_user_profile(root: Path, user_id: str):
    """为指定用户创建健康档案模板"""
    user_dir = root / "blocks" / user_id
    user_dir.mkdir(parents=True, exist_ok=True)

    templates = {
        "profile": f"""# 健康档案：{user_id}

## 基本信息
- 首次记录：{datetime.now().strftime("%Y-%m-%d")}
- 性别：<未提供>
- 年龄段：<未提供>
- 生活特征：<待采集>

## 体质辨识
- **当前体质**：<待辨证>
- **体质演变**：
  <!-- 格式: - YYYY-MM-DD：旧体质 → 新体质（原因） -->
- **体质倾向**：<待判断>

## 病史脉络
<!-- 按脏腑系统分类记录 -->

### 脾胃系统
- （暂无记录）

### 肝胆系统
- （暂无记录）

### 心肺系统
- （暂无记录）

### 肾与膀胱系统
- （暂无记录）

## 持续问题追踪
| 问题 | 首次出现 | 最近一次 | 状态 | 趋势 |
|------|---------|---------|------|------|
| （暂无） | - | - | - | - |

## 敏感信息
- 过敏史：<无/待补充>
- 用药情况：<无/待补充>
- 已知疾病：<无/待补充>

## 调理偏好
- 愿意尝试：<待了解>
- 不愿尝试：<无>
- 方案依从性：<待评估>
""",
        "constitution": f"""# 体质演变追踪：{user_id}

## 体质判定记录
| 日期 | 体质判断 | 判断依据 | 辨证次数 | 置信度 |
|------|---------|---------|---------|--------|
| {datetime.now().strftime("%Y-%m-%d")} | <待定> | <待记录> | 1 | 初步 |

## 体质因子分析
| 因子 | 当前状态 | 趋势 |
|------|---------|------|
| 气虚 | <未评估> | - |
| 阳虚 | <未评估> | - |
| 阴虚 | <未评估> | - |
| 痰湿 | <未评估> | - |
| 湿热 | <未评估> | - |
| 血瘀 | <未评估> | - |
| 气郁 | <未评估> | - |

## 体质演变图
<!-- 用文字描述体质变化的轨迹 -->
""",
        "index": f"""# 长记忆索引：{user_id}

## 索引统计
- 总记忆块数：0
- high优先级：0 | medium：0 | low：0
- 首次记录：{datetime.now().strftime("%Y-%m-%d")}
- 最近更新：{datetime.now().strftime("%Y-%m-%d")}

## 按时间索引
| 日期 | 证型 | 主诉 | 关键词 | 优先级 | 文件名 |
|------|------|------|--------|--------|--------|
| （暂无） | - | - | - | - | - |

## 按证型索引
<!-- 按证型分类的记忆块摘要 -->

## 按系统索引
<!-- 按脏腑系统分类的记忆块摘要 -->
- 脾胃系统：（暂无）
- 肝胆系统：（暂无）
- 心肺系统：（暂无）
- 肾与膀胱系统：（暂无）

## 待反馈追踪
| 记忆块日期 | 主诉 | 反馈状态 |
|-----------|------|---------|
| （暂无） | - | - |
""",
    }

    for name, content in templates.items():
        if name == "profile":
            path = root / "long_term" / f"{user_id}_profile.md"
        elif name == "constitution":
            path = root / "long_term" / f"{user_id}_constitution.md"
        else:
            path = root / "long_term" / f"{user_id}_index.md"

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ 用户档案: {path.relative_to(root.parent.parent)}")

    print(f"\n  👤 用户 '{user_id}' 档案创建完成")


def main():
    args = sys.argv[1:]
    user_id = None
    force = False

    i = 0
    while i < len(args):
        if args[i] == "--user" and i + 1 < len(args):
            user_id = args[i + 1]
            i += 2
        elif args[i] == "--force":
            force = True
            i += 1
        else:
            i += 1

    root = get_memory_root()

    print(f"🏥 TCM 记忆系统初始化")
    print(f"   根目录: {root}")
    print()

    if force and root.exists():
        print("  ⚠️  --force 模式：将清除已有数据并重建")
        print()

    create_directory_structure(root, force)
    create_config(root, force)
    create_reflection_meta(root, force)
    create_evolution_templates(root, force)

    if user_id:
        create_user_profile(root, user_id)
    else:
        print("\n  💡 提示：使用 --user <匿名ID> 为特定用户创建档案")
        print("     例: python init_memory.py --user 张先生")

    # 证型简码速查
    print("\n📋 记忆系统就绪。可用命令：")
    print("   初始化: python init_memory.py [--user <ID>] [--force]")
    print("   睡眠反思: python sleep_reflection.py --user <ID>")
    print("   记忆归档: python sleep_reflection.py --user <ID> --archive-only")


if __name__ == "__main__":
    main()
