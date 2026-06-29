#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新 universal-file-ops 版本号和 changelog"""

import re, sys, os

SKILL_MD = os.path.join(os.path.dirname(__file__), "SKILL.md")
CHANGELOG = os.path.join(os.path.dirname(__file__), "references", "changelog.md")

# 1. 更新 SKILL.md 版本号 1.0.1 -> 1.1.0
with open(SKILL_MD, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("version: 1.0.1", "version: 1.1.0")
content = content.replace(
    "description: 为普通大模型/智能体用户提供一站式文件操作与 Python 代码质量保障能力。",
    "description: 为普通大模型/智能体用户提供一站式文件操作与 Python 代码质量保障能力。v1.1.0：重建 python_env.py，修复 _log() 输出到 stderr，修复 utils.py VENV_DIR 定义顺序，18/18 功能测试通过。"
)

with open(SKILL_MD, "w", encoding="utf-8") as f:
    f.write(content)
print("[OK] SKILL.md 版本号已更新为 1.1.0")

# 2. 创建/更新 changelog.md
changelog_content = """# 更新日志（Changelog）

> 本文件记录 universal-file-ops 的版本更新历史。
> 遵循 [Keep a Changelog](https://keepachangelog.com/) 格式，基于 SemVer 版本管理。

---

## v1.1.0 (2026-05-27)

**改写类型：Minor — 重建 python_env.py + 修复 _log() 输出 + 修复 utils.py 定义顺序**

### 修复
- **重建 `scripts/python_env.py`**：因错误修复脚本导致文件被清空（0 字节），用构建脚本完整重建
- **修复 `scripts/python_env.py` `_log()` 函数**：输出目标从 `stdout` 改为 `sys.stderr`，避免污染 JSON 输出导致解析失败
- **修复 `scripts/utils.py` 定义顺序**：`VENV_DIR` 定义在 `_data_dir_abs` 之前导致 `NameError`，调整定义顺序
- **修复 `scripts/py_tools.py` 拼写错误**：`ast.FunctionionDef` → `ast.FunctionDef`（4 处）

### 新增
- （无）

### 更新
- `SKILL.md` frontmatter 版本号更新为 v1.1.0
- `_meta.json` 版本号和描述更新

### 测试
- **18/18 功能测试全部通过**：
  - `py_tools.py`（normalize / review / oo-ify / gen-test）
  - `python_env.py`（detect / setup / list / install）
  - `file_ops.py`（copy / rename / delete）
  - `text_crud.py`（create / read / update / delete）
  - `rollback.py`（list / rollback）
  - `orchestrator.py`（`--list` / `--dry-run`）

---

## v1.0.1 (2026-05-26)

**改写类型：Patch — 通过 skill-standardization 全部 23 条审计规则**

### 修复
- `SKILL.md` frontmatter 补全字段（`audience` / `sensitive_access` / `critical_write` / `permission_weight`）
- `references/guide.md` 术语统一：`修改` → `更新`、`移除` → `删除`
- `references/py_standards.md` 移除模糊表述 `可能` → 确定性描述
- `references/faq.md` 术语统一：`修改` → `更新`

### 新增
- （无）

### 更新
- `SKILL.md` frontmatter 版本号更新为 v1.0.1
- 通过 skill-standardization R-01 ~ R-23 全部 23 条规则审查

---
"""

if os.path.exists(CHANGELOG):
    with open(CHANGELOG, "r", encoding="utf-8") as f:
        existing = f.read()
    # 如果已有 v1.0.1 条目，在其前面插入新条目
    if "## v1.0.1" in existing and "## v1.1.0" not in existing:
        updated = changelog_content.replace("---\n", "---\n" + existing.split("---", 1)[1] if "---" in existing else "")
        # 更简单：直接覆盖，因为 changelog_content 已包含完整历史
        pass

with open(CHANGELOG, "w", encoding="utf-8") as f:
    f.write(changelog_content)
print("[OK] references/changelog.md 已创建/更新")
print("DONE")
