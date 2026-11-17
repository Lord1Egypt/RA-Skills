# 使用指南 — skill-standardization v2

本指南提供 skill-standardization v2 六种执行模式的详细操作教程。

---

## 目录

1. [模式 R：readonly — 只读查询](#模式-rreadonly--只读查询)
2. [模式 A：audit — 审计/修复/分类](#模式-aaudit--审计修复分类)
3. [模式 C：create — 创建新 Skill](#模式-ccreate--创建新-skill)
4. [模式 U：update — 更新已有 Skill](#模式-uupdate--更新已有-skill)
5. [模式 F：refactor — 改造非标 Skill](#模式-frefactor--改造非标-skill)
6. [模式 B：bump — 版本号升级](#模式-bbump--版本号升级)
7. [LLM 二次筛除流程](#llm-二次筛除流程)
8. [审查后自动更新（fix.py）](#审查后自动更新-fixpy)
9. [安全增强功能](#安全增强功能)
10. [注意事项](#注意事项)

---

> **⚠️ 文件更新约束**：更新 `SKILL.md` 或 `references/*.md` 时，建议使用 Python 脚本原子写入（`open(tmp)+os.replace()`），避免编码损坏。更新后必须运行审计确认 0 ERROR 0 WARN。

---

## 总览：6 种模式

所有入口命令均为 `python -m scripts.skill_audit`，需传 `--mode` 匹配自检闸门输出。

| 门禁输出 | 入口命令 | 是否修改文件 | 流程长度 |
|----------|---------|------------|----------|
| `【模式=readonly】` | `rules` / `create-template` | ❌ 只读 | 1 步：输出 |
| `【模式=audit】` | `audit` (+ flags) | ⚠️ 取决于 `--fix` | 1 步：审计 |
| `【模式=create】` | `create` | ✅ 生成骨架 | 3 步：骨架→审计→报告 |
| `【模式=update】` | `update` | ✅ 有备份 | 9 步 |
| `【模式=refactor】` | `refactor` | ✅ 有备份 | 9 步 |
| `【模式=bump】` | `bump` | ✅ 只改版本号 | 含双0前置检查 |

门禁 + `--mode` 锁确保模式与命令匹配。不匹配则 `exit(1)` 拒绝。

---

## 模式 R：readonly — 只读查询

列出所有审查规则，或输出创建模板。**不修改任何文件。**

```bash
# 列出 R-01~R-26 规则
python -m scripts.skill_audit rules --confirmed --mode readonly

# 输出创建模板（供 LLM 创建技能时参考）
python -m scripts.skill_audit create-template --confirmed --mode readonly

# JSON 格式输出
python -m scripts.skill_audit create-template --json --confirmed --mode readonly
```

---

## 模式 A：audit — 审计/修复/分类

audit 有四种模式，靠 flags 区分：

### 纯查看
```bash
python -m scripts.skill_audit audit <skill-dir> --confirmed --mode audit
```
输出 R-01~R-26 全量报告，exit(0)。

### 自动修复
```bash
python -m scripts.skill_audit audit <skill-dir> --fix --confirmed --mode audit
```
按 fix key 粒度分离修复路径：fix key 不在 _llm_only_fix_keys 的条目 auto-fix；在 _llm_only_fix_keys 中或无 fix key 的条目输出 LLM 手动指引。修完后重新审计确认。

### 验证双0
```bash
python -m scripts.skill_audit audit <skill-dir> --verify --confirmed --mode audit
```
过滤已通过 `--classify` 标记的误报，展示剩余真问题。
有真问题则 exit(1) 阻断，无则 exit(0)。

### 标记误报
```bash
# 先获取 ID（从 --verify 输出获取）
python -m scripts.skill_audit audit <skill-dir> --verify --confirmed --mode audit

# 标记指定 ID 为误报（须带 --category）
python -m scripts.skill_audit audit <skill-dir> --classify 42,55,67 --category engine_mistake --reason "BOM字符" --confirmed --mode audit

# 取消误报标记
python -m scripts.skill_audit audit <skill-dir> --no-fp 42,55 --confirmed --mode audit

# 一致性审查误报 ID 格式: C-missing_doc_ref, C-stale_doc_ref
python -m scripts.skill_audit audit <skill-dir> --classify C-missing_doc_ref --category engine_mistake --reason "概念图路径被当真实文件" --confirmed --mode audit
```

---

## 模式 C：create — 创建新 Skill

### 基础用法
```bash
python -m scripts.skill_audit create <skill-dir> --desc "技能描述" --confirmed --mode create
```

### 流程
```
[1/3] 生成标准骨架 → [2/3] 全量审计 → [3/3] 创建总结
```

### 产出物结构
```
<skill-dir>/
├── SKILL.md              # 主文件（含占位符模板）
├── _meta.json            # 元数据（七字段）
├── references/
│   ├── LICENSE.md        # MIT 许可证模板
│   ├── permissions.md    # 权限说明骨架
│   ├── changelog.md      # 更新日志骨架
│   ├── examples.md       # 输出示例骨架
│   ├── faq.md            # FAQ 骨架
│   └── antipatterns.md   # 反模式骨架
└── scripts/.gitkeep
```

### create 后的后续步骤
1. **更新 SKILL.md**：填充触发词、核心功能、使用方式等章节
2. **补充脚本**：在 `scripts/` 中添加实际功能代码
3. **运行 update**：`python -m scripts.skill_audit update <skill-dir> --confirmed --mode update`

---

## 模式 U：update — 更新已有 Skill

范围明确的更新流程，适合增删改特定功能时使用。

### 基础用法
```bash
# 全量审计（未指定 changed-files 时）
python -m scripts.skill_audit update <skill-dir> --confirmed --mode update

# 针对性审计（指定变更文件）
python -m scripts.skill_audit update <skill-dir> --changed-files scripts/foo.py references/bar.md --confirmed --mode update
```

### 完整流程（9 步）
```
[1/9] 蓝皮书扫描 → 输出技能目录结构快照
[2/9] cleanup session + 备份 → pre_update_<timestamp>.zip
[3/9] 变更声明 → 校验 changed-files 路径有效性
[4/9] 针对性/全量审计 → _run_audit_loop()
        ├─ ★ 前置 LLM 二次筛阻断点（首次进入，无 --classify 数据时阻断）
        ├─ auto-fix（按 fix key 粒度过滤 _llm_only_fix_keys 后修复）
        └─ LLM manual 指引输出
[5/9] LLM 剩余项检查
[6/9] 全量审计确认（双 0 验证）
[7/9] 针对性一致性审查 + 修复循环
        ├─ 自有二次筛（读取 --classify 中的 C-{type} ID）
        ├─ auto-fix（outdated_rule_ref 等）
        └─ LLM 语义对比（流程描述 vs 代码执行）
[8/9] bump (fix → PATCH)
[9/9] cleanup 清理
```

### --continue（仅 refactor 支持）
LLM 标记误报后继续：
```bash
python -m scripts.skill_audit refactor <skill-dir> --continue --confirmed --mode refactor
```

---

## 模式 F：refactor — 改造非标 Skill

全流程标准化改造，最完整的流程。

### 基础用法
```bash
python -m scripts.skill_audit refactor <skill-dir> --confirmed --mode refactor
```

### 完整流程（9 步）
```
[1/9] 蓝皮书扫描
[2/9] cleanup session + 备份 → pre_refactor_<timestamp>.zip
[3/9] 全量审计
[4/9] _run_audit_loop()（含二次筛阻断点、auto-fix、LLM manual）
[5/9] LLM 剩余项检查
[6/9] 全量审计确认（双 0 验证）
[7/9] 全量一致性审查 + 修复循环
[8/9] bump (feature → MINOR)
[9/9] cleanup 清理
```

### --continue
```bash
python -m scripts.skill_audit refactor <skill-dir> --continue --confirmed --mode refactor
```

---

## 模式 B：bump — 版本号升级

版本号三端同步（SKILL.md + _meta.json + changelog）。**必须在双 0 确认后执行**。

```bash
python -m scripts.skill_audit bump <skill-dir> --desc "变更说明" --confirmed --mode bump
```

`cmd_refactor` 和 `cmd_update` 内部会在最后一步自动调 `cmd_bump`，无需手动调用。

---

## LLM 二次筛除流程

前置 LLM 二次筛除是 `refactor` 和 `update` 模式的强制步骤，位于全量审计之后、修复循环之前。

### 阻断点触发条件
- 首次进入 `_run_audit_loop()`
- 有 FAIL 项
- 无 `--classify` 数据（`.verify_fp.json` 为空或不存在）
- 未传 `--continue`

### 阻断输出
```
⏸  ★ 前置 LLM 二次筛除（阻断点）
原始审计发现 N 项 FAIL，需要 LLM 确认真问题 vs 误报

步骤 1: 查看 FAIL 详情
  python -m scripts.skill_audit audit <skill-dir> --verify --mode refactor

步骤 2: 对确认为误报的项执行 --classify（须带 --category）
  python -m scripts.skill_audit audit <skill-dir> --classify ID1,ID2 --category engine_mistake --reason "..." --mode refactor

步骤 3: 重新执行 refactor --continue
  python -m scripts.skill_audit refactor <skill-dir> --continue --confirmed --mode refactor
```

### 一致性审查阻断
一致性审查也有自己的前置二次筛阻断点，读取 `--classify` 中的 `C-{type}` 格式 ID。
步骤与主审计相同，但在 `--classify` 时使用 `C-missing_doc_ref` 等 ID 格式。

---

## 审查后自动更新（fix.py）

审计输出 WARN/ERROR 后，可直接调用 `scripts/skill_audit/fix.py` 中的修复函数自动修复，无需手写修复脚本。

### 用法

```bash
# 方式一：在 skill-standardization 目录下调用
cd ~/workbuddy/skills/skill-standardization
python -c "
from scripts.skill_audit.fix import apply_fix
# 修复单条规则
apply_fix('~/workbuddy/skills/<skill-dir>', 'R-07')
# 修复多条规则
apply_fix('~/workbuddy/skills/<skill-dir>', 'R-07', 'R-18', 'R-19')
"
```

### 全部修复函数一览

| 函数名 | 对应规则 | 说明 |
|---------|---------|------|
| `fix_name(skill_dir, value)` | R-01 | 修复 name 字段 |
| `fix_description(skill_dir, value)` | R-04 | 修复 description 字段 |
| `fix_version(skill_dir, value)` | R-03 | 修复 version 字段 |
| `fix_author(skill_dir, value)` | R-02 | 修复 author 字段 |
| `fix_h1(skill_dir)` | R-06 | 删除正文一级标题 |
| `fix_section_trigger(skill_dir)` | R-07 | 添加触发条件章节 |
| `fix_section_core(skill_dir)` | R-08 | 添加核心能力章节 |
| `fix_section_workflow(skill_dir)` | R-09 | 添加工作流程章节 |
| `fix_progressive_loading(skill_dir)` | R-21 | 添加渐进式加载模板句 |
| `fix_antipattern_progressive(skill_dir)` | R-18 | 创建/更新 references/antipatterns.md |
| `fix_faq_progressive(skill_dir)` | R-19 | 创建/更新 references/faq.md |
| `fix_writing_standards(skill_dir)` | R-20 | 统一术语（配置/更新/删除） |
| `fix_data_dir_compliance(skill_dir)` | R-22 | 添加 data_dir 声明 |
| `fix_doc_code_consistency(skill_dir)` | R-23 | 修复文档-代码一致性 |
| `fix_artifact_paths(skill_dir)` | R-11 | 修复产出物路径 |
| `fix_external_data_dir(skill_dir)` | R-12 | 修复外部数据目录 |
| `fix_sensitive_access(skill_dir)` | R-13 | 添加敏感信息访问声明 |
| `fix_critical_write(skill_dir)` | R-14 | 添加关键位置写入声明 |
| `fix_create_permissions_md(skill_dir)` | R-15 | 创建 references/permissions.md |
| `fix_permission_weight(skill_dir)` | R-16 | 添加权限权重说明 |

---

## 安全增强功能

> 本 skill 在创建/更新/改造其他 skill 时，会自动进行权限检查和授权管理。

### 权限检查流程

`skill-standardization` 在 `update`/`refactor` 模式下会自动调用 `permission_checker.py` 扫描目标 skill 的脚本，计算权限权重，生成风险报告。

```
-m scripts.skill_audit update <skill-dir>
  ↓
调用 permission_checker.py 扫描脚本
  ↓
计算权限权重（敏感信息 40% + 关键位置 30% + 网络 20% + 删除 10%）
  ↓
生成 JSON 报告 → 打印到终端
  ↓
如发现中高风险操作，提示用户审批
```

### R-13~R-26 规则说明

| 规则 | 严重度 | 检查内容 |
|------|---------|----------|
| R-13 | ERROR | 敏感信息访问声明 |
| R-14 | ERROR | 关键位置写入声明 |
| R-15 | ERROR | 高权限操作风险说明 |
| R-16 | WARN | 权限权重说明 |
| R-17 | ERROR | 渐进加载引用 |

---

## 注意事项

1. **所有入口命令必须传 `--mode`**，与自检闸门输出的模式一致
2. **`--continue` 跳过前置 LLM 二次筛阻断点**，仅用于 LLM 已标记误报后继续
3. **WARN 是真问题**，不是样式建议，不存在"可跳过"类别
4. **版本号三端一致**：更新后同步 `SKILL.md` / `_meta.json` / `changelog.md`
5. **审查报告必须用 `present_files` 展示**，不得默认用户自己找文件
