# 蓝皮书与审计流程规范

> 定义蓝皮书（Blueprint）、审计（Audit）、修复循环（Fix Loop）三者的关系与流程。
> 适用于 create / update / refactor 三种模式。

---

## 1. 蓝皮书的精确定义

**蓝皮书 = `inspect_skill()` 输出的技能目录结构快照。**

### 包含内容

| 字段 | 说明 | 来源 |
|------|------|------|
| `structure_tree` | tree 命令格式的目录树 | 现场扫描 |
| `root_files` | 根目录所有文件 | `os.listdir(skill_dir)` |
| `root_dirs` | 根目录所有子目录 | `os.listdir(skill_dir)` |
| `ref_files` | references/ 下 .md 文件 | `os.listdir(references/)` |
| `script_files` | scripts/ 下所有文件 | `os.walk(scripts/)` |
| `has_data_dir` | 是否存在 data/ | `os.path.isdir(data/)` |
| `has_output_dir` | 是否存在 output/ | `os.path.isdir(output/)` |
| `has_logs_dir` | 是否存在 logs/ | `os.path.isdir(logs/)` |
| `has_temp_dir` | 是否存在 temp/ | `os.path.isdir(temp/)` |
| SKILL.md 解析 | frontmatter + H2 章节 | 文件解析 |
| `_meta.json` | 元数据 | 文件解析 |
| `doc_code_gaps` | 文档与代码的函数签名差异 | 代码扫描 |

### 蓝皮书的合法用途（仅此两条）

1. **给 LLM 看** — 帮助 LLM 理解技能结构，确定更新范围
2. **给审计提供路径地图** — 审计知道该扫哪些目录（不做判断依据）

### 蓝皮书不参与审计判断

- 检查器**不得**从 `kw.get("blueprint")` 拿数据做审计判断（已删除）
- 审计判断**必须**用实时磁盘数据（`os.listdir` / `os.walk` / 读文件内容）
- `audit_skill()` 已删除 `blueprint` 参数（v2.75.0），`_audit_with_blueprint()` 简化为废弃别名

---

## 2. 三个模式的完整流程

### 2.1 创建（create）

```
1. 生成骨架（SKILL.md + _meta.json + references/ + scripts/ .gitkeep）
2. 全量审计（无蓝皮书——创建没有旧结构）
3. 输出报告 + 建议（不修复，不循环）
```

**特征**：无蓝皮书、无备份、无修复循环。

---

### 2.2 更新（update）— 范围明确的更新

```
用户输入："给 xxx 技能增加/更新/更新某个功能或部分"
  ↓
[步骤 1] 蓝皮书扫描
  - inspect_skill(skill_dir) 输出文本版蓝皮书
  - LLM 看蓝皮书理解技能结构
  ↓
[步骤 2] 更新声明（流程钩子 — 强制）
  - LLM 必须输出更新声明 JSON：
    {"changed_files": ["scripts/foo.py", "references/bar.md"], "description": "增加 --format 参数"}
  - 无更新声明 → 流程拦住
  ↓
[步骤 3] 针对性审计
  - 只跑跟 changed_files 相关的规则
  - audit_skill(skill_dir, filter_files=changed_files)
  - 爆出真问题列表（含 LLM 二次筛除）
  ↓
[步骤 4] 修复 + 细碎审计循环
  ┌─────────────────────────────────────────────┐
  │ LLM 修一批/一类/一个问题                      │
  │   ↓                                          │
  │ ★★★ 流程钩子（强制）★★★                       │
  │ LLM 必须声明修了哪些规则：                     │
  │   代码自动跑针对性审计（每次 LLM 修复后触发）：  │
  │   audit_skill(skill_dir)                       │
  │   还有 FAIL？→ 继续修                           │
  │   ↓                                          │
  │ 还有 FAIL？→ 继续修                           │
  │ 全部 PASS？→ 退出循环                         │
  └─────────────────────────────────────────────┘
  ↓
[步骤 5] 全量审计确认
  - audit_skill(skill_dir) 全量跑
  - 还有 FAIL？→ 回到步骤 4
  - 双 0 → 继续
  ↓
[步骤 6] 针对性一致性审查 + 修复
  - 只审 changed_files 涉及的文档-代码一致性
  - 修复文档描述匹配代码
  ↓
[步骤 7] 输出报告 → bump (PATCH)
```

---

### 2.3 改造（refactor）— 全量重构

```
用户输入："重构/标准化 xxx 技能"
  ↓
[步骤 1] 蓝皮书扫描
  - inspect_skill(skill_dir) 输出文本版蓝皮书
  - LLM 理解旧结构全貌
  ↓
[步骤 2] 备份
  - zip 到 .standardization/<skill>/backup/pre_refactor_<timestamp>.zip
  ↓
[步骤 3] 全量审计
  - audit_skill(skill_dir) 全量跑
  - 含 LLM 二次筛除，爆出真问题列表
  ↓
[步骤 4] 修复 + 细碎审计循环
  ┌─────────────────────────────────────────────┐
  │ LLM 修一批/一类/一个问题                      │
  │   ↓                                          │
  │ ★★★ 流程钩子（强制）★★★                       │
  │ LLM 必须声明修了哪些规则：                     │
  │   代码自动跑针对性审计（每次 LLM 修复后触发）：  │
  │   audit_skill(skill_dir)                       │
  │   还有 FAIL？→ 继续修                           │
  │   ↓                                          │
  │ 还有 FAIL？→ 继续修                           │
  │ 全部 PASS？→ 退出循环                         │
  └─────────────────────────────────────────────┘
  ↓
[步骤 5] 全量审计确认
  - audit_skill(skill_dir) 全量跑
  - 还有 FAIL？→ 回到步骤 4
  - 双 0 → 继续
  ↓
[步骤 6] 全量一致性审查 + 修复
  - 全量检查文档-代码一致性
  - 修复所有文档描述匹配代码
  ↓
[步骤 7] 输出报告 → bump (FEATURE) + cleanup
```

---

## 3. 关键机制设计

### 3.1 针对性审计 — `audit_skill()` 新增参数

```python
def audit_skill(skill_dir, filter_rules=None, filter_files=None, ...):
    """
    filter_rules: ["R-23", "R-26"] — 只跑指定规则
    filter_files: ["scripts/foo.py"] — 只跑跟这些文件相关的规则
    
    两个参数可同时使用（取交集）
    None = 不限（全量）
    """
```

每个检查器需要声明自己"关联哪些文件"和"关联哪些规则ID"，审计据此判断是否该跑。

### 3.2 细碎审计钩子（代码级强制）

```
触发时机：
  A. apply_fix() 返回后（自动修复完成）
  B. LLM 声明"手动修复完成"后（通过流程交互）

钩子行为：
  1. LLM 修复后重新审计
  2. 剩余问题继续循环修复
  3. 结果全部 PASS → 放行
  4. 还有 FAIL → 拦住，要求继续修

不依赖 LLM 自觉 — 钩子由 cmd_refactor / cmd_update 的代码流程控制
```

### 3.3 更新声明（更新模式专用）

```
触发时机：update 流程步骤 1（蓝皮书扫描后）

格式：
  {"changed_files": ["scripts/foo.py", "references/bar.md"], "description": "..."}

校验：
  - changed_files 中的路径必须在蓝皮书中有对应文件
  - 无更新声明 → 流程拒绝继续
```

### 3.4 一致性审查阶段

```
触发条件：双 0 确认后

范围：
  - refactor：全量（所有文件）
  - update：只审 changed_files 涉及的部分

检查内容：
  - 文档中描述的功能代码里是否存在
  - 代码中有的功能文档里是否写了
  - 参数签名是否一致
  - 示例是否过期
  - 目录树 vs 磁盘文件是否一致（双向）
```

---

## 4. 蓝皮书与审计的关系总表

| 场景 | 蓝皮书角色 | 审计数据源 | 备注 |
|------|-----------|-----------|------|
| 第一次全量审计 | 路径地图 | 实时磁盘 | 蓝皮书告诉审计"技能有哪些目录" |
| 细碎审计（循环中） | 已过期，不用 | 实时磁盘 | 审计自己扫，不依赖任何快照 |
| 全量审计确认（双0） | 已过期，不用 | 实时磁盘 | 同上 |
| 一致性审查 | 已过期，不用 | 实时磁盘 | 现场扫磁盘 vs 文档内容对比 |
| update 更新声明 | LLM 参考 | — | LLM 看蓝皮书确定 changed_files |

---

## 5. 代码改动清单

### 5.1 `skill_inspector.py` — 蓝皮书输出格式

- [x] 已支持 `output_format="dict"`（本次新增）

### 5.2 `skill_audit/__init__.py`

- [x] `audit_skill()` 新增 `filter_rules`、`filter_files` 参数
- [x] 每个检查器声明关联规则ID和关联文件
- [x] `_audit_with_blueprint()` 改为废弃别名（直接调 `audit_skill()`）
- [x] `cmd_refactor()` 重写：蓝皮书→备份→全量审计→细碎循环→全量确认→一致性审查→bump
- [x] `cmd_update()` 重写：蓝皮书→更新声明→针对性审计→细碎循环→全量确认→针对性一致性审查→bump
- [x] 细碎审计钩子（代码级强制，不依赖 LLM 自觉）
- [x] `audit_skill()` 删除 `blueprint` 参数
- [x] 所有 `_audit_with_blueprint()` 调用点改为直接调 `audit_skill()`
- [x] 新增 `_validate_changed_files()` 更新声明校验
- [x] 新增 `_run_audit_loop()` 修复循环通用实现（自动修复 + LLM 手动 + 细碎审计钩子 + 针对性审计）
- [x] `cmd_update()` 新增 `--changed-files` CLI 参数

- [x] `cmd_update()` 步骤2更新声明从空壳改为实际校验
- [x] refactor 一致性审查后增加修复循环（最多3轮重试）

### 5.3 `skill_audit/structure_checker.py`

- [x] 6 处 `kw.get("blueprint")` → 改为现场扫磁盘（`os.listdir` / `os.walk`）
- [x] 检查器声明关联文件列表（用于 filter_files 过滤）
- [x] 所有 blueprint 引用已清除

### 5.4 新增：一致性审查检查器

- [x] 文档-代码双向一致性检查（文档有代码没有 / 代码有文档没有）
- [x] 目录树 vs 磁盘文件双向对比
- [x] 规则编号范围过时检测（从 R-23 检查4 + R-25 C-16 迁移而来）
- [x] argparse flag 一致性（文档示例 vs 代码 add_argument）
- [x] data_dir 路径一致性（正文路径 vs frontmatter）
- [x] 函数签名一致性（骨架就绪）

### 5.5 其他

- [x] `creator.py` 中 `audit_skill()` 调用改为不传 blueprint
- [x] `audit_skill()` 签名删除 `blueprint` 参数
- [x] `_audit_with_blueprint()` 简化为废弃别名

---

## 6. 版本

当前版本：**v1.2** — 流程钩子代码级强制、更新声明实现、一致性审查增强、R-25 C-16 迁移
