---
name: smartbi-cli
description: Smartbi BI 业务操作入口：AI 对话分析（大模型问数、智能体、知识库/知识图谱构建与训练、数据解释）、数据查询（MQL/DuckDB 取数、指标统计、字段发现）、数据建模（维度/指标/计算成员/命名集管理）、数据源管理（JDBC连接、Schema 与表同步、元数据刷新）、定时任务与 ETL（计划调度、作业流、因果图）、消息推送（企微/钉钉/飞书/邮件/系统消息）、资源与权限管理（目录树、用户/角色/组）。通过 @smartbi/cli 发现与调用 API。
---

# Smartbi CLI
## 流程概览
- **Step 0 — Scenario Router**（入口）：先看用户问句是否命中已有场景。命中 → 加载 `scenarios/` 下对应文件执行；未命中 → 进入 Part 1。
- **Part 1 — Core CLI Workflow**（骨架）：任何 `domain.operationId` 的发现→理解→调用→排错流程一致。
- **Part 2 — Scenario Guides**（场景）：高频业务场景的端到端模板，按需加载。
- **`references/`**（参考）：各 Phase 的详细流程、策略模板与文档路径索引。

## Triggers（触发条件）

当用户描述 **BI 业务动作 + 业务对象**，但未显式给出接口名/operationKey（例如"帮我训练模型资源A""基于模型资源A分析去年销售额"）时触发。

当用户问及 BI 相关业务操作（分析、训练、指标查询、报表/问句类需求、定时计划任务等）时触发本 skill。触发后进入 Step 0 路由判断。

`operationKey` 格式为 `${domain}.${operationId}`（如 `demo.createOrder`、`aichat.getAgentItems`）。`list` 输出结果可直接复制作为 `describe`/`call` 的参数。

---

## 全局约定（所有路径共用）

以下规则适用于 **所有** 执行路径（Part 1 通用流程和 Part 2 场景流程）。先读完全局约定，再进入 Step 0 路由判断。

### CLI 安装与配置

- MUST 仅通过 **npm 全局安装** 获得可执行命令 `smartbi`：`npm install -g @smartbi/cli@latest`，随后 `smartbi --version` 验证版本 ≥ 1.2.0。
- MUST NOT 使用 `yarn` / `pnpm` / `bun` / `npx` 或其它程序代替上述 `smartbi`。
- 初始化 MUST：`smartbi init`（或 `smartbi init --tmpl` 获取占位符模板），再按 `references/init.md` 补齐配置；不得跳过 init 手写。
- 配置文件路径：默认 **`~/.smartbi/config.yaml`**，或用户在 init 后 **明确指定** 的 `--config <path>`。MUST NOT 在系统中猜测或套用其它文件。
- CLI 不存在时的处理流程见 `references/init.md`「标准安装」。

### 自动补齐配置

在首次运行 `smartbi`（任意子命令）时，若检测到 `baseUrl`/`token` 缺失，MUST 分步向用户索要（一次一个问题），全部获取后后台生成配置文件：

1. **先问 Smartbi 地址**：用户提供 → `serverType: smartbi`；用户无法提供 → 询问是否用 SDK Server 地址替代（`serverType: sdk-server`）；仍无法提供 → 暂停。
2. **再问个人令牌**：用户提供后，执行 `smartbi init --tmpl` 获取占位符模板 → 替换 `{{BASE_URL}}`、`{{TOKEN}}`、`{{SERVER_TYPE}}` → 写入 `~/.smartbi/config.yaml`。仅告知用户"配置已写入"，不展示文件内容。
3. `serverType` 取值约束（MUST）：只能是 `sdk-server` 或 `smartbi`，不得使用其他变体。

详细流程与替换规则见 `references/init.md`「生成配置文件」。

### 参数构造规范

构造 `smartbi call` 的请求体时，按以下优先级确定取值来源：
1. **用户输入或上下文已知事实**：对话中已明确提供的值
2. **文档内容**（优先）：字段业务含义、合法枚举值、字段间依赖、完整使用示例（通过 `smartbi doc` 加载）
3. **`requestBodySchema`**（兜底）：文档不可用或未覆盖时使用
4. **`callParameterPlan`**：CLI 标志映射
5. **`suggestedCall`**：仅供参考的命令模板，不应直接复用其占位值
6. **仍无法确定的字段**：向用户确认，不得自行编造

构造 call 参数时，应主动获取 `docs/specs/` 下的业务文档作为理论依据；文档不可用或未覆盖时，以 schema 定义兜底。已加载路径不重复加载。

**请求体文件规范（MUST）**：
- JSON 请求体必须使用 `-d @file.json`（避免跨 shell/OS 转义差异）
- MUST NOT 使用内联 JSON（如 `-d '{"k":"v"}'` 或 `-d "{\"k\":\"v\"}"`）
- 为本轮 `call` **新建**的 JSON 文件：在 `smartbi call` 流程结束后 **MUST** 删除；不得删除用户自带的 `@` 文件
- 临时文件写入系统临时目录或仓库内已 `.gitignore` 的路径，降低误提交风险
- 写入请求体前，若有 Rhino 脚本等需转义的内容，MUST 使用 `scripts/inject-script.mjs` 工具，禁止手工转义

### 子任务机制

执行 `call` 前，若某些参数值依赖其他 smartbi 操作（如先查资源 ID、先创建关联对象），MUST 以子任务方式自动完成，**不得让用户手动查找**。

- 子任务执行路径：**绕过 Step 0 场景匹配**，直接进入 Part 1 Phase 1→3 通用流程（`list` → `describe` → `call`），完成前置操作后把结果填回父 call。
- 退出硬限制（任一触发即停止自动化，执行用户升级流程，详见 `references/call.md`「前置条件与子任务」）：
  - **深度上限**：嵌套深度 ≤ 3（原始 call 为深度 0）
  - **数量上限**：每个父 call 的直接前置子任务 ≤ 5 个
  - **去重**：同一 `operationKey` + 相同参数意图，同一调用链内已完成的前置操作不再重复发起
- 子任务失败时向用户报告原因并暂停当前 call。

### 重试与幂等

- **写请求**（POST / PUT / PATCH / DELETE）：仅当 `--idempotent` 指定或 describe 元数据 `idempotent === true` 时才可自动重试，否则最多尝试 1 次
- **可触发的 HTTP 状态重试**（在剩余次数内）：429 / 502 / 503
- **最大尝试次数**：允许重试时最多 3 次（含指数退避与抖动）

### 输出格式（Output Contract）

每次调用完成后，按以下固定顺序输出：
1. `operationKey`
2. 最终执行命令
3. 关键结果（`status`/`tid`/核心业务字段）
4. 若失败：单行修复建议 + 下一条可执行命令

### 参考文件按需加载

默认只使用 SKILL.md 本摘要。需要模板/字段映射/检查清单/异常分支时，以及需要加载接口关联文档时，才读取 `references/` 下的对应文件或执行 `smartbi doc`。

# Part 1: Core CLI Workflow（骨架流程）

以下四个 Phase 定义了从用户意图到 API 调用的完整流程。
通用参数构造、子任务等底层规则在 [全局约定](#全局约定所有路径共用) 中定义，这里只描述各阶段的执行顺序。

## Phase 0 — 惰性预检

默认不强制在每个新会话先检查安装/配置。直接进入 Phase 1（`list` / discover）。

当**任意一次**实际执行 `smartbi`（任意子命令）时，若出现下列情况，才按 [全局约定 · CLI 安装与配置](#cli-安装与配置) 补齐与排查：

- **CLI 不存在**（`command not found` / 退出码 127 等）→ 立即停止，按标准安装流程处理
- **鉴权/凭证**：`AUTH_FAILED` / `FORBIDDEN` / `PROFILE_NOT_FOUND`
- **服务不可达**：`NETWORK_TIMEOUT` / `NETWORK_ERROR` / `UPSTREAM_UNAVAILABLE`
- **配置缺失或不合法**：`INVALID_ARGUMENT` 且 hint 指向 `Config file not found`

其余错误跳过惰性预检，由 Phase 4 诊断处理。

## Phase 1 — Discover

```
smartbi list --agent
```

1. 默认先执行 `smartbi list --agent`，将候选全集交给大模型做语义重排。
2. 若结果过大，先加 `--domain` / `--service` 再次 `list` 收敛。
3. 若候选唯一且语义明确匹配（用户意图与接口 summary 高度一致，无歧义）→ 直接进入 Phase 2，在 Phase 3 `call` 前向用户展示"准备调用 `<operationKey>`，参数如下…"做一次性确认。不要继续 search，也不要单独停下来等用户确认 operationKey。
4. 若候选唯一但语义匹配度存疑（摘要与意图不完全对应）→ 展示该候选给用户，等用户明确确认后进入 Phase 2。
5. 若存在多条疑似候选无法区分 → 仅对难以区分的候选调用 `smartbi search <operationKey> --verbose --agent` 获取详细信息以消歧。MUST NOT 对所有 Top-N 逐个 search。
6. `search` 的关键词检索仅作为补充回退手段（例如用户提供了明确关键词锚点时），不作为默认第一步。

Phase 1 定位约束（MUST）：
- MUST 默认使用 `list` 路径定位接口，不得先走 `search` 作为主路径。
- `search --verbose` 仅用于消歧，不得对每个候选盲目执行。
- 存在多候选时 MUST 等在候选阶段让用户选择，不得替用户拍板。唯一且明确匹配时可直接进入 Phase 2（在 Phase 3 call 前做一次性确认）。

细节见 `references/discovery.md`。

## Phase 2 — Contract

```
smartbi describe <operationKey> --agent
```

消费字段：`callParameterPlan`、`requestBodySchema`、`consumes/produces`、`suggestedCall`。

### 文档加载（优先获取，不可用时兜底）

`describe` 完成后，应主动尝试加载关联文档作为理解接口语义的理论依据。

**步骤 1 — 识别文档来源**：

| 维度 | 识别方式 | 示例 |
|------|----------|------|
| `description` 中的链接 | 扫描 `describe` 输出的 `description` 字段中的 Markdown 链接 | `[MQL详情](/docs/specs/datamodel/mql/mql.md)` |
| `requestBodySchema` 中的链接 | 沿 `$ref` 链查找被引用 schema 的 `description` 中的链接 | schemas.yaml 中组件定义的 description |
| domain 推断 | 根据 `operationKey` 所属 domain 推断相关文档目录 | `createDataSet` → `docs/specs/tabularmodel/` |
| 数据类型推断 | 根据请求体中涉及的核心数据类型推断参考文档 | 含 `DataSetMeasure` → `docs/specs/tabularmodel/mdl/references/measures.md` |
| `llmBrief` / `summary` 中的引用 | 检查 describe 输出其他字段中的文档引用 | — |

**步骤 2 — 加载与穿透**：对识别到的文档路径，执行 `smartbi doc <path> --agent`，stdout 纳入上下文。文档中的引用链接继续递归加载，硬限制：
- **深度 ≤ 3**（初始文档为深度 0），**去重**（已加载路径不重复）
- 绝对路径 `/...` → 直接传给 `smartbi doc`；相对路径 → 基于当前文档路径解析；外部 URL → WebFetch

**步骤 3 — 文档优先，schema 兜底**：按 [全局约定 · 参数构造规范](#参数构造规范) 的优先级规则取值。文档有定义时以文档为准，不可用时以 schema 兜底。

MUST NOT 忽略链接或自行猜测文档内容。细节见 `references/describe.md`。

## Phase 3 — Execute

```
smartbi call <operationKey> -d @body.json --agent
```

- 参数构造、请求体格式、临时文件清理等底层规则见 [全局约定 · 参数构造规范](#参数构造规范)
- 前置参数依赖的子任务机制见 [全局约定 · 子任务机制](#子任务机制)
- 重试策略与幂等门控见 [全局约定 · 重试与幂等](#重试与幂等)
- 复杂参数组合策略见 `references/strategy.md`

细节见 `references/call.md`。

## Phase 4 — Diagnose

失败后 `smartbi describe <operationKey> --agent`；仍有契约歧义再加 `--include-raw-schema`。
诊断策略参考 `references/strategy.md`。

# Part 2: Scenario Guides（场景索引）

**入口先走 Step 0 — Scenario Router。** 将用户问句与下表比对：
- 命中 → 加载对应场景文件，按场景流程执行
- 未命中 → Part 1 通用流程
- 加载后场景判定不适用 → 回退 Part 1

| 场景 | 关键触发词 | 场景文件 |
|------|-----------|---------|
| S1 定时计划任务 | 每天/每周/定时/cron + 查询/统计/推送/ETL | `scenarios/schedule-task.md` |
| S2 消息推送 | 发送/推送/通知 + 企微/钉钉/飞书/邮件 | `scenarios/push-message.md` |

触发词仅用于快速匹配；精确判定由场景文件 `## 触发` 节负责。仅命中时才加载对应文件。

场景随 OpenAPI 的扩展可持续追加，每个新场景须经过端到端验证后再入库。

> **开发者**：新增场景操作指南见 `docs/guide/smartbi-cli-新增场景操作手册.md`。

---

## 常见错误速查

### CLI / 连接类

| 错误 | 原因 | 处理 |
|------|------|------|
| `command not found` (127) / `is not recognized` | 未安装 CLI | → Phase 0 标准安装 |
| `AUTH_FAILED` (401) | token 无效或已过期 | 让用户重新申请令牌，更新 `config.yaml` |
| `FORBIDDEN` (403) | 用户无权限执行该 operation | 检查 `x-funcPerm` 要求，确认用户角色 |
| `NETWORK_TIMEOUT` / `NETWORK_ERROR` | 服务不可达 | 检查 `baseUrl` 是否正确，网络是否通 |
| `UPSTREAM_UNAVAILABLE` (503) | Smartbi 服务未启动或过载 | 确认服务状态后重试 |
| `Config file not found` (INVALID_ARGUMENT) | 配置文件不存在 | → Phase 0 init 流程 |
| `SpecRejected` / `path not in spec` | sdk-server 路径前缀错误 | 确认 `serverType` 与 `baseUrl` 配置一致 |

### API 业务类

| 错误 | 原因 | 处理 |
|------|------|------|
| `选择字段不能为空` | dims/metrics 空或不匹配 | 先调 `getDataModelTrees` 确认字段 label |
| `Failed to obtain two-dimensional data` | `showDataTable: true` 不兼容某些模型 | 改为 `false`，走 s3Url Parquet |
| `unsupported literal in MQL filter` | MQL `:param` 占位符不兼容 | 改为字面量 `'值'`，内部单引号双写 |
| `connector.remoteInvoke` 报错 | RMI 签名不匹配 | 调 `getTaskScriptEnv` 查看可用方法 |
| HTTP 500 / `Internal Server Error` | 服务端异常 | 记录 `tid`，用 `describe --include-raw-schema` 排查请求体 |

---

## 参考（按需加载）

| 文件 | 内容 |
|------|------|
| `references/init.md` | 安装与配置 |
| `references/discovery.md` | Phase 1 接口发现 |
| `references/describe.md` | Phase 2 契约理解 |
| `references/call.md` | Phase 3 执行调用 |
| `references/strategy.md` | 策略与常见模式（Phase 3 构造复杂参数或 Phase 4 诊断时加载） |
| `references/rhino-template.md` | MQL 取数 Rhino JS 模板（定时任务场景共用） |
| `references/doc-index.md` | domain → 文档路径索引（Phase 2 文档加载时参照） |
| `scenarios/schedule-task.md` | S1 定时计划任务 |
| `scripts/inject-script.mjs` | 脚本注入工具：将多行 JS 文件自动 JSON 转义后注入请求体 |
