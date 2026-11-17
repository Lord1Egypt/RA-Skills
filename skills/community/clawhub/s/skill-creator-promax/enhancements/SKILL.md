## 特殊增强能力 / Special Enhancements

**根据 Skill 类型自动增强，不使用统一模板硬套。**
**Auto-enhance based on Skill type. Never force-fit a single template.**

必须根据不同类型补充不同维度的能力 / Must supplement different dimensions based on different Skill types:

### 开发类 Skill / Development Skills

自动增强 / Auto-enhance:

- 工程实践 / 开发 workflow / 团队协作
- 风险识别 / debug 策略 / CI/CD
- API 流程 / 权限体系 / 状态管理 / 组件复用

**具体方法论 / Methodology：**
- 必须增加：错误处理策略（分类错误场景+降级方案）、测试方案建议（单元/集成/E2E 覆盖建议）、API 设计规范（请求/响应格式、版本策略、限流处理）
- 推荐增加：依赖管理策略、环境配置规范、日志与监控方案

**重点 / Focus:** "开发者快速进入真实开发状态。" / "Help developers reach real dev state fast."

### UI / 设计类 Skill / UI / Design Skills

自动增强 / Auto-enhance:

- 页面结构分析 / 布局拆解 / 组件层级推断
- 响应式策略 / design system / 交互状态识别
- 可复用组件识别 / 页面骨架生成

**具体方法论 / Methodology：**
- 必须增加：设计 Token 规范（颜色/间距/字号系统化映射）、无障碍合规检查（WCAG 2.1 AA 关键规则）、组件状态矩阵（loading/empty/error/disabled 等边界态）
- 推荐增加：主题切换策略、性能优化方案（懒加载/虚拟滚动）

**重点 / Focus:** "快速完成高质量 UI 实现。" / "Quickly complete high-quality UI implementation."

### 文档类 Skill / Documentation Skills

自动增强 / Auto-enhance:

- 信息结构设计 / 摘要能力 / 分阶段输出
- 可读性优化 / 重点提炼 / 推荐阅读顺序

**具体方法论 / Methodology：**
- 必须增加：信息层级模板（TL;DR → 概述 → 详细 → 参考）、受众适配策略（按角色调整深度和术语）、版本变更标注规范
- 推荐增加：交叉引用机制、内容 freshness 检查规则

**重点 / Focus:** "降低阅读成本，提高信息获取效率。" / "Reduce reading cost, improve information efficiency."

### 架构类 Skill / Architecture Skills

自动增强 / Auto-enhance:

- 模块关系 / 分层 / 数据流 / 调用链
- 服务边界 / 微服务关系 / monorepo / 技术债识别

**具体方法论 / Methodology：**
- 必须增加：依赖方向约束规则（禁止循环依赖/跨层直连）、变更影响半径评估方法（1 行改动→影响链路→回归范围）、架构决策记录模板（ADR：上下文→决策→后果）
- 推荐增加：演进策略（渐进式重构路径）、技术债量化与优先级排序

**重点 / Focus:** "快速建立系统级认知。" / "Quickly build system-level understanding."

### 测试类 Skill / Testing Skills

自动增强 / Auto-enhance:

- 测试策略 / 边界 case / mock 策略
- fixture 设计 / 覆盖建议

**具体方法论 / Methodology：**
- 必须增加：测试分层策略（单元→集成→E2E 比例建议，如 70/20/10）、边界 case 生成方法（等价类划分+边界值分析）、mock/tape 策略选择（何时 mock、何时录制真实响应）
- 推荐增加：测试命名规范、flaky test 检测与隔离方案

### Code Review 类 Skill / Code Review Skills

自动增强 / Auto-enhance:

- 风险识别 / 性能 / 安全 / 可维护性
- anti-pattern 检测 / 潜在 bug / 边界条件

**具体方法论 / Methodology：**
- 必须增加：回归风险分级方法（按影响范围+发生概率矩阵）、安全检查清单（注入/XSS/权限泄漏/敏感数据暴露）、可维护性评估维度（圈复杂度/耦合度/命名清晰度）
- 推荐增加：团队规范一致性检查、性能退化检测规则

### AI Workflow 类 Skill / AI Workflow Skills

自动增强 / Auto-enhance:

- Agent 边界 / Prompt chaining / Context 管理
- 多 Agent 协作 / retry / fallback / hallucination reduction

**具体方法论 / Methodology：**
- 必须增加：Context 预算分配策略（总 token 限→各环节分配→压缩规则）、hallucination 检测与缓解（结构化输出校验/事实核查步骤/fallback 话术）、多 Agent 交接协议（输入/输出 schema + 状态传递格式）
- 推荐增加：成本优化策略（模型分级调用/缓存策略）、错误传播阻断机制

### 产品 / 需求类 Skill / PM / Product Skills

自动增强 / Auto-enhance:

- 需求拆解 / 用户场景 / 边界识别 / 技术影响
- PRD 结构化 / 验收标准 / MVP 分析

**具体方法论 / Methodology：**
- 必须增加：需求歧义检测清单（模糊量词/未定义术语/隐含假设）、MVP 边界划定方法（核心路径→必要功能→可延后功能三级分类）、验收标准编写模板（Given-When-Then 格式）
- 推荐增加：技术影响评估框架、需求优先级矩阵（影响力×实现成本）

### 数据 / 分析类 Skill / Data / Analytics Skills

自动增强 / Auto-enhance:

- 指标体系 / 数据流 / 埋点 / dashboard
- 数据质量风险 / 实验设计 / 分析维度

**具体方法论 / Methodology：**
- 必须增加：指标分层体系（北极星→核心指标→辅助指标→过程指标）、数据质量检查规则（完整性/一致性/时效性/准确性）、A/B 实验设计规范（样本量估算+显著性标准+SOP）
- 推荐增加：埋点校验方案、数据血缘追踪规则

---

## 自动增强原则 / Enhancement Principles

增强能力必须 / Enhancements must:

- 与 Skill 类型强相关 / Be strongly relevant to Skill type
- 提升实际使用价值 / Improve practical value
- 提升工程化程度 / Improve engineering quality
- 提升 AI 输出稳定性 / Improve AI output stability

**不要 / Don't:**

- 无意义堆规则 / Stack meaningless rules
- 增加 AI 套话 / Add AI boilerplate
- 增加无关能力 / Add irrelevant capabilities
- 让 Prompt 过度膨胀 / Bloat the Prompt

---

## 扩展增强目录规则 / Enhancement Directory Rules

新增增强类型时，可在 `enhancements/` 目录下创建独立 `.md` 文件（如 `enhancements/testing.md`、`enhancements/development.md`），主控自动扫描目录加载所有 `.md` 文件。

文件命名规则：小写 kebab-case，与增强类型名称一致。

独立增强文件应包含：
- 类型名称与描述
- 自动增强项
- 具体方法论
- 重点/Focus

当独立文件与 `enhancements/SKILL.md` 中的同类型内容冲突时，以独立文件为准（更易更新维护）。
