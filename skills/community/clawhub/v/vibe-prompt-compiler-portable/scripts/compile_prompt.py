#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import sys
from textwrap import dedent

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from extract_repo_rules import extract_rules

TASK_TYPES = [
    "new-project",
    "page-ui",
    "crud-feature",
    "api-backend",
    "bugfix",
    "refactor",
    "ai-feature",
    "architecture-review",
    "integration",
    "automation-workflow",
    "deployment",
    "general",
]

LANGUAGE_PRESETS = ["english-first", "chinese-first"]
RULESETS = ["none", "minimal-diff", "test-first", "repo-safe"]

TEMPLATES = {
    "new-project": dedent("""\
    You are my senior product-engineering partner.

    Goal:
    Build a minimal viable version of: {request}

    Current Task:
    Turn the idea into a short implementation plan and then build the smallest working slice.

    Context Already Known:
    - Target users: {audience}
    - Problem to solve: {problem}
    - Project maturity: {maturity}

    Assumptions:
    - prioritize the first usable workflow over completeness
    - choose a conventional stack shape unless specified otherwise

    Scope:
    - Define the smallest useful workflow
    - Implement one end-to-end slice
    - Keep the project runnable locally

    Out of Scope:
    - Unrelated extra features
    - Premature architecture complexity
    - Broad rewrites after scaffolding

    Tech Stack:
    - Preferred stack: {stack}

    Constraints:
    - Prefer MVP simplicity over extensibility.
    - Avoid over-engineering.
    - Keep each step independently testable.

    Acceptance Criteria:
    - The smallest useful workflow works.
    - The project runs locally.
    - Key states are handled where relevant.

    Output Requirements:
    1. Restate the goal briefly.
    2. Provide task breakdown.
    3. Propose the smallest first slice.
    4. Implement only that slice unless otherwise asked.
    5. Explain how to verify it.
    """),
    "page-ui": dedent("""\
    You are my senior frontend engineering partner.

    Goal:
    Implement this UI request: {request}

    Current Task:
    Design and build the relevant page/component with working states.

    Context Already Known:
    - User action: {user_action}
    - Primary outcome: {outcome}
    - Style direction: {style}

    Assumptions:
    - follow existing design conventions if present
    - keep layout and interaction accessible and responsive

    Scope:
    - Build only the requested page/component area
    - Include loading, empty, and error states when relevant
    - Match existing conventions if present

    Out of Scope:
    - Unrelated redesigns
    - Backend rewrites
    - New features beyond this UI scope

    Tech Stack:
    - Preferred stack: {stack}

    Constraints:
    - Keep structure simple and reusable.
    - Do not change unrelated files.
    - Avoid unnecessary dependencies.

    Acceptance Criteria:
    - UI renders correctly.
    - Main interaction works.
    - State handling is sensible.

    Output Requirements:
    1. UI structure.
    2. State handling.
    3. Implementation code.
    4. Integration notes.
    """),
    "crud-feature": dedent("""\
    You are my full-stack engineering partner.

    Goal:
    Build a CRUD workflow from this request: {request}

    Current Task:
    Implement the smallest useful create/read/update/delete flow.

    Context Already Known:
    - Entity: {entity}
    - Important fields: {fields}
    - Users: {audience}

    Assumptions:
    - use straightforward validation and conventional API routes
    - optimize for maintainability over abstraction

    Scope:
    - Create flow
    - List view
    - Edit/detail view if needed
    - Validation and clear errors

    Out of Scope:
    - Advanced permissions
    - Analytics
    - Unrelated entities or modules

    Tech Stack:
    - Preferred stack: {stack}

    Constraints:
    - Prefer minimal schema and API surface.
    - Do not invent unnecessary abstractions.
    - Keep naming clear.

    Acceptance Criteria:
    - A user can create an item.
    - The item appears in a list.
    - The item can be updated.
    - Validation and errors are handled.

    Output Requirements:
    1. Data model.
    2. API design.
    3. UI flow.
    4. Minimal implementation order.
    5. Code for the current slice.
    """),
    "api-backend": dedent("""\
    You are my backend engineering partner.

    Goal:
    Implement or modify this backend/API request: {request}

    Current Task:
    Design the API shape and implement the smallest correct backend change.

    Context Already Known:
    - Business purpose: {problem}
    - Inputs/outputs: {io}
    - Existing stack: {stack}

    Assumptions:
    - match existing conventions before inventing new patterns
    - keep validation and error handling explicit

    Scope:
    - Request validation
    - Core business logic
    - Response shape
    - Error handling

    Out of Scope:
    - Full architecture redesign
    - Speculative future endpoints
    - Unrelated refactors

    Constraints:
    - Keep the API surface minimal.
    - Match existing response conventions.
    - Avoid unnecessary dependencies.

    Acceptance Criteria:
    - Endpoint behaves as specified.
    - Invalid input is handled clearly.
    - Success and error responses are consistent.

    Output Requirements:
    1. API design.
    2. Minimal implementation plan.
    3. Code changes.
    4. Verification examples.
    """),
    "bugfix": dedent("""\
    You are my debugging partner.

    Goal:
    Diagnose and minimally fix this bug: {request}

    Current Task:
    Identify the root cause and apply the smallest safe fix.

    Context Already Known:
    - Symptom: {symptom}
    - Expected behavior: {expected}
    - Actual behavior: {actual}
    - Error message: {error}

    Assumptions:
    - preserve existing behavior outside the fix
    - prefer root-cause fixes over cosmetic patches

    Scope:
    - Root-cause analysis
    - Targeted fix
    - Verification steps

    Out of Scope:
    - Broad refactors
    - Unrelated cleanup
    - Speculative optimizations

    Constraints:
    - Preserve existing behavior outside the fix.
    - Change as little as possible.
    - Explain why the bug happened.

    Acceptance Criteria:
    - The bug is resolved.
    - No unrelated behavior changes are introduced.
    - Verification steps are clear.

    Output Requirements:
    1. Root cause.
    2. Minimal fix plan.
    3. Patch/code.
    4. Verification steps.
    """),
    "refactor": dedent("""\
    You are my refactoring partner.

    Goal:
    Refactor this code request without changing behavior: {request}

    Current Task:
    Improve readability, structure, and maintainability with a small safe diff.

    Context Already Known:
    - Main pain point: {problem}
    - Existing stack: {stack}

    Assumptions:
    - preserve external behavior
    - reduce complexity before adding abstractions

    Scope:
    - Readability improvements
    - Duplication reduction
    - Structure simplification

    Out of Scope:
    - Behavior changes
    - New features
    - Unrelated file edits

    Constraints:
    - Keep public behavior the same.
    - Avoid clever abstractions.
    - Prefer a small, understandable diff.

    Acceptance Criteria:
    - Behavior remains unchanged.
    - Code is easier to read and maintain.
    - Each change is easy to explain.

    Output Requirements:
    1. Problems in current code.
    2. Refactor plan.
    3. Updated code.
    4. Verification guidance.
    """),
    "ai-feature": dedent("""\
    You are my AI product-engineering partner.

    Goal:
    Add this AI feature: {request}

    Current Task:
    Design and implement the smallest useful AI workflow.

    Context Already Known:
    - User input: {io}
    - Desired output: {outcome}
    - Existing product context: {problem}

    Assumptions:
    - prefer observable flows over hidden prompt magic
    - keep cost, latency, and failure behavior explicit

    Scope:
    - Prompt structure
    - Invocation path
    - Result handling
    - Failure handling

    Out of Scope:
    - Complex orchestration unless explicitly requested
    - Broad platform rewrites
    - Speculative evaluation systems

    Constraints:
    - Keep the workflow observable and easy to debug.
    - Prefer deterministic output formats.
    - Manage cost and latency explicitly.

    Acceptance Criteria:
    - A user can trigger the AI feature.
    - Output format is usable.
    - Failure states are handled.

    Output Requirements:
    1. Interaction design.
    2. Prompt shape.
    3. Backend/client flow.
    4. Minimal implementation.
    5. Verification steps.
    """),
    "architecture-review": dedent("""\
    You are my principal software architect.

    Goal:
    Design a practical architecture for this request: {request}

    Current Task:
    Turn the request into a concrete architecture decision with an implementation path.

    Context Already Known:
    - Product or system: {system}
    - Current stack: {stack}
    - Operating constraints: {constraints}
    - Scale or reliability concerns: {concerns}

    Assumptions:
    - prefer evolutionary change over full rewrite
    - optimize for clarity, operability, and future migration paths

    Scope:
    - system boundaries
    - service or module responsibilities
    - data/storage design
    - scaling and isolation strategy
    - rollout path

    Out of Scope:
    - speculative platform rebuilding
    - unnecessary microservices
    - implementation of every component unless requested

    Constraints:
    - explain trade-offs explicitly
    - prefer simple operating models
    - separate current-state recommendation from future-state evolution

    Acceptance Criteria:
    - the architecture is implementable
    - trade-offs are clear
    - a phased rollout path exists
    - performance and operational risks are addressed

    Output Requirements:
    1. Architecture recommendation.
    2. Alternatives considered.
    3. Trade-offs.
    4. Phased implementation plan.
    5. Validation and monitoring guidance.
    """),
    "integration": dedent("""\
    You are my senior integration engineer.

    Goal:
    Connect this system with another service or platform: {request}

    Current Task:
    Define and implement the safest minimal integration slice.

    Context Already Known:
    - Source system: {source}
    - Target system: {target}
    - Data or action flow: {flow}
    - Auth model if known: {auth}

    Assumptions:
    - third-party systems can fail, throttle, or return inconsistent payloads
    - idempotency matters unless explicitly irrelevant

    Scope:
    - auth and credentials flow
    - request/response mapping
    - retries and failure handling
    - observability and verification

    Out of Scope:
    - broad platform redesign
    - unnecessary SDK abstractions
    - unrelated product work

    Constraints:
    - keep integration boundaries explicit
    - document rate limits, retries, and idempotency behavior
    - avoid hidden side effects

    Acceptance Criteria:
    - the integration works for the primary use case
    - failures are handled predictably
    - verification and debugging steps are clear

    Output Requirements:
    1. Integration design.
    2. Data flow.
    3. Failure and retry rules.
    4. Minimal implementation plan.
    5. Verification checklist.
    """),
    "automation-workflow": dedent("""\
    You are my workflow automation engineer.

    Goal:
    Design or improve this automation workflow: {request}

    Current Task:
    Turn the request into a reliable, observable workflow with a minimal first slice.

    Context Already Known:
    - Trigger: {trigger}
    - Inputs: {inputs}
    - Outputs: {outputs}
    - Systems involved: {systems}

    Assumptions:
    - automation can fail mid-run and must be restartable
    - operational visibility matters as much as the happy path

    Scope:
    - trigger and execution flow
    - sync vs async boundary
    - retries, idempotency, and alerts
    - minimal implementation slice

    Out of Scope:
    - overbuilt orchestration layers
    - abstract platforms without a real workflow need
    - unrelated app refactors

    Constraints:
    - keep execution observable
    - define ownership for failure handling
    - prefer deterministic steps where possible

    Acceptance Criteria:
    - the workflow can run reliably for the main use case
    - retry and failure behavior are defined
    - monitoring or alert hooks are identified

    Output Requirements:
    1. Workflow design.
    2. Execution states.
    3. Retry and failure rules.
    4. Implementation slice.
    5. Verification steps.
    """),
    "deployment": dedent("""\
    You are my release engineering partner.

    Goal:
    Deploy or prepare this project for deployment: {request}

    Current Task:
    Choose the simplest reliable deployment path and list the required changes.

    Context Already Known:
    - App/project type: {problem}
    - Stack: {stack}
    - Target environment: {outcome}

    Assumptions:
    - prefer the least operational overhead that still meets the requirement
    - make rollback and verification explicit

    Scope:
    - Deployment steps
    - Environment variables
    - Basic verification
    - Rollback awareness

    Out of Scope:
    - Full infrastructure redesign
    - Unrelated code changes

    Constraints:
    - Prefer the least operational overhead.
    - Keep setup explicit.
    - Call out secrets and environment assumptions.

    Acceptance Criteria:
    - Deployment steps are complete.
    - Required environment variables are known.
    - A post-deploy verification path exists.

    Output Requirements:
    1. Deployment recommendation.
    2. Config/env checklist.
    3. Step-by-step rollout.
    4. Verification and rollback notes.
    """),
    "general": dedent("""\
    You are my senior engineering partner.

    Goal:
    Help with this request: {request}

    Current Task:
    Convert the request into a scoped implementation task and solve only the current slice.

    Context Already Known:
    - Constraints: {problem}
    - Existing stack: {stack}

    Assumptions:
    - prefer explicit assumptions to fake certainty
    - narrow scope before expanding effort

    Scope:
    - Only the directly requested work

    Out of Scope:
    - Unrelated refactors
    - Hidden assumptions presented as facts

    Constraints:
    - Make assumptions explicit.
    - Prefer minimal, testable progress.
    - Ask only if a missing detail blocks progress.

    Acceptance Criteria:
    - The output is scoped, implementable, and verifiable.

    Output Requirements:
    1. Clarified goal.
    2. Assumptions.
    3. Minimal plan.
    4. Implementation for the current step.
    5. Verification guidance.
    """),
}

CHINESE_TEMPLATES = {
    "new-project": dedent("""\
    你是我的资深产品与工程协作伙伴。

    目标：
    构建这个需求的最小可用版本：{request}

    当前任务：
    先把想法整理成简短实现计划，再完成最小可运行切片。

    已知上下文：
    - 目标用户：{audience}
    - 要解决的问题：{problem}
    - 项目阶段：{maturity}

    假设：
    - 优先交付第一个真正可用的工作流，而不是追求完整性
    - 如果没有明确指定，就采用常规且易落地的技术栈形态

    范围：
    - 定义最小但有价值的核心工作流
    - 实现一条端到端切片
    - 保持项目可在本地运行

    非范围：
    - 无关的额外功能
    - 过早引入架构复杂度
    - 搭好脚手架后再做大范围重写

    技术栈：
    - 优先技术栈：{stack}

    约束：
    - 优先 MVP 简洁性，而不是过度扩展性
    - 避免过度设计
    - 每一步都应可独立验证

    验收标准：
    - 最小有用工作流能够跑通
    - 项目可以本地运行
    - 关键状态在相关场景下已被覆盖

    输出要求：
    1. 简要重述目标。
    2. 给出任务拆解。
    3. 提出最小第一切片。
    4. 除非另有要求，否则只实现这一切片。
    5. 说明如何验证。
    """),
    "page-ui": dedent("""\
    你是我的资深前端工程协作伙伴。

    目标：
    实现这个 UI 需求：{request}

    当前任务：
    设计并实现相关页面/组件，并补齐可运行状态。

    已知上下文：
    - 用户动作：{user_action}
    - 主要结果：{outcome}
    - 风格方向：{style}

    假设：
    - 如果项目里已有设计规范，就优先沿用
    - 布局与交互要兼顾可访问性和响应式

    范围：
    - 只实现被请求的页面或组件区域
    - 相关时补齐加载、空态和错误态
    - 尽量对齐现有项目约定

    非范围：
    - 无关重设计
    - 后端重写
    - 超出当前 UI 范围的新功能

    技术栈：
    - 优先技术栈：{stack}

    约束：
    - 保持结构简单且可复用
    - 不改动无关文件
    - 避免引入不必要依赖

    验收标准：
    - UI 渲染正确
    - 主要交互可用
    - 状态处理合理

    输出要求：
    1. UI 结构。
    2. 状态处理。
    3. 实现代码。
    4. 集成说明。
    """),
    "crud-feature": dedent("""\
    你是我的全栈工程协作伙伴。

    目标：
    基于这个需求构建 CRUD 工作流：{request}

    当前任务：
    实现最小但有用的增删改查流程。

    已知上下文：
    - 实体：{entity}
    - 关键字段：{fields}
    - 用户：{audience}

    假设：
    - 使用直白的校验和常规 API 路由
    - 优先可维护性，而不是抽象炫技

    范围：
    - 新增流程
    - 列表视图
    - 按需补齐编辑/详情视图
    - 校验和清晰报错

    非范围：
    - 高级权限设计
    - 数据分析
    - 无关实体或模块

    技术栈：
    - 优先技术栈：{stack}

    约束：
    - 数据结构和 API 面尽量最小化
    - 不发明没必要的抽象
    - 命名保持清晰

    验收标准：
    - 用户可以创建一条记录
    - 记录会出现在列表中
    - 记录可以被更新
    - 校验与错误处理清晰

    输出要求：
    1. 数据模型。
    2. API 设计。
    3. UI 流程。
    4. 最小实现顺序。
    5. 当前切片代码。
    """),
    "api-backend": dedent("""\
    你是我的后端工程协作伙伴。

    目标：
    实现或修改这个后端/API 需求：{request}

    当前任务：
    设计 API 形态，并实现最小且正确的后端改动。

    已知上下文：
    - 业务目的：{problem}
    - 输入/输出：{io}
    - 现有技术栈：{stack}

    假设：
    - 优先匹配现有约定，而不是发明新模式
    - 保持校验和错误处理清晰可见

    范围：
    - 请求校验
    - 核心业务逻辑
    - 返回结构
    - 错误处理

    非范围：
    - 全量架构重设计
    - 对未来接口的过度预埋
    - 无关重构

    约束：
    - 保持 API 面最小化
    - 对齐现有返回约定
    - 避免引入不必要依赖

    验收标准：
    - 接口行为符合预期
    - 非法输入能被清晰处理
    - 成功与失败响应保持一致

    输出要求：
    1. API 设计。
    2. 最小实现计划。
    3. 代码改动。
    4. 验证示例。
    """),
    "bugfix": dedent("""\
    你是我的调试协作伙伴。

    目标：
    诊断并以最小改动修复这个问题：{request}

    当前任务：
    找出根因，并应用最小且安全的修复。

    已知上下文：
    - 现象：{symptom}
    - 预期行为：{expected}
    - 实际行为：{actual}
    - 错误信息：{error}

    假设：
    - 修复之外的现有行为应保持不变
    - 优先修根因，而不是做表面补丁

    范围：
    - 根因分析
    - 定向修复
    - 验证步骤

    非范围：
    - 大范围重构
    - 无关清理
    - 猜测式优化

    约束：
    - 除修复点外尽量保持行为不变
    - 改动越小越好
    - 说明 bug 为什么会发生

    验收标准：
    - 问题得到解决
    - 没有引入无关行为变化
    - 验证步骤足够清晰

    输出要求：
    1. 根因。
    2. 最小修复计划。
    3. 补丁/代码。
    4. 验证步骤。
    """),
    "refactor": dedent("""\
    你是我的重构协作伙伴。

    目标：
    在不改变行为的前提下重构这段需求对应的代码：{request}

    当前任务：
    用一个小而安全的 diff 改善可读性、结构和可维护性。

    已知上下文：
    - 主要痛点：{problem}
    - 现有技术栈：{stack}

    假设：
    - 保持外部行为不变
    - 优先先降复杂度，再考虑抽象

    范围：
    - 提升可读性
    - 减少重复
    - 简化结构

    非范围：
    - 行为改动
    - 新功能
    - 无关文件改动

    约束：
    - 对外行为保持一致
    - 避免炫技式抽象
    - 优先小而好懂的 diff

    验收标准：
    - 行为保持不变
    - 代码更易读、更易维护
    - 每一处改动都容易解释

    输出要求：
    1. 当前代码的问题。
    2. 重构计划。
    3. 更新后的代码。
    4. 验证建议。
    """),
    "ai-feature": dedent("""\
    你是我的 AI 产品与工程协作伙伴。

    目标：
    为产品增加这个 AI 功能：{request}

    当前任务：
    设计并实现最小但有价值的 AI 工作流。

    已知上下文：
    - 用户输入：{io}
    - 期望输出：{outcome}
    - 现有产品上下文：{problem}

    假设：
    - 优先可观测流程，而不是隐藏式 prompt 魔法
    - 成本、时延和失败行为都应明确

    范围：
    - Prompt 结构
    - 调用路径
    - 结果处理
    - 失败处理

    非范围：
    - 未明确要求时的复杂编排
    - 大范围平台重写
    - 猜测式评估体系

    约束：
    - 工作流要可观测且易调试
    - 优先确定性的输出格式
    - 明确管理成本和时延

    验收标准：
    - 用户能触发这个 AI 功能
    - 输出格式可用
    - 失败状态被处理

    输出要求：
    1. 交互设计。
    2. Prompt 形态。
    3. 前后端流程。
    4. 最小实现。
    5. 验证步骤。
    """),
    "architecture-review": dedent("""\
    你是我的首席软件架构协作伙伴。

    目标：
    为这个需求设计一个务实可落地的架构：{request}

    当前任务：
    把需求收敛成明确的架构决策，并给出实现路径。

    已知上下文：
    - 产品或系统：{system}
    - 当前技术栈：{stack}
    - 运行约束：{constraints}
    - 规模或可靠性关注点：{concerns}

    假设：
    - 优先渐进式演进，而不是整体重写
    - 优先清晰性、可运维性和未来迁移路径

    范围：
    - 系统边界
    - 服务或模块职责
    - 数据/存储设计
    - 扩展性与隔离策略
    - 分阶段落地路径

    非范围：
    - 纯概念化的平台重建
    - 没必要的微服务拆分
    - 在未要求时实现所有组件

    约束：
    - 明确解释 trade-off
    - 优先简单可运维的模型
    - 区分当前建议与未来演进方向

    验收标准：
    - 架构可落地
    - trade-off 清晰
    - 有分阶段实施路径
    - 性能与运维风险被覆盖

    输出要求：
    1. 架构建议。
    2. 备选方案。
    3. 关键权衡。
    4. 分阶段实施计划。
    5. 验证与监控建议。
    """),
    "integration": dedent("""\
    你是我的资深集成工程协作伙伴。

    目标：
    把当前系统与另一个服务或平台接起来：{request}

    当前任务：
    定义并实现最小且安全的集成切片。

    已知上下文：
    - 来源系统：{source}
    - 目标系统：{target}
    - 数据或动作流：{flow}
    - 已知鉴权方式：{auth}

    假设：
    - 第三方系统可能失败、限流或返回不一致 payload
    - 除非明确无关，否则要考虑幂等性

    范围：
    - 鉴权与凭证流
    - 请求/响应映射
    - 重试与失败处理
    - 可观测性与验证方式

    非范围：
    - 大范围平台重设计
    - 没必要的 SDK 抽象
    - 无关产品工作

    约束：
    - 集成边界必须清晰
    - 记录限流、重试与幂等性策略
    - 避免隐藏副作用

    验收标准：
    - 主用例可用
    - 失败处理可预测
    - 验证与排障步骤清晰

    输出要求：
    1. 集成设计。
    2. 数据流。
    3. 失败与重试规则。
    4. 最小实现计划。
    5. 验证清单。
    """),
    "automation-workflow": dedent("""\
    你是我的自动化工作流工程协作伙伴。

    目标：
    设计或改进这个自动化工作流：{request}

    当前任务：
    把需求整理成可靠、可观测的工作流，并落地最小第一版切片。

    已知上下文：
    - 触发方式：{trigger}
    - 输入：{inputs}
    - 输出：{outputs}
    - 涉及系统：{systems}

    假设：
    - 自动化可能中途失败，必须支持可恢复执行
    - 运维可见性和 happy path 一样重要

    范围：
    - 触发与执行流
    - 同步/异步边界
    - 重试、幂等与告警
    - 最小实现切片

    非范围：
    - 过度设计的编排层
    - 没有真实需求的抽象平台
    - 无关应用重构

    约束：
    - 执行过程要可观测
    - 失败处理责任要明确
    - 能确定性就尽量确定性

    验收标准：
    - 主用例可稳定运行
    - 重试与失败行为被定义清楚
    - 监控或告警挂点被识别出来

    输出要求：
    1. 工作流设计。
    2. 执行状态。
    3. 重试与失败规则。
    4. 实现切片。
    5. 验证步骤。
    """),
    "deployment": dedent("""\
    你是我的发布与部署工程协作伙伴。

    目标：
    部署这个项目，或把它整理成可部署状态：{request}

    当前任务：
    选择最简单且可靠的部署路径，并列出所需改动。

    已知上下文：
    - 应用/项目类型：{problem}
    - 技术栈：{stack}
    - 目标环境：{outcome}

    假设：
    - 优先最低运维负担且能满足要求的方案
    - 回滚与验证路径必须明确

    范围：
    - 部署步骤
    - 环境变量
    - 基础验证
    - 回滚意识

    非范围：
    - 全量基础设施重设计
    - 无关代码改动

    约束：
    - 优先最低运维负担
    - 配置过程必须显式
    - 明确指出密钥和环境假设

    验收标准：
    - 部署步骤完整
    - 所需环境变量明确
    - 存在部署后验证路径

    输出要求：
    1. 部署建议。
    2. 配置/环境清单。
    3. 分步上线流程。
    4. 验证与回滚说明。
    """),
    "general": dedent("""\
    你是我的资深工程协作伙伴。

    目标：
    协助完成这个需求：{request}

    当前任务：
    把需求转换成边界清晰的实现任务，并只解决当前切片。

    已知上下文：
    - 约束：{problem}
    - 现有技术栈：{stack}

    假设：
    - 显式写出假设，不伪装成确定事实
    - 先收紧范围，再扩展投入

    范围：
    - 只处理被直接要求的工作

    非范围：
    - 无关重构
    - 把隐含猜测包装成既定事实

    约束：
    - 假设必须明确
    - 优先最小且可验证的进展
    - 只有在真正阻塞时才追问缺失细节

    验收标准：
    - 输出边界清晰、可实现、可验证

    输出要求：
    1. 澄清目标。
    2. 明确假设。
    3. 最小计划。
    4. 当前步骤的实现。
    5. 验证方式。
    """),
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def detect_task_type(request: str) -> str:
    text = request.lower()
    if any(word in text for word in ["bug", "报错", "fix", "broken", "异常", "修复", "不生效", "崩溃", "500", "404", "traceback"]):
        return "bugfix"
    if any(word in text for word in ["refactor", "重构", "整理代码", "优化结构", "improve readability"]):
        return "refactor"
    if any(word in text for word in [
        "架构", "architecture", "多租户", "multi-tenant", "隔离", "扩容", "高并发", "scaling", "scalability",
        "缓存", "队列", "control plane", "data plane", "tool catalog", "tool discovery", "selective discovery",
        "handshake", "protocol design", "协议设计", "工具发现", "按需发现", "expose every tool", "exposing every tool"
    ]):
        return "architecture-review"
    if any(word in text for word in ["集成", "integration", "webhook", "sso", "oauth", "支付", "payment", "对接", "第三方", "同步到", "回调", "回写", "打通", "api 对接"]):
        return "integration"
    if any(word in text for word in ["deploy", "上线", "vercel", "docker", "env", "环境变量", "发布", "ci/cd", "k8s", "nginx", "部署", "windows 机器", "迁移"]):
        return "deployment"
    if any(word in text for word in ["自动化", "workflow", "cron", "定时", "队列任务", "background job", "worker", "异步任务", "审批流", "pipeline"]):
        return "automation-workflow"
    if any(word in text for word in ["api", "接口", "endpoint", "route", "后端", "handler", "schema", "数据库写入"]):
        return "api-backend"
    if any(word in text for word in [
        "页面", "landing page", "landing", "组件", "表单", "screen", "page", "resize", "resizable",
        "layout", "pane", "sidebar", "modal", "dialog", "responsive", "preview window", "preview pane"
    ]):
        return "page-ui"
    if any(word in text for word in ["crud", "列表", "新增", "编辑", "删除", "detail", "create", "update"]):
        return "crud-feature"
    if any(word in text for word in ["ai", "llm", "chat", "总结", "提取", "生成", "agent", "智能"]):
        return "ai-feature"
    if any(word in text for word in ["build", "做一个", "从零", "mvp", "prototype", "原型", "app", "工具", "后台", "admin panel", "admin", "dashboard"]):
        return "new-project"
    return "general"


def extract_entity(request: str) -> str:
    match = re.search(r"(?:for|about|管理|创建|新增|实现)([A-Za-z0-9_\-\u4e00-\u9fff ]{2,30})(?:的| crud| CRUD| 列表| 接口| 页面| flow| 功能)?", request, re.IGNORECASE)
    if match:
        return normalize_text(match.group(1))
    return "Not clearly specified"


def build_context(request: str, stack: str, audience: str) -> dict:
    text = normalize_text(request)
    return {
        "request": text,
        "stack": stack or "Use the existing project stack or choose the simplest suitable option",
        "audience": audience or "Not specified",
        "problem": "Not fully specified; infer the simplest practical interpretation from the request",
        "maturity": "MVP unless the user explicitly asks for production-grade implementation",
        "user_action": "Derived from the request; infer the primary user flow before coding",
        "outcome": "Deliver the requested behavior with a minimal, testable implementation",
        "style": "Match existing product style or use a clean modern SaaS style",
        "entity": extract_entity(text),
        "fields": "Infer the minimum necessary fields and call out assumptions",
        "io": "Infer likely inputs and outputs from the request and make assumptions explicit",
        "symptom": text,
        "expected": "Match the intended behavior implied by the request",
        "actual": "Currently broken or incomplete as described in the request",
        "error": "Use the provided error if any; otherwise request logs only if they block diagnosis",
        "system": "Infer the current product or application boundary from the request",
        "constraints": "Use stated constraints first; otherwise prefer minimal-risk evolution",
        "concerns": "Infer likely reliability, scale, isolation, or maintainability concerns from the request",
        "source": "Infer the source system from the request",
        "target": "Infer the target system from the request",
        "flow": "Infer the primary sync or data flow from the request",
        "auth": "Assume standard auth unless the request specifies otherwise",
        "trigger": "Infer the event, schedule, or user action that starts the workflow",
        "inputs": "Infer the required inputs and call out assumptions",
        "outputs": "Infer the expected outputs and side effects",
        "systems": "Infer the internal and external systems involved in the workflow",
    }


def localize_prompt(text: str, language_preset: str) -> str:
    if language_preset != "chinese-first":
        return text

    replacements = [
        ("You are my senior product-engineering partner.", "你是我的资深产品与工程协作伙伴。"),
        ("You are my senior frontend engineering partner.", "你是我的资深前端工程协作伙伴。"),
        ("You are my full-stack engineering partner.", "你是我的全栈工程协作伙伴。"),
        ("You are my backend engineering partner.", "你是我的后端工程协作伙伴。"),
        ("You are my debugging partner.", "你是我的调试协作伙伴。"),
        ("You are my refactoring partner.", "你是我的重构协作伙伴。"),
        ("You are my AI product-engineering partner.", "你是我的 AI 产品与工程协作伙伴。"),
        ("You are my principal software architect.", "你是我的首席软件架构协作伙伴。"),
        ("You are my senior integration engineer.", "你是我的资深集成工程协作伙伴。"),
        ("You are my workflow automation engineer.", "你是我的自动化工作流工程协作伙伴。"),
        ("You are my release engineering partner.", "你是我的发布与部署工程协作伙伴。"),
        ("You are my senior engineering partner.", "你是我的资深工程协作伙伴。"),
        ("Goal:", "目标："),
        ("Current Task:", "当前任务："),
        ("Context Already Known:", "已知上下文："),
        ("Assumptions:", "假设："),
        ("Scope:", "范围："),
        ("Out of Scope:", "非范围："),
        ("Tech Stack:", "技术栈："),
        ("Constraints:", "约束："),
        ("Acceptance Criteria:", "验收标准："),
        ("Output Requirements:", "输出要求："),
        ("Build a minimal viable version of:", "构建这个需求的最小可用版本："),
        ("Implement this UI request:", "实现这个 UI 需求："),
        ("Build a CRUD workflow from this request:", "基于这个需求构建 CRUD 工作流："),
        ("Implement or modify this backend/API request:", "实现或修改这个后端/API 需求："),
        ("Diagnose and minimally fix this bug:", "诊断并以最小改动修复这个问题："),
        ("Refactor this code request without changing behavior:", "在不改变行为的前提下重构这段需求对应的代码："),
        ("Add this AI feature:", "为产品增加这个 AI 功能："),
        ("Design a practical architecture for this request:", "为这个需求设计一个务实可落地的架构："),
        ("Connect this system with another service or platform:", "把当前系统与另一个服务或平台接起来："),
        ("Design or improve this automation workflow:", "设计或改进这个自动化工作流："),
        ("Deploy or prepare this project for deployment:", "部署这个项目，或把它整理成可部署状态："),
        ("Help with this request:", "协助完成这个需求："),
        ("Identify the root cause and apply the smallest safe fix.", "找出根因，并应用最小且安全的修复。"),
        ("Design the API shape and implement the smallest correct backend change.", "设计 API 形态，并实现最小且正确的后端改动。"),
        ("Turn the idea into a short implementation plan and then build the smallest working slice.", "先把想法整理成简短实现计划，再完成最小可运行切片。"),
        ("Design and build the relevant page/component with working states.", "设计并实现相关页面/组件，并补齐可运行状态。"),
        ("Turn the request into a concrete architecture decision with an implementation path.", "把需求收敛成明确的架构决策，并给出实现路径。"),
        ("Define and implement the safest minimal integration slice.", "定义并实现最小且安全的集成切片。"),
        ("Turn the request into a reliable, observable workflow with a minimal first slice.", "把需求整理成可靠、可观测的工作流，并落地最小第一版切片。"),
        ("Choose the simplest reliable deployment path and list the required changes.", "选择最简单且可靠的部署路径，并列出所需改动。"),
        ("Convert the request into a scoped implementation task and solve only the current slice.", "把需求转换成边界清晰的实现任务，并只解决当前切片。"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def localize_assumptions(assumptions: list[str], language_preset: str) -> list[str]:
    if language_preset != "chinese-first":
        return assumptions

    mapping = {
        "Missing details are converted into explicit assumptions instead of hidden guesses.": "缺失细节应转成显式假设，而不是隐含猜测。",
        "The implementation should prefer a minimal, verifiable slice.": "实现应优先选择最小且可验证的切片。",
        "Unrelated files should not be changed unless necessary.": "除非必要，不要改动无关文件。",
        "Prefer evolutionary change over broad rewrites unless the request clearly requires a redesign.": "除非需求明确要求重构，否则优先渐进式演进而不是大改。",
    }
    return [mapping.get(item, item) for item in assumptions]


def empty_rule_payload() -> dict:
    return {"must_rules": [], "must_not_rules": [], "validation_rules": [], "scope_guardrails": []}


def load_repo_rules(repo_rules_file: str) -> dict:
    if not repo_rules_file:
        return empty_rule_payload()
    path = pathlib.Path(repo_rules_file)
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "must_rules": data.get("must_rules", []),
        "must_not_rules": data.get("must_not_rules", []),
        "validation_rules": data.get("validation_rules", []),
        "scope_guardrails": data.get("scope_guardrails", []),
    }


def merge_rule_payloads(base: dict, extra: dict) -> dict:
    merged = {}
    for key in ["must_rules", "must_not_rules", "validation_rules", "scope_guardrails"]:
        merged[key] = list(dict.fromkeys([*base.get(key, []), *extra.get(key, [])]))
    return merged


def build_ruleset_payload(ruleset: str, language_preset: str) -> dict:
    if ruleset == "none":
        return {"must_rules": [], "must_not_rules": [], "validation_rules": [], "scope_guardrails": []}

    if language_preset == "chinese-first":
        packs = {
            "minimal-diff": {
                "must_rules": ["只改和当前任务直接相关的文件。", "保持现有命名、风格和项目约定。"],
                "must_not_rules": ["不要做无关重构。", "不要顺手扩大范围。"],
                "validation_rules": ["给出最小可行的验证步骤。"],
                "scope_guardrails": ["优先小补丁而不是大改。"],
            },
            "test-first": {
                "must_rules": ["先明确验证方式，再动手修改。", "优先补最贴近改动的测试或检查步骤。"],
                "must_not_rules": ["不要在没有验证路径时直接提交大改。"],
                "validation_rules": ["列出自动测试或手工验证步骤。", "说明修复前后预期差异。"],
                "scope_guardrails": ["验证范围先从最小相关范围开始。"],
            },
            "repo-safe": {
                "must_rules": ["遵守仓库现有约定和目录边界。", "优先复用已有模式，而不是新建抽象。"],
                "must_not_rules": ["不要改动无关模块。", "不要新增依赖，除非必要且说明原因。"],
                "validation_rules": ["说明受影响文件和验证方式。"],
                "scope_guardrails": ["把改动限制在当前任务涉及的目录和文件中。"],
            },
        }
    else:
        packs = {
            "minimal-diff": {
                "must_rules": ["Change only files directly related to the task.", "Preserve existing naming, style, and project conventions."],
                "must_not_rules": ["Do not perform unrelated refactors.", "Do not expand scope opportunistically."],
                "validation_rules": ["Provide the smallest viable verification steps."],
                "scope_guardrails": ["Prefer a small patch over broad changes."],
            },
            "test-first": {
                "must_rules": ["Define how the change will be verified before editing.", "Prefer the closest relevant test or verification step first."],
                "must_not_rules": ["Do not make broad changes without a verification path."],
                "validation_rules": ["List automated tests or manual verification steps.", "Explain the expected before/after behavior."],
                "scope_guardrails": ["Start validation from the smallest affected surface."],
            },
            "repo-safe": {
                "must_rules": ["Follow existing repository conventions and directory boundaries.", "Prefer existing patterns over inventing new abstractions."],
                "must_not_rules": ["Do not modify unrelated modules.", "Do not add dependencies unless necessary and justified."],
                "validation_rules": ["Describe impacted files and how to verify them."],
                "scope_guardrails": ["Keep the patch limited to files and directories touched by the current task."],
            },
        }
    return packs[ruleset]


def compile_prompt(task: str, request: str, stack: str, audience: str, language_preset: str, ruleset: str, repo_rules_file: str, repo_root: str, auto_repo_rules: bool) -> dict:
    detected = detect_task_type(request) if task == "auto" else task
    if detected not in TEMPLATES:
        detected = "general"
    context = build_context(request, stack, audience)
    template_map = CHINESE_TEMPLATES if language_preset == "chinese-first" else TEMPLATES
    template = template_map.get(detected, TEMPLATES[detected])
    prompt = template.format(**context).strip() + "\n"
    assumptions = [
        "Missing details are converted into explicit assumptions instead of hidden guesses.",
        "The implementation should prefer a minimal, verifiable slice.",
        "Unrelated files should not be changed unless necessary.",
    ]
    if detected in ["architecture-review", "integration", "automation-workflow"]:
        assumptions.append("Prefer evolutionary change over broad rewrites unless the request clearly requires a redesign.")
    localized_prompt = prompt if language_preset == "chinese-first" and detected in CHINESE_TEMPLATES else localize_prompt(prompt, language_preset)
    localized_assumptions = localize_assumptions(assumptions, language_preset)
    rules = build_ruleset_payload(ruleset, language_preset)
    repo_rules = load_repo_rules(repo_rules_file)
    auto_rules = extract_rules(repo_root) if auto_repo_rules and repo_root else empty_rule_payload()
    merged_rules = merge_rule_payloads(merge_rule_payloads(rules, repo_rules), auto_rules)
    return {
        "task_type": detected,
        "request": normalize_text(request),
        "language_preset": language_preset,
        "ruleset": ruleset,
        "repo_rules_file": repo_rules_file,
        "repo_root": repo_root,
        "auto_repo_rules": auto_repo_rules,
        "compiled_prompt": localized_prompt,
        "assumptions": localized_assumptions,
        **merged_rules,
    }


def main():
    parser = argparse.ArgumentParser(description="Compile rough coding requests into portable structured prompts.")
    parser.add_argument("--task", default="auto", choices=["auto", *TASK_TYPES], help="Task type to compile. Default: auto")
    parser.add_argument("--request", required=True, help="Raw user request")
    parser.add_argument("--stack", default="", help="Preferred tech stack")
    parser.add_argument("--audience", default="", help="Target users or stakeholders")
    parser.add_argument("--language-preset", default="english-first", choices=LANGUAGE_PRESETS, help="Language style preset")
    parser.add_argument("--ruleset", default="none", choices=RULESETS, help="Development rule preset")
    parser.add_argument("--repo-rules-file", default="", help="Optional JSON file with repository-specific rules")
    parser.add_argument("--repo-root", default="", help="Repository root for automatic rule extraction")
    parser.add_argument("--auto-repo-rules", action="store_true", help="Automatically extract rules from common repository files")
    parser.add_argument("--output", default="prompt", choices=["prompt", "json"], help="Output format")
    args = parser.parse_args()

    result = compile_prompt(args.task, args.request, args.stack, args.audience, args.language_preset, args.ruleset, args.repo_rules_file, args.repo_root, args.auto_repo_rules)
    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["compiled_prompt"])


if __name__ == "__main__":
    main()
