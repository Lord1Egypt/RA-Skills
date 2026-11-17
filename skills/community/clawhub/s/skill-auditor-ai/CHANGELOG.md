# Changelog

All notable changes to this skill will be documented in this file.

## [2.0.1] - 2026-07-16

### Fixed
- **D-M3 / T-AST03 / T-AST04 / P-C3 同源修复**：SKILL.md frontmatter 新增 `metadata.openclaw` 段（skillKey/emoji/homepage/os/requires/primaryEnv/envVars/always），消除 v2.0.0 自举审计发现的"声明-行为不一致"问题
- **plugin.json permissions.filesystem 声明扩展**：`read`/`write` 追加 `<audited-skill-dir>/` 占位符，完整覆盖 Phase 4.5 整改模式声明的"Edit/Write 修改被审计 Skill 文件"行为（原 v2.0.0 只声明 .audit-report.md，与整改模式行为不一致）
- **T-AST10 跨平台复用声明**：metadata.openclaw.os 声明 `["windows", "macos", "linux"]`

### Design Note
- **T-LT Lethal Trifecta 自检结论**：skill-auditor 满足 2/3 要素（T-LT2 暴露不可信内容：被审计 Skill 是外部输入 + T-LT3 对外通信：WebFetch SkillHub API），不满足 T-LT1 访问私有数据。2/3 不构成 Lethal Trifecta，作为审计类技能的固有特性记录。未来如添加读取用户凭证功能（如审计凭证管理类技能时检查凭证格式），需重新评估是否触发 3/3 红线。

### Self-Audit
- 执行 v2.0.0 自举审计（用 v2.0.0 新增的 4 个检查项系列审计 skill-auditor 自身）
- 发现 1 个 Important（D-M3 / T-AST03 / T-AST04 / P-C3 同源声明-行为不一致）+ 1 个 Minor（T-AST10）+ 1 个 FYI（T-LT 2/3）
- 本版本修复 Important + Minor，FYI 记录到本条目作为设计说明
- 自审报告保存到 .audit-report.md（.gitignore 已排除）

## [2.0.0] - 2026-07-16

### Design Principle
v2.0.0 是 skill-auditor 的重大升级，基于对业界主流 Skill 平台开源仓库和 OWASP Agentic Skills Top 10 安全框架的深度研究，将审计能力从"基础 5 层扫描"升级为"平台级对齐审计"，并新增 Skill 撰写指导能力。

### Added — T 维度对齐 OWASP AST10
- 新增 T-AST 系列：AST01 恶意技能 / AST02 供应链 / AST03 过度授权 / AST04 元数据不安全 / AST05 不安全反序列化 / AST06 隔离薄弱 / AST07 更新漂移 / AST10 跨平台复用（8 个检查项）
- 新增 T-LT 系列：Lethal Trifecta 红线检查（三要素同时满足 = Critical：访问私有数据 + 暴露不可信内容 + 对外通信）
- 审计覆盖面从 AST10 的 3/10 提升到 8/10

### Added — D 维度声明-行为一致性
- 新增 D-M1：frontmatter env 声明 vs 实际环境变量引用
- 新增 D-M2：frontmatter bins 声明 vs 实际 CLI 调用
- 新增 D-M3：frontmatter metadata.openclaw 完整性
- 解决 v1.2.1 被 SkillSpector 报 6 个 finding 的根因（声明-行为不一致）

### Added — P 维度 Coherence 审计
- 新增 P-C1：Name-Summary Coherence（name 与 description 对齐）
- 新增 P-C2：Summary-Behavior Coherence（description 覆盖实际行为）
- 新增 P-C3：Metadata-Behavior Coherence（frontmatter 声明与代码行为一致）
- 新增 P-C4：Power-Proportionality（权力与用途成比例）

### Added — 双维度评分体系
- 新增 Risk Level：Low / Medium / High（基于技能声明的权力评估）
- 新增 Audit Status：Pass / Review / Warn / Fail（基于审计结果评估）
- 新增 Risk-Status 矩阵：High Risk + Pass = 合理（权力大但已披露且比例适当）

### Added — Skill 撰写指导能力
- 新建 references/skill-authoring-guide.md（486 行）：5 大原则 + frontmatter 规范 + description 公式 + 权力-风险自评 + 6 大反模式 + 10 项发布前自检清单 + 平台规范要点
- 审计发现问题时可引用指南章节提供改进建议
- 也可作为开发者独立撰写 Skill 的参考指南

### Changed
- audit-dimensions.md：T 维度拆分为 T1-T14 基础 + T-AST 系列 + T-LT 系列
- audit-dimensions.md：D 维度新增 D-M 系列段
- audit-dimensions.md：P 维度新增 P-C 系列段
- audit-dimensions.md：评分计算段新增双维度评分
- report-template.md：综合评分段新增双维度评分表
- SKILL.md：维度概览标注新增项 / 评分标准新增双维度 / References 新增 skill-authoring-guide.md

## [1.2.1] - 2026-07-15

### Fixed
- **安全修复**：嫁接清洗触发词不再跳过确认点 O。所有触发词（含"嫁接清洗"/"清洗嫁接痕迹"）都必须经过确认点 O 用户授权后才能执行 Edit 操作（修复 SkillSpector Finding #4/#6：Missing User Warnings + Intent-Code Divergence）
- originality-check.md Phase O-4 段追加前置条件说明：未授权 = 只输出清单，不修改任何文件
- originality-check.md 主动触发模式表追加安全约束：任何触发词都不能绕过确认点 O

### Changed
- README.md 用户须知段优化：明确"本技能不执行发布，仅提供发布建议由用户手动执行"，消除"不负责发布"与"用户授权后可发布"的措辞矛盾（修复 SkillSpector Finding #1/#2：Description-Behavior Mismatch + Intent-Code Divergence）
- README.md 用户须知段补充原创度清洗子模式（A2）的授权说明（修复 SkillSpector Finding #3）
- README.en.md 同步以上变更

### SkillSpector Findings 评估
- Finding #1/#2（发布职责矛盾）：过度解读，但措辞优化可降低误判
- Finding #3（审计却改文件）：合理担忧，已通过强化授权说明解决
- Finding #4/#6（嫁接清洗跳过确认点）：**确实有问题，已修复** ✅
- Finding #5（触发词太宽泛）：过度解读，不改（审计类技能固有特性）

## [1.2.0] - 2026-07-14

### Added
- D 维度新增 D-O1~O7 嫁接痕迹检查项（7 类：直接继承声明/Do NOT 指向具体技能名/三角分工定位/发布交接措辞/示例点名其他技能/CHANGELOG 历史痕迹/场景描述点名）
- 原创度审计专项触发词：「原创度审计」/「嫁接清洗」/「清洗嫁接痕迹」
- 整改模式新增 A1/A2/A3 子模式：A1 标准整改 / A2 原创度优化（仅清洗嫁接痕迹）/ A3 两者都做
- A2 子模式含 6 阶段流程：扫描 → 分类标记 → 【确认点 O】 → 执行清洗 → 7 项验证 → 回归报告
- 新增 references/originality-check.md（7 类痕迹识别模式 + 清洗策略表 + 7 项验证清单 + 主动触发模式 + 评分影响 + 清洗边界 + 常见误区）
- 新增示例4：原创度审计 + 嫁接清洗（A2 子模式完整流程演示）

### Changed
- D 维度概览追加"嫁接痕迹(D-O1~O7)"检查项
- 触发词段合并原创度专项触发词到主触发词列表
- 规则段合并网络降级+回归前提（规则6），精简表述
- 示例1/2 压缩空行（保持语义不变）

### Design Principle
- 核心判断铁律：能用「场景描述」替代「具体技能名」就替代，不能替代的（自引用/自身触发词）保留
- 清洗只改"措辞"，不改"语义"
- L1 跳过 D-O 检查（原型阶段允许快速派生），L2 检查 Important 类，L3 全部检查

## [1.1.0] - 2026-07-14

### Added
- 三级成熟度模型（L1原型 / L2迭代 / L3发布），按成熟度确定审计范围和严格度
- 4 个用户确认点（成熟度确认 / 报告后选择 / 整改后选择 / 发布确认）
- 整改模式（用户授权后帮修复 P0/P1/P2 问题，最小化改动）
- 严格发布门槛：绝不自动发布，必须用户在确认点4明确选"是，发布"后才提供发布建议
- 成熟度覆盖：用户可强制指定等级
- 新增 references/maturity-model.md（三级成熟度详细模型）
- 各维度检查项标注适用等级（L1/L2/L3）

### Changed
- 审计范围按成熟度动态调整（L1: 3项精简 / L2: 6维度 / L3: 全量8维度）
- 严格度按成熟度分级（L1: 只报Critical / L2: Critical必修+Important建议 / L3: Critical+Important必修）
- L1/L2 阶段不显示发布选项

## [1.0.0] - 2026-07-14

### Added
- 初始版本：8 维度深度审计（S/T/A/E/C/P/D/Q）
- 4 种入口模式：全量/单维度/批量/回归
- 标准化审计报告（严重性分级 + 修复建议 + 优先级）
- 回归审计机制（前后差异对比）
- 独立审计定位：专注深度审计+整改+回归，不负责创建或发布
- 5 个 references 文件：audit-dimensions / security-scan / benchmarking / report-template / regression
