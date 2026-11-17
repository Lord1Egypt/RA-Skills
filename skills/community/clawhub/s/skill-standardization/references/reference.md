# API / 命令参考

> ⛔ **本文件已废弃。**
>
> 为消除过时信息导致的混淆，所有命令参考已迁移至：
>
> - **命令参考（完整）** → `references/guide.md`
> - **审计规则定义（R-01~R-26）** → `references/rules.md`
> - **示例** → `references/examples.md`
> - **FAQ** → `references/faq.md`
>
> 请使用上述文件获取最新准确信息。
>
> 本文件将在后续清理中移除，已从渐进式索引表中取消引用。


---

## CLI 命令参考

以下列出所有可通过命令行直接调用的脚本及其参数。

### safe_io — 标准化文件 IO

**已有 API 文档：** 见上文 [safe_io](#safe_io) 章节。

**CLI 子命令：**

```bash
# 读取文件（输出到 stdout 或指定文件）
python scripts/safe_io.py read --file <path> [--output <path>]

# 写入文件（覆盖，默认自动备份）
python scripts/safe_io.py write --file <path> --content "<text>" [--no-backup]
python scripts/safe_io.py write --file <path> --stdin [--no-backup]   # 从 stdin 读取

# 正则替换（默认自动备份）
python scripts/safe_io.py patch-regex --file <path> --pattern "<regex>" --replacement "<repl>" [--flags 0] [--no-backup]

# 按行号替换（默认自动备份）
python scripts/safe_io.py patch-line --file <path> --line <N> --content "<text>" [--no-backup]
```

**参数表：**

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--file` | str | 是 | - | 目标文件路径 |
| `--content` | str | 否 | `""` | 写入/替换内容 |
| `--stdin` | flag | 否 | False | 从标准输入读取(与`--content`互斥) |
| `--no-backup` | flag | 否 | False | 跳过自动备份(仅 write/patch-*) |
| `--pattern` | str | 是 | - | 正则表达式模式 |
| `--replacement` | str | 是 | - | 替换字符串 |
| `--flags` | int | 否 | 0 | Python re 标志位 |
| `--line` | int | 是 | - | 目标行号 |
| `--output` | str | 否 | stdout | 输出文件路径(仅 read) |

---

### permission_checker — 权限检查器

**已有 API 文档：** 见上文 [permission_checker](#permission_checker) 章节。

**CLI 用法：**

```bash
# 基础扫描
python scripts/permission_checker.py <skill_dir>

# 详细日志 + JSON 报告导出
python scripts/permission_checker.py <skill_dir> --verbose --output report.json
```

**参数表：**

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill_dir` | str(位置) | 是 | - | 技能根目录路径 |
| `--verbose` / `-v` | flag | 否 | False | 输出详细扫描日志 |
| `--output` / `-o` | str | 否 | None | JSON 报告输出路径 |

**Python API：**

```python
from permission_checker import PermissionChecker
checker = PermissionChecker('/path/to/skill', verbose=False)
report = checker.generate_report()  # 等价于 checker.scan()
# report = { 'risk_level': 'LOW', 'stats': {...}, 'findings': [...] }
```

---

### skill_audit.fix — 统一修复工具

**功能：** 为全部23条审计规则(R-01~R-26)提供针对性修复函数。`apply_fix()` 是统一入口。

**Python API（无独立 CLI）：**

```python
from skill_audit.fix import apply_fix, list_fixable

# 查看所有可修复的 key
keys = list_fixable()

# 修复单个规则
n = apply_fix('/path/to/skill', 'name', value='my-skill')          # R-01
n = apply_fix('/path/to/skill', 'version', value='1.2.3')          # R-04
n = apply_fix('/path/to/skill', 'sensitive_access', value=True)    # R-13
n = apply_fix('/path/to/skill', 'artifact_paths', violations=[...]) # R-11
```

**fix_key -> 规则映射表：**

| fix_key | 规则 | 修复行为 | 常用参数 |
|---------|------|----------|----------|
| `name` | R-01 | 添加/更正 name | value="技能名" |
| `description` | R-02 | 添加/更正 description | value="描述" |
| `author` | R-03 | 添加 author | value="作者名" |
| `version` | R-04 | 更正版本号格式 | value="1.2.3" |
| `skill_macro` | R-05 | 添加 skill_macro | value="unified" |
| `h1` | R-26 | 添加一级标题 | value="标题" |
| `section_trigger` | R-07 | 添加触发场景章节 | - |
| `section_core` | R-08 | 添加核心能力章节 | - |
| `section_workflow` | R-09 | 添加工作流程章节 | - |
| `home_url` | R-10 | 添加 home_url | value="URL" |
| `artifact_paths` | R-11 | 迁出违规文件 | violations=[...] |
| `external_data_dir` | R-12 | 统一数据目录路径 | - |
| `sensitive_access` | R-13 | 敏感访问声明 | value=True/False |
| `critical_write` | R-14 | 关键写入声明 | value=True/False |
| `create_permissions_md` | R-15 | 创建权限说明文档 | - |
| `permission_weight` | R-16 | 权限权重说明 | value="LOW/MEDIUM/HIGH/CRITICAL" |
| `progressive_loading` | R-17 | 渐进加载拆分 | - |
| `antipattern_progressive` | R-18 | 反模式到 references/ | - |
| `faq_progressive` | R-19 | FAQ 到 references/ | - |
| `writing_standards` | R-20 | 写作规范自动更正 | - |
| `progressive_loading_explicit` | R-21 | 渐进加载显式声明 | - |
| `data_dir_compliance` | R-22 | 数据目录规范修复 | dry_run=True/False |
| `doc_code_consistency` | R-23 | 文档-代码一致性 | - |

---

### progress_manager — 过程管理

**功能：** 读写 `.standardization/<skill>/.progress.md`，追踪审计执行进度。仅在审计结束后一次性更新，不逐条写入。

**Python API（无独立 CLI）：**

```python
from progress_manager import (
    create_progress,
    update_progress_from_audit,
    finalize_progress,
    load_progress,
    format_progress_markdown,
)

data_dir = 'skills/.standardization/my-skill'

# 创建进度文件
create_progress(data_dir, mode='update')

# 审计后更新进度
update_progress_from_audit(data_dir, audit_result)

# 写入最终结果
finalize_progress(data_dir, audit_result)

# 读取当前进度（用于断点续传）
progress = load_progress(data_dir)
# {'R-01': {'passed': True, 'detail': '...'}, 'R-02': {...}, ...}

# 格式化进度条
md = format_progress_markdown(data_dir)
# '**进度**：`████████░░░░░░░░░░░░` 16/24 通过（8 失败）'
```

---

### permission_checks — 权限检查函数集

**功能：** R-13~R-26 权限相关规则的检查函数。被 audit 引擎调用，无独立 CLI。

**Python API：**

```python
from skill_audit.permission_checks import (
    check_sensitive_access_declaration,    # R-13
    check_critical_write_declaration,      # R-14
    check_authorization_present,           # R-15
    check_permission_weight_explained,     # R-16
    check_progressive_loading_forced,      # R-17
)

# 每个函数接收统一签名
result = check_sensitive_access_declaration(
    filepath='SKILL.md',
    content=full_text,
    fm=frontmatter_dict,
    body=body_text,
    skill_dir='/path/to/skill'
)
# result = {'passed': bool, 'detail': str, 'fix': {...} (可选), 'skip': bool (可选)}
```


---

## 内部模块速查表

以下模块被 audit 引擎（`skill_audit`）内部调用，通常不需要直接 CLI 调用。
在排查审计故障或定制检查逻辑时按需查阅。

| 模块 | 所属包 | 职责 | 关键函数 |
|------|--------|------|----------|
| `artifact_checker.py` | skill_audit | R-11 产出物路径检查 + 修复 | `check_artifact_paths()`, `fix_external_data_dir()` |
| `data_dir_checker.py` | skill_audit | R-22 数据目录规范检查 + 修复 | `check_data_dir_compliance()`, `fix_data_dir_compliance()` |
| `structure_checker.py` | skill_audit | 技能目录结构完整性检查 | `check_structure()` |
| `frontmatter_checker.py` | skill_audit | Frontmatter 字段验证（R-01~R-26） | `check_frontmatter()` |
| `fix.py` | skill_audit | 统一修复分发（R-01~R-26） | `apply_fix()`, `list_fixable()` — 见 [skill_audit.fix](#skill_auditfix-统一修复工具) |
| `permission_checks.py` | skill_audit | R-13~R-26 权限检查函数 | 见 [permission_checks](#permission_checks-权限检查函数集) |
| `report_generator.py` | skill_audit | 审计报告生成（text/json/html） | `generate_report()` |
| `utils.py` | skill_audit | `parse_simple_yaml_frontmatter()` 等工具函数 | `parse_simple_yaml_frontmatter()` |
| `__init__.py` | skill_audit | 主入口（6 种模式） | `cmd_audit()`, `cmd_create()`, `cmd_update()`, `cmd_refactor()`, `cmd_bump()`, `cmd_rules()`, `cmd_create_template()` |
| `consistency_checker.py` | skill_audit | 一致性审查 | `check_consistency()`, `apply_consistency_fix()` |
| `structure_checker.py` | skill_audit | R-06~R-26 检查函数 | `body_check_*()` |
| `fix.py` | skill_audit | 自动修复分发 | `apply_fix()`, `dispatch_fix()` |
| `permission_checker.py` | — | 权限扫描 | `scan_permissions()` |
| `safe_io.py` | — | 原子写操作 | `safe_write()` |
| `skill_inspector.py` | — | 蓝皮书扫描 | `inspect_skill()` |
| `cleanup_manager.py` | — | 清理管理 | `start_session()`, `end_session()` |

### 调用关系

```
skill_audit
  ├─ creator / updater / migrator  (模式路由)
  └─ version_manager               (版本管理)
skill_audit
  ├─ audit_runner                  (编排25条规则)
  ├─ frontmatter_checker           (R-01~R-26)
  ├─ structure_checker             (R-07~R-26)
  ├─ permission_checks             (R-13~R-26)
  ├─ artifact_checker              (R-11)
  ├─ data_dir_checker              (R-22)
  ├─ fix.py                        (apply_fix分发)
  ├─ report_generator              (输出格式化)
  └─ utils.py                      (通用工具)
permission_checker                 (权限扫描)
progress_manager                   (进度追踪)
safe_io                            (基础设施)
```

## 脚本 CLI 使用参考
以下是 skill-standardization 下所有带命令行接口的脚本的使用说明，按照渐进式加载规范放入本章节，大模型可根据需要加载本章节参考。
---
### scripts/safe_io.py
**功能**: 提供原子化、备份安全的文件读写操作，是所有 .md 文件更新的唯一合规入口。
**子命令**: `read`、`write`、`patch-regex`、`patch-line`
**用法**:
```bash
python scripts/safe_io.py read --file <path> [--output <output_path>]
python scripts/safe_io.py write --file <path> --content "<内容>" [--no-backup]
python scripts/safe_io.py patch-regex --file <path> --pattern "<正则表达式>" --replacement "<替换内容>" [--flags 0] [--no-backup]
python scripts/safe_io.py patch-line --file <path> --line <行号> --content "<内容>" [--no-backup]
```
**参数说明**:
| 子命令 | 参数 | 说明 | 必需 | 默认值 |
|---------|------|------|------|--------|
| 通用 | `--file` | 目标文件路径 | 是 | — |
| `read` | `--output` | 输出文件路径（默认 stdout） | 否 | stdout |
| `write` | `--content` | 要写入的内容 | 是 | — |
| `write` | `--no-backup` | 跳过自动备份 | 否 | `False` |
| `patch-regex` | `--pattern` | 正则表达式模式 | 是 | — |
| `patch-regex` | `--replacement` | 替换字符串 | 是 | — |
| `patch-regex` | `--flags` | 正则标志位 | 否 | 0 |
| `patch-regex` | `--no-backup` | 跳过自动备份 | 否 | `False` |
| `patch-line` | `--line` | 目标行号 | 是 | — |
| `patch-line` | `--content` | 替换后的行内容 | 是 | — |
| `patch-line` | `--no-backup` | 跳过自动备份 | 否 | `False` |
**示例**:
```bash
python scripts/safe_io.py read --file SKILL.md
python scripts/safe_io.py write --file test.md --content "# 测试内容"
python scripts/safe_io.py patch-regex --file SKILL.md --pattern "version: .*" --replacement "version: 2.38.8"
python scripts/safe_io.py patch-line --file SKILL.md --line 5 --content "version: 2.38.8"
```
---
### scripts/permission_checker.py
**功能**: 扫描技能目录的权限风险，检查敏感访问、关键写入、授权说明等。
**用法**:
```bash
python scripts/permission_checker.py <skill_dir> [--verbose] [--output <report_path>]
```
**参数说明**:
| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `skill_dir` | 目标技能根目录路径 | 是 | — |
| `--verbose` / `-v` | 输出详细扫描日志 | 否 | `False` |
| `--output` / `-o` | 扫描报告输出路径（JSON 格式） | 否 | stdout |
**示例**:
```bash
python scripts/permission_checker.py .
python scripts/permission_checker.py . --verbose --output permission_report.json
```
---
### scripts/skill_audit/cleanup_manager.py（通过 refactor 流程调用）
**功能**: 管理改造清理过程，基于 manifest 标记的待删除文件执行清除，支持备份注册和批量处理。
**调用方式**: refactor 流程自动触发，无需手动调用。
---
### scripts/skill_audit/fix.py（通过 `audit --fix` 调用）
**功能**: 统一修复入口，根据审计结果自动修复可修复的规则违规（覆盖 R-01~R-26）。
**调用方式**: `python -m scripts.skill_audit audit <skill-dir> --fix`
或使用子命令: `python -m scripts.skill_audit fix <skill_dir> --key <fix_key>`
**用法**:
```bash
python -m scripts.skill_audit audit <skill-dir> --fix
python -m scripts.skill_audit fix <skill_dir> --key R-11
```
**参数说明**:
| 命令 | 参数 | 说明 | 必需 | 默认值 |
|---------|------|------|------|--------|
| `audit --fix` | `skill-dir` | 目标技能根目录路径 | 是 | — |
| `audit --fix` | `--fix` | 自动修复可修复规则 | 是 | off |
| `fix` | `skill_dir` | 目标技能根目录路径 | 是 | — |
| `fix` | `--key` | 要修复的 fix key | 是 | — |
| `fix` | `--dry-run` | 仅模拟不更新 | 否 | false |
---
### scripts/skill_audit/fix.py
**功能**: 规则级修复函数库，提供每个规则（R-01~R-26）的独立修复函数，供 `audit --fix` 或 `audit fix` 子命令调用。
**Python API 示例**:
```python
from skill_audit.fix import apply_fix, list_fixable_rules

fixable = list_fixable_rules()
apply_fix('.', 'R-11', violations=[{'file': 'scripts/foo.py', 'reason': '临时脚本'}])
apply_fix('.', 'R-13', sensitive_access=True)
```
---
### scripts/skill_audit/artifact_checker.py
**功能**: 检查产出物路径合规性（R-11），确保仅 SKILL.md、_meta.json、scripts/、references/ 出现在根目录。
**Python API 示例**:
```python
from skill_audit.artifact_checker import check_artifacts

result = check_artifacts('.')
# {'passed': True, 'violations': [], 'details': '...'}
```
---
### scripts/skill_audit/data_dir_checker.py
**功能**: 检查数据目录合规性（R-12），确保外部数据目录路径统一为 `.standardization/<skill>/`。
**Python API 示例**:
```python
from skill_audit.data_dir_checker import check_data_dir

result = check_data_dir('.')
# {'passed': True, 'issues': [], 'details': '...'}
```
---
