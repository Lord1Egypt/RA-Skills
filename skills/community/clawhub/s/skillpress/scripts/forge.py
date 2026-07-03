#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw SkillForge - 技能锻造炉
从分析中自动生成标准 SKILL.md + 脚本骨架
原创实现，设计受 Claude Code Skillify 启发
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
import json
from pathlib import Path
from datetime import datetime


SKILL_TEMPLATE = """---
name: {name}
description: "{description}"
metadata:
  openclaw:
    emoji: "{emoji}"
    requires:
      bins: [{bins}]
---

# {emoji} {display_name}

## 功能

{description}

## 使用方式

### 基本用法
```
{sample_usage}
```

## 步骤

{steps_yaml}

## 参数说明

{params_table}

## 注意事项

- 待补充
"""


def create_skill(slug, display_name, description, emoji, steps, bins="python3"):
    """创建技能骨架"""
    skills_dir = Path(os.environ.get('OPENCLAW_WORKDIR', '.')) / 'skills'
    skill_dir = skills_dir / slug

    if skill_dir.exists():
        print(f"⚠️  技能已存在: {skill_dir}")
        cont = input("覆盖? (y/N): ")
        if cont.lower() != 'y':
            print("取消")
            return

    # 创建目录
    (skill_dir / 'scripts').mkdir(parents=True, exist_ok=True)

    # 格式化步骤
    steps_yaml = ""
    for i, step in enumerate(steps, 1):
        steps_yaml += f"{i}. **{step.strip()}** \n"

    # 格式化参数表
    params_table = "| 参数 | 说明 |\n|------|------|\n| `<input>` | 输入内容 |\n| `<output>` | 输出目标 |\n"

    sample_usage = f"# 根据 {slug} 技能的具体功能填写使用示例"

    # 写入 SKILL.md
    content = SKILL_TEMPLATE.format(
        name=slug,
        display_name=display_name,
        description=description,
        emoji=emoji,
        bins=bins,
        sample_usage=sample_usage,
        steps_yaml=steps_yaml,
        params_table=params_table,
    )

    (skill_dir / 'SKILL.md').write_text(content, encoding='utf-8')

    # 创建空脚本
    scripts_dir = skill_dir / 'scripts'
    init_file = scripts_dir / '__init__.py'
    if not init_file.exists():
        init_file.write_text('', encoding='utf-8')

    print(f"\n✅ 技能创建成功!")
    print(f"   📁 {skill_dir}")
    print(f"   📄 {skill_dir / 'SKILL.md'}")
    print(f"   📁 {scripts_dir}/")
    print()
    print("下一步: 编辑 SKILL.md 完善技能描述和使用说明")


def show_info(slug):
    """显示技能信息"""
    skills_dir = Path(os.environ.get('OPENCLAW_WORKDIR', '.')) / 'skills'
    skill_dir = skills_dir / slug

    if not skill_dir.exists():
        print(f"❌ 技能不存在: {slug}")
        print(f"   路径: {skill_dir}")
        return

    skill_file = skill_dir / 'SKILL.md'
    if not skill_file.exists():
        print(f"⚠️  技能目录存在但缺少 SKILL.md")
        return

    content = skill_file.read_text(encoding='utf-8')
    print(f"\n📋 技能信息: {slug}")
    print(f"{'='*50}")
    print(content[:500] + ("..." if len(content) > 500 else ""))


def main():
    if len(sys.argv) < 2:
        print("用法: python forge.py <create|info> [args...]")
        print("\n示例:")
        print("  python forge.py create my-skill --name \"我的技能\" --emoji 🔧 --desc \"做什么的\" --steps \"步骤1,步骤2\"")
        print("  python forge.py info my-skill")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'create':
        if len(sys.argv) < 3:
            print("❌ 需要指定 slug: python forge.py create <slug> [选项]")
            sys.exit(1)

        slug = sys.argv[2]
        kwargs = {}
        for i in range(3, len(sys.argv)):
            if sys.argv[i] in ('--name', '--desc', '--emoji', '--steps', '--bins'):
                if i + 1 < len(sys.argv):
                    kwargs[sys.argv[i][2:]] = sys.argv[i + 1]

        display_name = kwargs.get('name', slug.replace('-', ' ').title())
        description = kwargs.get('desc', f'slug 技能的描述')
        emoji = kwargs.get('emoji', '🔧')
        steps = kwargs.get('steps', '步骤1,步骤2,步骤3').split(',')
        bins = kwargs.get('bins', 'python3')

        create_skill(slug, display_name, description, emoji, steps, bins)

    elif command == 'info':
        if len(sys.argv) < 3:
            print("❌ 需要指定 slug: python forge.py info <slug>")
            sys.exit(1)
        show_info(sys.argv[2])

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
