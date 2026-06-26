#!/usr/bin/env python3
"""
init_skill.py — 技能目录初始化脚本（四层骨架版）

用法: python3 init_skill.py <skill-name> [--path <path>]

默认路径: /sandbox/workspace/skills/

纯 Python 3.12 标准库实现，无第三方依赖。
"""

import sys
import re
from pathlib import Path

DEFAULT_PATH = "/sandbox/workspace/skills"

SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: 第一句说这个Skill做什么。Use when user asks to 触发短语1、触发短语2、触发短语3. 不适用于 XXX.]
# 好：将网页内容转为结构化 Markdown。Use when user asks to 抓取网页文章、URL转Markdown、保存网页. 不适用于本地文件转换、PDF处理.
# 差：一个格式转换工具。
---

# {skill_title}

## 概述

[TODO: 一句话说清能力边界]
# 好：对 WeSpy 抓取能力的封装，聚焦"给一个 URL，得到一个 Markdown 文件"的单一链路。
# 差：一个好用的工具。

### 功能范围

- [TODO: 能力1]
- [TODO: 能力2]
- [TODO: 能力3]
# 每条只列"能做什么"，不写"怎么做"。如：单篇文章抓取（微信公众号 / 通用网页），不要写：使用 python3 cli.py URL 抓取文章。

## 使用

[TODO: 按场景给完整示例，不要按参数给说明]
# 好：每个场景 = 意图说明 + 完整可执行命令。如：
#   ### 单篇微信文章抓取
#   用户给了微信文章链接，想保存为 Markdown。
#   python3 scripts/cli.py "https://mp.weixin.qq.com/s/xxxxx"
# 差：按参数列说明。如：
#   URL: 文章链接  --format: 输出格式  命令: python3 scripts/cli.py [URL] [OPTIONS]

### 场景一：[TODO: 场景名称]

[TODO: 注释说明 + 完整命令/步骤]

### 场景二：[TODO: 场景名称]

[TODO: 注释说明 + 完整命令/步骤]

## 补充说明

[TODO: 堵死岔路口——覆盖依赖缺失、输入异常、常见错误的兜底方案]
# 好的补充说明示例：
#   - WeSpy 未安装：优先用本地源码路径；不存在则 git clone；clone 失败则报错提示用户手动安装
#   - 网络超时：单次 30 秒，重试 2 次；仍失败则跳过，报告失败列表
#   - 同名文件已存在：追加数字后缀，不覆盖
# 差：处理异常、确保依赖安装、注意网络问题

- [TODO: 依赖不存在时的处理方式]
- [TODO: 输入格式不对时的处理方式]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 的辅助脚本

这是一个占位脚本，可直接执行。
根据实际需求替换实现，或在不需要时删除。
"""
import sys

def main():
    print("Hello from {skill_name}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

EXAMPLE_REFERENCE = """# {skill_title} 参考资料

本文件存放超出 SKILL.md 篇幅的详细参考内容。

Agent 会在需要时按需加载本文件。在 SKILL.md 中用以下方式引用：

> 详细规范见 references/本文件名.md
"""


def title_from_name(name: str) -> str:
    parts = name.split("-")
    return " ".join(p.capitalize() for p in parts if p)


def init_skill(skill_name: str, base_path: str) -> Path | None:
    skill_dir = Path(base_path) / skill_name

    if skill_dir.exists():
        print(f"错误: 目录已存在: {skill_dir}")
        return None

    if not re.match(r"^[a-z][a-z0-9-]*$", skill_name):
        print(f"错误: name 必须是 kebab-case（小写字母开头，只含小写字母、数字、连字符），当前: {skill_name}")
        return None

    if skill_name.startswith("-") or skill_name.endswith("-") or "--" in skill_name:
        print(f"错误: name 不能以连字符开头/结尾，也不能包含连续连字符，当前: {skill_name}")
        return None

    if len(skill_name) > 64:
        print(f"错误: name 不得超过 64 字符，当前 {len(skill_name)} 字符")
        return None

    skill_title = title_from_name(skill_name)

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"创建目录: {skill_dir}")
    except Exception as e:
        print(f"错误: {e}")
        return None

    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(
            SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title),
            encoding="utf-8",
        )
        print(f"创建: SKILL.md")
    except Exception as e:
        print(f"错误: {e}")
        return None

    try:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / "example.py"
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name), encoding="utf-8")
        example_script.chmod(0o755)
        print(f"创建: scripts/example.py")

        references_dir = skill_dir / "references"
        references_dir.mkdir(exist_ok=True)
        example_ref = references_dir / "reference.md"
        example_ref.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title), encoding="utf-8")
        print(f"创建: references/reference.md")
    except Exception as e:
        print(f"错误: {e}")
        return None

    print(f"\n技能 '{skill_name}' 初始化完成: {skill_dir}")
    print(f"\n后续步骤:")
    print(f"1. 编辑 SKILL.md，完成所有 [TODO] 项")
    print(f"2. 按四层骨架组织：头部 → 概述 → 操作指南 → 补充说明")
    print(f"3. 替换或删除 scripts/、references/ 中的示例文件")
    print(f"4. 运行质量检查（见 references/checklist.md）")
    return skill_dir


def main():
    if len(sys.argv) < 2:
        print("用法: python3 init_skill.py <skill-name> [--path <path>]")
        sys.exit(1)

    skill_name = sys.argv[1]

    base_path = DEFAULT_PATH
    if "--path" in sys.argv:
        idx = sys.argv.index("--path")
        if idx + 1 < len(sys.argv):
            base_path = sys.argv[idx + 1]

    result = init_skill(skill_name, base_path)
    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
