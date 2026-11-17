# CHANGELOG - MBA/学术论文多Agent协作工作流

所有重要更新都会记录在此文件。

## [v1.7.3] - 2026-06-19

### P0 修复

- **分页逻辑修正**：每章标题前分页（原为标题后分页导致空页），首章跳过
- **审核报告匹配增强**：改用 glob 通配匹配 + 结构化评分字段优先，不再依赖 emoji 硬编码
- **Verification Loop 真实校验**：新增字体/字号/行距/三线表边框/加粗残留/参考文献分编 6 项 Word 格式实质检查
- **空壳校验填补**：`check_table_format` 和 `check_table_caption_position` 从永远 `return True` 改为真实列数一致性和表标题位置检测
- **文件名泛化**：`*report*.md` 收窄为中文 `*报告*.md` + 大小写补充，`_find_review_report` Level 3 加论文关键词过滤
- **`_check_report_passed` 优先级重排**：综合评级 → 结构化评分 → emoji 回退，🔴 阈值从 5 放宽到 8
- **`_copy_proposal_cover` 锚点式匹配**：从硬编码"研究背景与研究问题"改为多锚点正则（第X章/1./研究背景/摘要等）
- **去重格式校验**：`md2docx_strict.py` 移除 `validate_md_format()`，统一由 `loop_self_check.py` 负责
- **硬编码参数化**：`min_lines`/`min_citations` 改为常量配置
- **代码风格统一**：8 个内部函数统一下划线 `_` 前缀

### Loop 架构落地

- **新增 `scripts/orchestrator.py`**：决策引擎 + 审核 Loop 自动重审 + Phase 完成自动校验
- **增强 `scripts/state_manager.py`**：新增 `parse_p0_from_report`、`set_hil_pause`、`clear_hil_pause`、`next_phase_name` 等 6 个方法
- **新增 `scripts/tests/`**：25 个单元测试覆盖 state_manager/loop_self_check/md2docx_strict
- **SKILL.md 精简**：1142 行 → 253 行（-78%），新增 Orchestrator 生命周期管理与 HIL 节点表

### 依赖变更

- `install.sh`：`pip install` → `python3 -m pip install --user python-docx`

## [v1.7] - 2026-06-17

### Loop Agent 架构（新增）

- **Orchestrator Loop**：每 Phase 完成后自动判断下一步，取代手动 trigger 模式
- **Phase 内部自检 Loop**：Observe → Think → Act → Verify 四步循环
- **审核 Loop**：Phase 3.5 → 修订 → 自动重审 → 连续 2 轮无新 P0 → 通过
- **Guardrails 校验**：10 项自动化规范检查（章节完整性/字数/引用/三线表/加粗等）
- **Verification Loop**：Word 输出后自动校验格式
- **Human-in-the-loop 检查点**：4 个强制人工确认节点

### 新增文件

- `scripts/loop_self_check.py`：Guardrails 自动化校验脚本（10 项校验 + JSON 输出）
- `references/checklist.md`：学术规范人工对照清单
- `references/loop-design.md`：Loop 设计原理说明文档

### 规则型 vs 审核型分工

- 脚本已覆盖的规范（字体/行距/标题层级/三线表），Agent 不再重复检查
- Agent 专注于脚本无法处理的事项（摘要字数/逻辑链/数据可信度/学术创新性）

---

## [v1.6] - 2026-06-02

### 新增功能

- **Phase 5.1 可选去AI味**：新增 HumanizerAgent，调用 humanize-chinese skill 执行学术风格降重，支持 CLI 脚本批量处理 + 差异报告
- **Phase 5.2 Word生成**：拆分独立步骤，支持生成两份Word（原版 + 润色后版）
- **前置检测机制**：去AI味前自动检测 humanize-chinese skill 是否安装，未安装则提示用户确认后自动安装
- **Phase 2 执行前检查表**：每次启动 Phase 2 前强制确认，包括 Phase 1 七项清单、章节×版本对照表、完成判定标准
- **章节×版本对照表**：枚举每个章节的 Executor（版本O）和 Hermes（版本H）要求，明确「必须」spawn，不可遗漏
- **Phase 2 强制检索要求**：新增5项强制检索检查项（PESTEL分析前/五力模型前/战略理论前/引用来源/检索记录≥3次），不满足则打回补充
- **Phase 2 完成判定标准**：版本O文件6个+版本H文件4个全部存在，ls验证，缺一则禁止进入 Phase 2.5
- **正文目录章节禁止规则**：写作规范新增，明确禁止在正文章节内自建「目录」章节
- **md2docx_strict.py 审核报告模糊匹配**：支持 `审核报告*.md` 命名规范模糊匹配（Level 1精确/Level 2模糊/Level 3候选列表）

### 移除功能

- **移除邮件发送流程**：Phase 5.2 改为仅生成Word并告知存储位置（`~/.openclaw/workspace/`）
- **移除联系方式必填**：Phase 1 确认清单去掉联系方式（微信/飞书ID）要求，去AI味后由用户自行取用文件
- **删除 Phase 5.5 成果发送**：整节移除，减少不必要的流程节点

### 架构升级

- **Agent 角色体系重构**：Orchestrator（调度）/ Executor（H-generator执行）/ Reviewer（规则型审核）/ DeepReviewer（学术深度评审）/ Integrator（整合方案）/ WordAgent（Word输出）/ HumanizerAgent（去AI味）七类专职分离
- **Agent 设计原则**：职责单一化，调度者不执行，执行者不调度；职责边界清晰
- **Phase 3.5 固定节点**：Phase 3 完成即触发，不得跳过，作为固定流程节点
- **Phase 3.5 分级标准**：P0（致命）/ P1（严重）/ P2（建议），审核报告结构化分级

### 修复问题

- **Phase 2 章节遗漏问题**：通过章节×版本对照表强制要求每个 ✅ 都是独立 spawn，防止核心章节（3/4/5/6）遗漏版本O或版本H
- **正文目录章节问题**：新增写作规范禁止正文内自建目录章节

---

## [v1.5] - 2026-06-01

### 新增功能

- **md2docx_strict.py 合规脚本**：严格按MBA论文格式规范转换（分页符/三线表/加粗过滤/标题层级/行距/中英文字体）
- **Phase 5 Word输出流程**：Review Agent终审 → 格式自检 → md2docx_strict.py → 发送，三步缺一不可

### 修复问题

- **Word格式问题**：分页符、标题层级、行距、加粗过滤、中英文参考文献格式
- **审核报告命名规范**：统一为 `审核报告_{论文题目}_Phase{N}_{版本}.md`

---

## [v1.0] - 2026-05-31

### 首次发布

- 多Agent协作工作流（Phase 1-5）
- 双版本起草机制（版本H + 版本O）
- Phase 3 审核（7个维度）
- Phase 4 整合方案
- md2docx 脚本（基础版）
