# semantic-split 版本更新日志

---

## v2.5.0（2026-05-23）

**改写类型：标准化改造 — SKILL.md 结构规范化 + 示例更新 + 路径修正**

### 变更内容

#### SKILL.md 结构规范化
- 章节重排为规范模板顺序：触发场景→核心能力→快速开始→主要流程→注意事项→脚本工具→参考文档
- 去掉标题中的版本号 `(Semantic Split v2.4)`，版本号仅在 frontmatter
- 「第一/二/三部分」改为标准章节名（语义拆分规则摘要、完整执行流程、触发场景→注意事项）
- 新增「注意事项」章节：双方案是内部推理、约束强度需上下文推断、锚定/反查不可跳过
- 触发场景从末尾移至第二个章节（核心能力之后）

#### examples.md 更新
- 新增示例 1：v2.4+ 增强格式（含约束标注🔴🟡⚪、5W2H维度、核心句、自我反查、隐式约束升级🟡🔴、双视角整合规划输出）
- 保留示例 2：v2.3 基础格式作为对照

#### 路径修正
- `json_schema.md` 第四节目录树：修正为 `skills/.standardization/semantic-split/data/`（铁律4）
- `automation_tasks.md` 第三节目录树：同上修正
- `loading_decision_tree.md` 两处路径：同上修正
- `changelog.md` 三处历史路径记录：同上修正
- `SKILL.md` 知识库路径说明：同上修正

### 标准化审查结果
- ERROR=0, PASS=11, SKIP=1(R-10)
- SKILL.md 行数=200（符合≤200行规范）

---

## v2.4.1（2026-05-23）

**改写类型：标准化改造 — SKILL.md 瘦身 + 渐进式MD体系完善**

### 变更内容

#### SKILL.md 主文件瘦身（315行 → 200行）
- 第一部分「语义拆分规则」详细内容迁移至 `references/split_rules.md`，主文件仅保留摘要表格
- 步骤4输出模板压缩（5W2H逐行展开改为单行格式）
- 步骤6加载提示和双视角推理描述精简
- 步骤1-2合并
- 触发条件精简
- 脚本工具表合并
- 参考文档表精简

#### 新增文件
- `references/split_rules.md` — 从SKILL.md第一部分迁移的完整语义拆分规则（划分块、诉求聚合、主语映射表、边界情况、5W2H提取规则）

#### 格式统一
- references/ 内部交叉引用统一为不带 `references/` 前缀
- SKILL.md 内引用统一带 `references/` 前缀
- `automation_tasks.md` 2处引用修正
- `planning_rules.md` 1处引用修正
- 参考文档表增加 `split_rules.md` 条目

### 标准化审查结果
- ERROR=0, WARN=0, PASS=11, SKIP=1(R-10)
- SKILL.md 行数=200（符合≤200行规范）

---

## v2.4.0（2026-05-23）

**改写类型：功能增强 — 5W2H维度提取 + 约束标注 + 双视角推理整合**

### 变更内容

#### 新增功能
- **步骤 2.5：任务类型识别与 5W2H 初始化** — 自动判断任务类型，按映射表填入 5W2H 默认值，预标注约束强度
- **步骤 3 增强：注意力锚定 + 5W2H 提取 + 约束标注** — 提取前强制执行锚定（[CRITICAL]/[CORE]/[ENTITY]/[EXAMPLE]/[RESISTANCE]），逐句增加 5W2H 维度和约束强度标注
- **步骤 4 增强：结构化输出含约束标注** — 诉求点增加 🔴🟡⚪ 标记，新增 5W2H 维度输出、阻力记录、核心句
- **步骤 4.5：自我反查** — 输出前强制执行硬约束遗漏/约束误判/举例干扰/5W2H 完整性四项反查
- **步骤 6 增强：双视角推理整合** — 模型思考时从聚焦+发散两个视角推理，整合为单一执行步骤输出，🌟标记发散增强步骤
- **工作包分解** — 聚焦式 WP 格式 + 探索式模块格式

#### 新增文件
- `references/task_type_defaults.md` — 5 种任务类型（制作PPT/填写周报/安排行程/写邮件/策划活动）的 5W2H 默认值映射表 + 通用默认值
- `references/constraint_annotation.md` — 约束强度定义（🔴🟡⚪）、自动识别规则、注意力锚定规则、自我反查、双方案处理差异、整合时约束处理规则

#### 文件改动
- `SKILL.md` — 版本号 2.3.0→2.4.0，核心能力表扩展（8项），步骤 2.5/3/4/4.5/6 增强，参考文档表更新
- `references/planning_rules.md` — 末尾追加第六节（双视角推理与整合规则）+ 第七节（约束遵循检查）
- `references/json_schema.md` — steps 子字段表增加 `constraint_level`/`source` 可选字段，示例 json 增加 `s3c` 发散增强步骤
- `_meta.json` — 版本号 2.3.0→2.4.0，description 更新，tags 增加 5W2H/约束标注

#### 未改动文件
- `references/loading_decision_tree.md` — 渐进加载逻辑不变
- `references/automation_tasks.md` — 定时任务逻辑不变
- `references/examples.md` — 示例格式不变
- `scripts/json_manager.py` — 脚本逻辑不变

### 标准化审查结果
- ERROR=0, WARN=0, PASS=11, SKIP=1(R-10)

---

## v2.3.0（2026-05-23）

**改写类型：产出物路径修正**

- DATA_DIR 路径修正（Path.home()/standardization → SKILL_DIR.parent/.standardization/semantic-split/data/）
- _meta.json 补充 data_dir 字段

---

**改写类型：skill-standardization 标准化改造（R-11 产出物迁移 + 结构补全）**

### 变更内容

#### R-11 产出物路径修正（铁律4）
- `data/capabilities/make_product_ppt_v1.json` 从技能目录迁移至 `skills/.standardization/semantic-split/data/capabilities/`
- `scripts/json_manager.py` DATA_DIR 路径常量更新：`SKILL_DIR / "data"` → `Path.home() / ".workbuddy" / "semantic-split" / "data"`
- 旧 `data/` 目录已删除

#### 交叉引用修复（9处）
- `references/automation_tasks.md`：4 处 `data/` 路径 + 目录树更新
- `references/loading_decision_tree.md`：2 处路径引用更新
- `references/json_schema.md`：3 处 CLI 示例路径 + 目录树更新

#### 结构补全
- 新增「快速开始」章节（含 scan/categorize/create/generalize 四个核心命令示例）
- 知识库路径说明：`skills/.standardization/semantic-split/data/`

#### 版本号同步
- SKILL.md `version:` `2.1.0` → `2.2.0`
- `_meta.json` `"version"` `2.1.0` → `2.2.0`

### 标准化审查结果
- ERROR=0, WARN=1, PASS=5（预修复：1E → 0E）

---

## v2.1.0（2026-05-22）

**改写类型：初始标准化**

- 初始版本，由 skill-standardization 引擎创建
