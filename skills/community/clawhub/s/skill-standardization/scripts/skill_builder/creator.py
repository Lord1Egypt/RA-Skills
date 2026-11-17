#!/usr/bin/env python3
"""
SkillCreator — 负责 create 模式（创建新 Skill）
模板严格遵循 R-01~R-21 规范
"""

import json
import sys
import tempfile
import os
from pathlib import Path


class SkillCreator:
    """Skill 创建器"""

    SKILL_TEMPLATE = """---
name: {name}
version: 0.1.0
author: your-name-here
license: MIT
description: >
  {description}
tags: []
data_dir: ../.standardization/{name}/
external_data_dir: true
sensitive_access: false
critical_write: false
permission_weight: LOW
trigger: 生成报告/分析数据/转换格式
trigger_negative: 闲聊/翻译/简单问答
h1_position: true
meta_field_sync: true
create_permissions_md: true
trigger_quality: add_triggers
faq_unparsable: reformat
antipattern_count: add_examples

# {name} — {description}

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

## 约束

- **[必须] 输入验证** — 输入文件必须存在且格式正确，否则阻断
- **[必须] 输出规范** — 输出写入 `DATA_DIR/outputs/`，不得写入技能目录
- **[必须] 路径集中管理** — 所有路径从 `scripts/_paths.py` 导入，禁止硬编码

## 触发条件

当用户提到以下意图时触发本技能：
- `"/{name}"` 直接调用
- 用户描述任务包含：生成XX、分析XX、转换XX
- 用户要求输出格式为：Markdown / JSON / HTML

**不触发**：
- 用户仅询问概念、定义，不要求执行操作
- 用户明确要求使用其他指定技能

## 核心能力

| # | 功能 | 说明 |
|---|------|------|
| 1 | 主功能 | 读取输入 → 处理 → 输出结果 |
| 2 | 辅助功能 | 校验输入格式，生成摘要报告 |

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
|--------|------|----------|----------|
| `references/guide.md` | 使用指南 | 参数说明和完整工作流 | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描报告、风险说明和 skill-function-test 测试结论 | R-15, R-16 |
| `references/examples.md` | 使用示例 | 使用示例和输出样例 | 无 |
| `references/changelog.md` | 版本管理 | 版本变更记录 | R-24 |
| `references/antipatterns.md` | 规范指南 | 常见反模式与正确做法 | R-18 |
| `references/faq.md` | 常见问题 | 常见疑问与解答 | R-19 |

## 数据目录

所有路径从 `scripts/_paths.py` 统一管理，不要在代码中手写路径：

```python
from scripts._paths import DATA_DIR, OUTPUTS_DIR
# DATA_DIR  = skills/.standardization/{name}/data/
# OUTPUTS_DIR = skills/.standardization/{name}/outputs/
```

> 详细路径常量见 `scripts/_paths.py`

## 快速开始

```bash
# 最简用法
skill-sub {name} --input <input-file> --output <output-dir>
```

## 工作流程

1. **解析输入** — 输入 用户文件/参数 → 输出 结构化数据
2. **执行核心逻辑** — 输入 结构化数据 → 输出 处理结果
3. **输出结果** — 输入 处理结果 → 输出 `OUTPUTS_DIR/result`

## 权限说明

本技能需要以下权限才能正常工作：

| 工具 | 访问级别 | 用途 |
|------|----------|------|
| Read | read-only | 读取输入文件和配置 |
| Write | write | 写入输出结果 |
| Bash | restricted | 运行内部处理脚本（仅限 `scripts/` 目录） |

- **不会**访问系统敏感路径或凭证文件
- **不会**向外部网络发送数据
- **不会**执行用户 Shell 配置文件（`.bashrc` / `.zshrc`）

---

> 反模式详见 `references/antipatterns.md`，常见问题详见 `references/faq.md`

> 本文档由 `skill-standardization` 生成，遵循 R-01~R-25 规范。
"""

    META_TEMPLATE = """{{
  "name": "{name}",
  "version": "0.1.0",
  "description": "{description}",
  "author": "your-name-here",
  "tags": [{tags_json}],
  "data_dir": "skills/.standardization/{name}/",
  "triggers": []
}}"""

    def create(self, args):
        """创建新的标准 skill 目录结构"""
        name = args.name
        description = args.desc or f"{name} skill"
        tags = args.tags or []
        base_dir = Path(args.dir) if args.dir else Path.cwd()

        skill_dir = base_dir / name

        # 检查是否已存在
        if skill_dir.exists():
            print(f"[X] 目录已存在: {skill_dir}")
            return False

        # 创建目录结构（技能自身目录：仅有 SKILL.md + references/ + scripts/）
        skill_dir.mkdir(parents=True)
        (skill_dir / "references").mkdir(exist_ok=True)
        (skill_dir / "scripts").mkdir(exist_ok=True)

        # 创建标准化产出物目录（skills/.standardization/<name>/，R-11 合规）
        std_dir = base_dir / ".standardization" / name
        (std_dir / "data").mkdir(parents=True, exist_ok=True)
        (std_dir / "outputs").mkdir(exist_ok=True)
        (std_dir / "cache").mkdir(exist_ok=True)
        (std_dir / "temp").mkdir(exist_ok=True)
        (std_dir / "backup").mkdir(exist_ok=True)

        # 写入 SKILL.md
        tags_str = ", ".join(f'"{t}"' for t in tags) if tags else '"todo"'
        tags_simple = ", ".join(tags) if tags else "todo"

        skill_content = self.SKILL_TEMPLATE.format(
            name=name,
            description=description,
        )
        (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")

        # 写入 _meta.json
        meta_content = self.META_TEMPLATE.format(
            name=name,
            description=description,
            tags_json=tags_str,
        )
        (skill_dir / "_meta.json").write_text(meta_content, encoding="utf-8")

        # 创建 .gitkeep 保持空目录
        (skill_dir / "references" / ".gitkeep").write_text("", encoding="utf-8")
        (skill_dir / "scripts" / ".gitkeep").write_text("", encoding="utf-8")

        # 创建 scripts/_paths.py（路径集中管理模板，R-11/R-12 合规）
        paths_content = self._generate_paths_template(name)
        (skill_dir / "scripts" / "_paths.py").write_text(paths_content, encoding="utf-8")

        # 创建 references/guide.md 详细文档模板
        guide_content = self._generate_guide_template(name, description)
        (skill_dir / "references" / "guide.md").write_text(guide_content, encoding="utf-8")

        # 创建 references/permissions.md 模板
        perm_content = self._generate_permissions_template(name)
        (skill_dir / "references" / "permissions.md").write_text(perm_content, encoding="utf-8")

        # 创建 references/examples.md 模板
        examples_content = self._generate_examples_template(name)
        (skill_dir / "references" / "examples.md").write_text(examples_content, encoding="utf-8")

        # 创建 references/LICENSE.md（空白 MIT 模板，R-26）
        license_content = self._generate_license_template(name)
        (skill_dir / "references" / "LICENSE.md").write_text(license_content, encoding="utf-8")

        # 创建 .progress.md
        progress_content = self._generate_progress_template(name)
        (skill_dir / ".progress.md").write_text(progress_content, encoding="utf-8")

        # 创建 references/changelog.md（R-24）
        changelog_content = self._generate_changelog_template(name)
        (skill_dir / "references" / "changelog.md").write_text(changelog_content, encoding="utf-8")

        # 创建 references/antipatterns.md（R-18）
        antipatterns_content = self._generate_antipatterns_template(name)
        (skill_dir / "references" / "antipatterns.md").write_text(antipatterns_content, encoding="utf-8")

        # 创建 references/faq.md（R-19）
        faq_content = self._generate_faq_template(name)
        (skill_dir / "references" / "faq.md").write_text(faq_content, encoding="utf-8")

        print(f"[OK] Skill 已创建: {skill_dir}")
        print(f"   ├── SKILL.md           (主文件, ≤230行)")
        print(f"   ├── _meta.json         (元数据 + 数据目录声明)")
        print(f"   ├── .progress.md       (审计进度跟踪)")
        print(f"   ├── references/")
        print(f"   │   ├── guide.md       (完整使用教程)")
        print(f"   │   ├── permissions.md  (权限说明)")
        print(f"   │   ├── examples.md    (使用示例)")
        print(f"   │   ├── changelog.md   (版本变更记录)")
        print(f"   │   ├── antipatterns.md(常见反模式)")
        print(f"   │   └── faq.md         (常见问题)")
        print(f"   ├── scripts/")
        print(f"   │   └── _paths.py      (路径集中管理, R-11合规)")
        print(f"   └── .standardization/{name}/  (产出物目录, R-11合规)")
        print(f"       ├── data/          (业务数据)")
        print(f"       ├── outputs/       (导出产物)")
        print(f"       ├── cache/         (缓存)")
        print(f"       ├── temp/          (临时文件)")
        print(f"       └── backup/        (备份)")
        print(f"\n下一步:")
        print(f"   1. 编辑 SKILL.md 填写触发词和核心能力")
        print(f"   2. 编辑 references/guide.md 填写详细教程")
        print(f"   3. 如需脚本，放入 scripts/")
        print(f"   4. 运行审计: python -m skill_audit audit {skill_dir}")
        print(f"   5. 修复问题: python -m skill_audit audit {skill_dir} --fix")

        # 审计 + 进度管理
        self._audit_and_update_progress(skill_dir, mode="create")
        return True

    def _generate_guide_template(self, name, description):
        """生成 references/guide.md 模板"""
        return f"""# {name} — 完整使用教程

{description}

## 目录

1. [安装与依赖](#安装与依赖)
2. [快速开始](#快速开始)
3. [参数说明](#参数说明)
4. [工作流程详解](#工作流程详解)
5. [输出格式](#输出格式)
6. [常见问题](#常见问题)
7. [错误处理](#错误处理)

---

## 安装与依赖

### 依赖项

| 依赖 | 版本要求 | 用途 |
|------|----------|------|
| Python | >=3.8 | 运行脚本 |
| <!-- 其他依赖 --> | <!-- 版本 --> | <!-- 用途 --> |

### 安装步骤

1. 确保本技能已通过 `skill-standardization` 创建
2. 安装依赖：`pip install -r requirements.txt`（如有）
3. 验证安装：运行 `python scripts/{name}_main.py --help`

## 快速开始

```bash
# 最简用法
python scripts/{name}_main.py --input input.txt --output output/

# 带可选参数
python scripts/{name}_main.py --input input.txt --output output/ --verbose
```

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--input` | path | 是 | - | 输入文件路径 |
| `--output` | path | 否 | `data/output/` | 输出目录 |
| `--verbose` | flag | 否 | `False` | 输出详细日志 |
| `--config` | path | 否 | `references/config.json` | 配置文件路径 |

## 工作流程详解

### 阶段 1：输入解析

- 读取 `--input` 指定的文件
- 验证文件格式和内容完整性
- 解析参数为内部数据结构

### 阶段 2：核心处理

- 调用核心算法/逻辑进行处理
- 支持的处理模式：
  - 模式 A：<!-- 描述 -->
  - 模式 B：<!-- 描述 -->

### 阶段 3：输出生成

- 将处理结果写入 `--output` 目录
- 生成摘要报告 `summary.md`
- 记录执行日志到 `data/logs/`

## 输出格式

### 输出文件列表

| 文件 | 格式 | 说明 |
|------|------|------|
| `summary.md` | Markdown | 处理摘要 |
| `result.json` | JSON | 结构化结果 |
| `details.csv` | CSV | 详细数据（可选） |

### 输出示例

```json
{{
  "status": "success",
  "input_file": "input.txt",
  "output_dir": "output/",
  "processed_items": 42,
  "errors": []
}}
```

## 常见问题

### Q: 输入文件格式不正确怎么办？
A: 技能会输出明确的错误信息，指出格式问题和期望的格式。请参考本文档"输入格式"章节。

### Q: 如何处理大文件？
A: 对于超过 10MB 的文件，建议使用流式处理模式，添加 `--stream` 参数。

## 错误处理

### 错误代码

| 代码 | 含义 | 处理方式 |
|------|------|----------|
| E001 | 输入文件不存在 | 检查文件路径 |
| E002 | 输入格式错误 | 参考"输入格式"章节 |
| E003 | 输出目录不可写 | 检查权限或换用 `--output` |
| E004 | 依赖缺失 | 运行 `pip install -r requirements.txt` |

### 错误恢复

- 所有错误都会记录到 `data/logs/error.log`
- 支持 `--retry` 参数进行自动重试（最多 3 次）
- 严重错误会生成 `data/rollback/` 目录用于回滚

---

> 本文档遵循 R-06 渐进式加载规范，由 `skill-standardization` 生成。
"""

    def _generate_permissions_template(self, name):
        """生成 references/permissions.md 模板"""
        return f"""# {name} — 基于skill-standardization渐进式披露规范的权限说明

本文档由 `skill-standardization` 权限扫描器自动生成，描述本技能运行所需的权限及其风险等级。

## 权限总览

| 工具 | 访问级别 | 风险等级 | 授权方式 | 说明 |
|------|----------|----------|----------|------|
| Read | read-only | 低 | 静默 | 读取输入文件和配置 |
| Write | write | 中 | 即时 | 写入输出结果到 `data/output/` |
| Bash | restricted | 中 | 统一 | 运行 `scripts/` 目录下的内部脚本 |

## 权限详细说明

### Read（读取）

- **用途**：读取用户输入文件、配置文件、参考数据
- **范围限制**：仅读取技能安装目录和指定输入文件，不访问系统敏感路径
- **不会读取**：系统敏感路径或凭证文件

### Write（写入）

- **用途**：将处理结果写入输出目录
- **范围限制**：仅写入 `data/output/` 目录，不写入安装目录或其他系统目录
- **文件覆盖策略**：默认不覆盖现有文件，添加 `--force` 参数可覆盖

### Bash（命令执行）

- **用途**：运行内部处理脚本
- **范围限制**：仅执行 `scripts/` 目录下的脚本，不执行用户 Shell 配置
- **不会执行**：`rm -rf /`、`curl` 外部 URL、`git` 远程操作等危险命令

## 风险缓解措施

1. **输入验证**：所有用户输入都经过格式和范围验证
2. **输出隔离**：输出文件限制在 `data/output/` 目录内
3. **错误隔离**：单个文件处理失败不影响整体流程
4. **审计日志**：所有操作记录到 `data/logs/audit.log`

## 授权方式说明

- **即时授权**：每次执行前需获得用户批准（用于 Write 操作）
- **统一授权**：首次执行前获得用户批准，后续不再询问（用于 Bash 操作）
- **静默授权**：无需用户交互，自动执行并记录（用于 Read 操作）

---

> 本文档会在每次运行 `python -m skill_audit audit . --fix` 后自动更新。
"""

    def _generate_examples_template(self, name):
        """生成 references/examples.md 模板"""
        return f"""# {name} — 使用示例

本文档提供本技能的常见使用场景和完整示例。

## 目录

1. [示例 1：基本用法](#示例-1基本用法)
2. [示例 2：批量处理](#示例-2批量处理)
3. [示例 3：自定义配置](#示例-3自定义配置)
4. [示例 4：错误处理](#示例-4错误处理)

---

## 示例 1：基本用法

### 场景描述

<!-- 描述一个简单的使用场景 -->

### 输入

`input.txt`:
```
<!-- 示例输入内容 -->
```

### 执行命令

```bash
python scripts/{name}_main.py --input input.txt --output output/
```

### 预期输出

`output/summary.md`:
```markdown
<!-- 示例输出内容 -->
```

---

## 示例 2：批量处理

### 场景描述

<!-- 描述批量处理多个文件的场景 -->

### 输入

`inputs/` 目录包含多个文件：
```
inputs/
  ├── file1.txt
  ├── file2.txt
  └── file3.txt
```

### 执行命令

```bash
for file in inputs/*.txt; do
  python scripts/{name}_main.py --input "$file" --output output/
done
```

### 预期输出

```
output/
  ├── file1_summary.md
  ├── file2_summary.md
  └── file3_summary.md
```

---

## 示例 3：自定义配置

### 场景描述

<!-- 描述使用自定义配置文件的场景 -->

### 配置文件

`references/config.json`:
```json
{{
  "param1": "value1",
  "param2": 42,
  "enabled": true
}}
```

### 执行命令

```bash
python scripts/{name}_main.py --input input.txt --config references/config.json
```

---

## 示例 4：错误处理

### 场景描述

输入文件格式错误，查看错误处理和恢复流程。

### 输入（错误格式）

`bad_input.txt`:
```
<!-- 错误格式的内容 -->
```

### 执行命令

```bash
python scripts/{name}_main.py --input bad_input.txt --output output/
```

### 预期错误输出

```
[ERROR] E002: 输入格式错误
  期望格式: <!-- 正确格式描述 -->
  实际内容: <!-- 错误内容描述 -->
  
建议: 请参考 `references/guide.md` 的"输入格式"章节
```

### 修复后重试

```bash
# 修复输入文件后重试
python scripts/{name}_main.py --input fixed_input.txt --output output/ --retry
```

---

## 输出样例

### 样例 1：成功结果

```json
{{
  "status": "success",
  "input_file": "input.txt",
  "output_dir": "output/",
  "result": {{
    // 结果数据
  }}
}}
```

### 样例 2：部分成功（有警告）

```json
{{
  "status": "partial_success",
  "input_file": "input.txt",
  "warnings": [
    "第 42 行数据格式异常，已跳过"
  ],
  "result": {{
    // 部分结果数据
  }}
}}
```

---

> 更多示例欢迎通过 PR 贡献到本文件的后续章节。
"""

    def _generate_antipatterns_template(self, name):
        """生成 references/antipatterns.md 模板（R-18）"""
        return f"""# {name} — 反模式与常见错误

## 1. 跳过输入验证

- **错误做法**：直接假设输入数据格式正确，不做检查就开始处理。
- **正确做法**：在入口处校验输入格式和必填字段，不符合时提示。

## 2. 硬编码路径

- **错误做法**：在代码中直接写入绝对路径或写死相对路径。
- **正确做法**：所有路径从 `scripts/_paths.py` 导入。

## 3. 不记录错误信息

- **错误做法**：抛出异常后不记录任何上下文，用户无法排查。
- **正确做法**：捕获异常后打印关键变量值和操作上下文。

> 更多反模式欢迎通过 PR 贡献。
"""

    def _generate_paths_template(self, name):
        """生成 scripts/_paths.py 路径集中管理模板（R-11/R-12 合规）"""
        return f'''"""
_paths.py — {name} 路径集中管理
只包含路径常量和路径推导函数，不包含任何业务逻辑。
所有脚本从本模块导入路径，禁止硬编码。
"""
import os
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR    = _SCRIPT_DIR.parent
SKILLS_ROOT  = SKILL_DIR.parent
SKILL_NAME   = SKILL_DIR.name

STD_ROOT     = SKILLS_ROOT / ".standardization"
STD_DIR      = STD_ROOT / SKILL_NAME
DATA_DIR     = STD_DIR / "data"
OUTPUTS_DIR  = STD_DIR / "outputs"
BACKUP_DIR   = STD_DIR / "backup"
CACHE_DIR    = STD_DIR / "cache"
TEMP_DIR     = STD_DIR / "temp"
'''

    def _generate_faq_template(self, name):
        """生成 references/faq.md 模板（R-19）"""
        return f"""# {name} — 常见问题（FAQ）

## 一、参数错误

### Q: 运行报"参数错误"

**原因：** 传入的参数数量或顺序不对。
**修复：** 查阅 SKILL.md 中的用法说明或运行 --help。

## 二、依赖错误

### Q: 提示 XX 模块未安装

**原因：** 缺少 Python 依赖包。
**修复：** 确认满足环境要求后重新运行。

## 三、环境错误

### Q: 技能无法启动

**原因：** 可能是不支持的操作系统或 Python 版本。
**修复：** 确认环境满足 SKILL.md 中的环境要求。
"""

    def _generate_license_template(self, name):
        """生成 references/LICENSE.md 模板（空白 MIT，R-26 规范）"""
        return f"""MIT License

Copyright (c) 2026 your-name-here

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    def _generate_progress_template(self, name):
        """生成 .progress.md 模板"""
        return f"""# {name} — 审计进度跟踪

本文档记录本技能通过 `skill-standardization` 审计的进度。

## 审计状态

- **技能名称**：`{name}`
- **当前版本**：`0.1.0`
- **审计工具版本**：`skill-standardization v2.29.2`
- **最后审计时间**：待首次审计
- **通过规则数**：0 / 21
- **待修复问题数**：0

## 规则检查进度

| 规则 | 状态 | 问题数 | 最后检查 |
|------|------|--------|----------|
| R-01 | [待检查] | 0 | - |
| R-02 | [待检查] | 0 | - |
| R-03 | [待检查] | 0 | - |
| R-04 | [待检查] | 0 | - |
| R-05 | [待检查] | 0 | - |
| R-06 | [待检查] | 0 | - |
| R-07 | [待检查] | 0 | - |
| R-08 | [待检查] | 0 | - |
| R-09 | [待检查] | 0 | - |
| R-10 | [待检查] | 0 | - |
| R-11 | [待检查] | 0 | - |
| R-12 | [待检查] | 0 | - |
| R-13 | [待检查] | 0 | - |
| R-14 | [待检查] | 0 | - |
| R-15 | [待检查] | 0 | - |
| R-16 | [待检查] | 0 | - |
| R-17 | [待检查] | 0 | - |
| R-18 | [待检查] | 0 | - |
| R-19 | [待检查] | 0 | - |
| R-20 | [待检查] | 0 | - |
| R-21 | [待检查] | 0 | - |

## 修复历史

| 日期 | 修复内容 | 修复者 |
|------|----------|--------|
| - | 待首次审计 | - |

## 待办事项

- [ ] 运行首次审计：`python -m skill_audit audit .`
- [ ] 修复所有 ERROR 级别问题
- [ ] 确认所有 WARN 级别问题已 Review
- [ ] 提交首次版本并通过审计

---

> 本文档会在每次运行 `python -m skill_audit audit . --fix` 后自动更新。
"""

    def _generate_changelog_template(self, name):
        """生成 CHANGELOG.md 模板"""
        return f"""# {name} — 变更日志

本文档记录 `{name}` 技能的版本变更，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 规范。

## [未发布]

### 新增
- （待添加）

### 修改
- （待添加）

### 修复
- （待添加）

### 移除
- （待添加）

---

## [0.1.0] - 2026-05-26

### 新增
- 初始版本，由 `skill-standardization v2.29.2` 创建
- 基础目录结构：`SKILL.md`、`references/`、`scripts/`
- 产出物目录：`.standardization/{name}/`（R-11/R-12 标准结构）
- 支持基本输入处理和结果输出
- 包含权限声明（R-07 合规）
- 包含渐进式加载文档体系（R-06 合规）

### 已知限制
- 暂不支持流式处理大文件
- 暂未实现缓存机制
- 错误处理仅支持基本错误类型

---

## 版本号说明

本技能遵循 **语义化版本 2.0.0**（Semantic Versioning）：

- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

---

> 变更日志由 `skill-standardization` 维护，每次版本发布时更新本节。
"""

    def _audit_and_update_progress(self, skill_dir, mode="create"):
        """审计 skill 并更新 .progress.md（直接调用，不通过 subprocess）"""
        from pathlib import Path
        from skill_audit import audit_skill, format_report

        skill_dir = Path(skill_dir).resolve()
        progress_file = skill_dir / ".progress.md"

        # 1. 创建 .progress.md
        from skill_audit.progress_manager import create_progress
        create_progress(str(skill_dir), mode)

        # 2. 运行审计（直接调用审计函数，避免 subprocess 风险）
        try:
            audit_result = audit_skill(str(skill_dir), progress_file=str(progress_file))
        except Exception as e:
            print(f"[!] 审计执行失败: {e}")
            return

        # 3. 打印报告（audit_sKill 已自动更新 .progress.md）
        print(format_report(audit_result, verbose=True))

    # ── 权限扫描结果自动写入 references/permissions.md ──────────────────

    def _write_permissions_md(self, skill_dir, report):
        """将权限扫描报告自动写入 references/permissions.md"""
        from pathlib import Path
        import json

        skill_dir = Path(skill_dir)
        pm = skill_dir / "references" / "permissions.md"
        issues = report.get("issues", [])
        risk_level = report.get("risk_level", "unknown")

        if not issues:
            print("[!] 权限扫描无风险项，跳过 permissions.md 写入")
            return

        lines = []
        lines.append("# 基于skill-standardization渐进式披露规范的权限说明\n")
        lines.append(f"权限扫描风险等级：**{risk_level}**\n")
        lines.append("## 权限总览\n")
        lines.append(f"共 {len(issues)} 项权限风险，按类别分组如下：\n")

        # 按类别分组（使用 type 字段，而非 category）
        categories = {}
        for iss in issues:
            cat = iss.get("type", "other")
            categories.setdefault(cat, []).append(iss)

        # 类型中文映射
        type_cn = {
            "sensitive_access": "敏感信息访问",
            "critical_write": "关键位置写入",
            "network_access": "网络访问",
            "file_delete": "文件删除",
            "subprocess_call": "子进程调用",
            "missing_declaration": "缺少声明",
        }
        cat_desc = {
            "sensitive_access": "读取内存文件、凭证、Token 等敏感数据",
            "critical_write": "向系统关键目录或 skills/ 安装目录写入文件",
            "network_access": "通过 HTTP/HTTPS 向外发送请求或接收数据",
            "file_delete": "删除文件或目录（可能不可逆）",
            "subprocess_call": "调用系统命令或其他可执行文件",
            "missing_declaration": "SKILL.md frontmatter 未声明对应权限字段",
        }

        for cat, items in categories.items():
            cat_name = type_cn.get(cat, cat)
            cat_action = cat_desc.get(cat, "未知权限作用")
            lines.append(f"### {cat_name}（{len(items)} 项）")
            lines.append(f"> **权限作用**：{cat_action}")
            lines.append("")
            lines.append("| # | 文件 | 行号 | 匹配内容 | 风险等级 | 授权方式 | 说明 |")
            lines.append("|---|------|----------|----------|----------|------|")
            for i, iss in enumerate(items, 1):
                sev = iss.get("severity", "?")
                sev_cn = {"HIGH": "[高]", "MEDIUM": "[中]", "LOW": "[低]", "ERROR": "[高]"}.get(sev, sev)
                file = iss.get("file", "")
                line = iss.get("line", "")
                match = iss.get("match", iss.get("pattern", ""))[:50]
                method = iss.get("authorization_method", "immediate")
                method_cn = {"immediate": "即时授权", "unified": "统一授权", "silent": "静默"}.get(method, method)
                reason = iss.get("reason", "")
                desc = iss.get("description", "")
                lines.append(f"| {i} | `{file}` | {line} | `{match}` | {sev_cn} | {method_cn} | {desc} |")
            lines.append("")

        lines.append("## 授权方式说明\n")
        lines.append("- **即时授权**：每次执行前需获得用户批准")
        lines.append("- **统一授权**：首次执行前获得用户批准，后续不再询问")
        lines.append("- **静默授权**：无需用户交互，自动执行并记录")
        lines.append("")
        lines.append("## 详细风险列表\n")
        for i, iss in enumerate(issues, 1):
            sev = iss.get("severity", "?")
            sev_cn = {"HIGH": "高", "MEDIUM": "中", "LOW": "低", "ERROR": "高"}.get(sev, sev)
            desc = iss.get("description", "")
            file = iss.get("file", "")
            line = iss.get("line", "")
            reason = iss.get("reason", "")
            lines.append(f"{i}. **[{sev_cn}] {desc}**")
            lines.append(f"   - 位置：`{file}` 第 {line} 行")
            if reason:
                lines.append(f"   - 原因：{reason}")
            lines.append("")

        pm.parent.mkdir(parents=True, exist_ok=True)
        new_content = "\n".join(lines)
        # 文件已存在且不含 skill-standardization 头部时，保留原有内容在下方
        if pm.exists():
            existing = pm.read_text(encoding="utf-8")
            if "基于skill-standardization渐进式披露规范的权限说明" not in existing:
                new_content = new_content + "\n\n---\n\n" + existing
        pm.write_text(new_content, encoding="utf-8")
        print(f"[OK] 权限扫描结果已自动写入 {pm}")

    def _get_category_description(self, category):
        """返回权限类别的中文描述"""
        descs = {
            "file_write": "写入文件（可能覆盖或破坏现有文件）",
            "file_read": "读取文件（可能访问敏感信息）",
            "network": "网络通信（可能传输数据到外部）",
            "subprocess": "执行外部命令（可能执行恶意代码）",
            "env_var": "读取环境变量（可能泄露系统信息）",
            "user_interaction": "用户交互（需要用户授权）",
            "other": "其他权限",
        }
        return descs.get(category, "未知权限类别")

    def _get_item_explanation(self, item):
        """返回权限项的详细解释"""
        return item.get("description", "无详细描述")

    def _get_auth_method(self, method):
        """返回授权方式的中文说明"""
        methods = {
            "immediate": "即时授权（每次执行前需获得用户批准）",
            "unified": "统一授权（首次执行前获得用户批准，后续不再询问）",
            "silent": "静默授权（无需用户交互，自动执行并记录）",
        }
        return methods.get(method, "未知授权方式")
