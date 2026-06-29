## [1.3.0] - 2026-06-12

### 新增
- **三阶段架构（Phase A/B/C）**: 环境准备→语义路由→工具箱/脚本流水线
- **scripts/hook_runner.py**: 18 个流程钩子，check/done/fail/status/reset 命令
- **自引用 I/O**: 所有文件写入强制通过 text_crud.py / file_ops.py / atomic_write()
- **H-C10 报告直通**: 路由定了就能出报告，不依赖 C/B 链执行结果

### 修复
- skill-standardization 审计 25/25 通过，0 ERROR
- fix_and_test.py import 行损坏（R-12 审计锚点导致）
- 错误码 UFO-4004/UFO-4005 更新

### 更新
- 版本 1.2.0 → 1.3.0
- SKILL.md 拆分为渐进式加载体系（≤230 行）
- 输出报告规范固定为 3 个 JSON 模板（A/B/C）

---

## [1.2.0] - 2026-06-12

### 修复
- refactor: universal-file-ops

---

## 1.1.2 (2026-05-30)

### 修复
- audit --fix 自动修正

---

# 更新日志（Changelog）

> 本文件记录 universal-file-ops 的版本更新历史。
> 遵循 [Keep a Changelog](https://keepachangelog.com/) 格式，基于 SemVer 版本管理。

---

## 1.1.0 (2026-05-27)

**改写类型：Minor — 重建 python_env.py + 修复 _log() 输出 + 修复 utils.py 定义顺序**

### 修复
- **重建 `scripts/python_env.py`**：因错误修复脚本导致文件被清空（0 字节），用构建脚本完整重建
- **修复 `scripts/python_env.py` `_log()` 函数**：输出目标从 `stdout` 改为 `sys.stderr`，避免污染 JSON 输出导致解析失败
- **修复 `scripts/utils.py` 定义顺序**：`VENV_DIR` 定义在 `_data_dir_abs` 之前导致 `NameError`，调整定义顺序
- **修复 `scripts/py_tools.py` 拼写错误**：`ast.FunctionionDef` → `ast.FunctionDef`（4 处）

### 新增
- （无）

### 更新
- `SKILL.md` frontmatter 版本号更新为 1.1.0
- `_meta.json` 版本号和描述更新

### 测试
- **18/18 功能测试全部通过**：
  - `py_tools.py`（normalize / review / oo-ify / gen-test）
  - `python_env.py`（detect / setup / list / install）
  - `file_ops.py`（copy / rename / delete）
  - `text_crud.py`（create / read / update / delete）
  - `rollback.py`（list / rollback）
  - `orchestrator.py`（`--list` / `--dry-run`）


## v1.3.0 (2026-06-12)

**改写类型：Minor — 三阶段架构 + 流程钩子系统 + skill-standardization 审计修复**

### 新增
- **三阶段架构（Phase A/B/C）**：环境准备→语义路由→工具箱/脚本流水线
- **scripts/hook_runner.py**：18 个流程钩子，check/done/fail/status/reset 命令
- **自引用 I/O**：所有文件写入强制通过 text_crud.py / file_ops.py / atomic_write()
- **H-C10 报告直通**：路由定了就能出报告，不依赖 C/B 链执行结果

### 修复
- skill-standardization 审计 25/25 通过，0 ERROR
- fix_and_test.py import 行损坏（R-12 审计锚点导致）
- 错误码 UFO-4004/UFO-4005 更新

### 更新
- 版本 1.2.0 → 1.3.0
- SKILL.md 拆分为渐进式加载体系（≤230 行）
- 输出报告规范固定为 3 个 JSON 模板（A/B/C）

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
