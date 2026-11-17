---
name: smartbi-cli
description: 广州思迈特软件有限公司（思迈特）提供的 SmartBI 通用业务操作技能。当用户需要连接 SmartBI、查询数据模型或指标模型、对已有报表问数、进行 AI 问数与复杂洞察，或管理智能体、知识库与知识图谱、数据模型、数据源、定时任务与 ETL、消息推送、资源及权限时使用。通过 @smartbi/cli 发现并调用当前环境的 SmartBI API，支持 MQL 与只读 SQL 直接取数。
---

# SmartBI CLI

## 流程概览
- **Step 0 — Scenario Router**（入口）：先看用户问句是否命中 Part 2 场景索引。命中 → 加载对应场景文件执行；未命中 → 进入 Part 1。组合请求按业务步骤衔接，不让取数场景覆盖调度、推送或资源操作。
- **Part 1 — Core CLI Workflow**（骨架）：任何 `domain.operationId` 的发现→理解→调用→排错流程一致。
- **Part 2 — Scenario Guides**（场景）：高频业务场景的端到端模板，按需加载。
- **`references/`**（参考）：各 Phase 的详细流程、策略模板与文档路径索引。

数据查询与洞察的扩展路径见 [scenarios/data-query.md](scenarios/data-query.md)，按需加载，不改变其他场景的通用调用流程。

命中数据查询与洞察场景后，已知 operationKey 按场景文件的最短可验证调用链执行；资源未知时按该场景定位业务资源。该场景已授权只读调用不执行下文 Phase 3 的逐次确认；下文 Part 1 的通用接口发现与写操作规则继续用于其他业务操作。

## Triggers（触发条件）

当用户描述 **BI 业务动作 + 业务对象**，但未显式给出接口名/operationKey（例如"帮我训练模型资源A""基于模型资源A分析去年销售额"）时触发。

当用户问及 BI 相关业务操作（分析、训练、指标查询、报表/问句类需求、定时计划任务等）时触发本 skill。触发后进入 Step 0 路由判断。

`operationKey` 格式为 `${domain}.${operationId}`（如 `demo.createOrder`、`aichat.getAgentItems`）。`list` 输出结果可直接复制作为 `describe`/`call` 的参数。

---

## 全局约定（所有路径共用）

以下规则适用于 **所有** 执行路径（Part 1 通用流程和 Part 2 场景流程）。先读完全局约定，再进入 Step 0 路由判断。

### CLI 安装与配置

- MUST 仅通过 **npm 全局安装** 获得可执行命令 `smartbi`：`npm install -g @smartbi/cli@latest`，随后 `smartbi --version` 验证版本 **≥ 2.0.0**，并执行 `smartbi profile list --help` 确认 profile 命令族可用。
- MUST NOT 使用 `yarn` / `pnpm` / `bun` / `npx` 或其它程序代替上述 `smartbi`。
- 初始化 MUST：由 CLI 全参数生成配置：`smartbi init --server-type <sdk-server|smartbi> --base-url <url> --token <token> [--profile <name>]`；凭证方式按用户选择，可使用字面令牌、环境变量或钥匙串，细节见 `references/init.md`。
- 配置文件路径：默认 **`~/.smartbi/config.yaml`**，或用户在 init 后 **明确指定** 的 `--config <path>`。MUST NOT 在系统中猜测或套用其它文件。config.yaml 可包含多个环境（profiles），默认环境由 `profile:` 字段指定；多环境的选择、配置与错误处理见 `references/profiles.md`。
- CLI 不存在时的处理流程见 `references/init.md`「标准安装」。

### 环境选择（多 profile）

任务开始时在内部确定本次使用的 profile：用户指定连接或客户时按 `references/profiles.md` 匹配或新建，未指定时用默认 profile（config.yaml 的 `profile:` 字段）。普通业务对话不询问或展示 `dev`、profile 名、`--profile` 等内部配置；多个连接无法区分时只按服务器地址或用户熟悉的业务名称澄清。

环境确定后，**所有** `smartbi` 命令（`list`/`search`/`describe`/`call`/`doc`）**一律带 `--profile <name>`**。

完整规范（确定/告知/配置/错误处理/版本约束）见 `references/profiles.md`。

### 首次配置

仅在无配置或所选环境缺少必要信息时补齐配置。复用已知地址、服务器类型、环境名和有效凭证来源（字面令牌、环境变量或钥匙串），只询问缺失项，一次一个问题。已有地址但缺少/失效令牌时只处理凭证，不再推荐体验中心。已有配置的修复见 `references/init.md`，不得用全量初始化覆盖其他环境。以下完整流程用于首次无配置的情况：

1. **先问地址**：用户提供 SmartBI 地址 → `serverType: smartbi`。如果用户只表达“连接 SmartBI”或“连接 SmartBI 地址”但没有提供具体地址，第一问直接说：“是否连接 SmartBI 官网体验中心 https://cloud.smartbi.com.cn/smartbi？如果要连接自己的环境，请提供地址。”不得只问“要连接哪个环境”而遗漏体验中心选项；也不得在用户确认前将体验中心写入配置或发起连接。用户确认后使用该地址和 `serverType: smartbi`。用户拒绝或需要其他环境时，再询问实际 SmartBI 地址；用户无法提供 SmartBI 地址时，询问 SDK Server 地址并使用 `serverType: sdk-server`；两者均无法提供时暂停。
2. **再问令牌**：问令牌时一并说明获取路径和存储方式（仅一句）："请提供 SmartBI 个人访问令牌（登录 SmartBI 后，在「个人中心 → 我的设置 → 个人访问令牌」中新建）。令牌默认直接存进配置；如对安全有更高要求，也可以改用「环境变量」或「系统钥匙串」存储。"首次配置不再询问环境名；若用户选择其他存储方式，步骤 3 按其选择生成。
3. 执行 `smartbi init --server-type <sdk-server|smartbi> --base-url <地址> --token <令牌> [--profile <环境名>]`（不指定 `--profile` 时默认 `dev`；CLI 写盘 `~/.smartbi/config.yaml`，该环境同时为默认环境）。若用户选择其他存储方式：「环境变量」→ 以 `--token-env <VAR>` 替代 `--token`；「系统钥匙串」→ agent 无交互终端，使用当前 shell 的安全 stdin 管道传入令牌，并带 `--token-keyring --token-stdin`；不要把字面令牌写进命令历史（裸 `--token-keyring` 在无 TTY 下会直接失败）。
4. 配置成功后继续原业务请求；仅需区分多个连接或排错时，用服务器地址或用户熟悉的名称说明当前连接，不单独展示内部 profile 名。

`serverType` 取值约束（MUST）：只能是 `sdk-server` 或 `smartbi`，不得使用其他变体。

新增连接（追加写入、不动默认环境）的流程见 `references/profiles.md`「连接配置流程」。详细提问模板见 `references/init.md`。

### 参数构造规范

构造 `smartbi call` 的请求体时，按以下优先级确定取值来源：
1. **用户输入或上下文已知事实**：对话中已明确提供的值
2. **文档内容**（优先）：字段业务含义、合法枚举值、字段间依赖、完整使用示例（通过 `smartbi doc` 加载）
3. **`requestBodySchema`**（兜底）：文档不可用或未覆盖时使用
4. **`callParameterPlan`**：CLI 标志映射
5. **`suggestedCall`**：仅供参考的命令模板，不应直接复用其占位值
6. **仍无法确定的字段**：向用户确认，不得自行编造

若通用指南/示例与当前 operation 的 required、字段类型、枚举或外层包装冲突，结构以当前 operation 契约为准；业务语义冲突需进一步核实，不能盲从示例或猜测。

构造 call 参数时，应主动获取 `docs/specs/` 下的业务文档作为理论依据；文档不可用或未覆盖时，以 schema 定义兜底。已加载路径不重复加载。

**请求体文件规范（MUST）**：
- JSON 请求体必须使用 `-d @file.json`（避免跨 shell/OS 转义差异）
- MUST NOT 使用内联 JSON（如 `-d '{"k":"v"}'` 或 `-d "{\"k\":\"v\"}"`）
- 为本轮 `call` **新建**的 JSON 文件：在 `smartbi call` 流程结束后 **MUST** 删除；不得删除用户自带的 `@` 文件
- 临时文件优先写入当前运行环境可写、且 CLI 能解析的系统临时目录，结束时清理；Windows 上若 Git Bash 的 `/tmp` 路径报 `Body file not found`，改用 Windows 临时目录的绝对路径，不写死用户名；清理被权限阻止时报告残留位置与原因，不声称删除成功，不将请求、日志或结果写入 Skill 目录
- 写入请求体前，若有 Rhino 脚本等需转义的内容，MUST 使用 `scripts/inject-script.mjs` 工具，禁止手工转义

### 子任务机制

执行 `call` 前，若某些参数值依赖其他 `smartbi` 操作（如先查资源 ID、先创建关联对象），MUST 以子任务方式自动完成，**不得让用户手动查找**。

- 子任务执行路径：继承父任务已选场景。数据查询场景中已知 operationKey 的只读前置操作按该场景最短可验证调用链执行；其他前置操作绕过 Step 0 场景匹配，进入 Part 1 Phase 1→3 通用流程（`list` → `describe` → `call`）。完成后把结果填回父 call。
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

直接取数路径对用户优先展示业务答案、口径与结果范围；上述技术明细仅在排错、审计或用户要求时展示，不逐接口打断业务流程。

### Agent 与自定义工具操作

- 创建、导出或修改 Agent 工作流：读取 [references/agent-workflows.md](references/agent-workflows.md)。
- OpenAPI Provider、工具解析和绑定：读取 [references/custom-tools.md](references/custom-tools.md)。
- 标准 SDK 未覆盖时才按上述参考使用 `scripts/smartbi_internal.py`；修改前导出、备份和校验，修改后回读并验证。普通查询不会触发这些修改。

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
smartbi list --profile <name> --agent
```

1. 默认先执行 `smartbi list --profile <name> --agent`，将候选全集交给大模型做语义重排。
2. 若结果过大，先加 `--domain` / `--service` 再次 `list` 收敛。
3. 若候选唯一且语义明确匹配（用户意图与接口 summary 高度一致，无歧义）→ 直接进入 Phase 2，在 Phase 3 `call` 前向用户展示"准备调用 `<operationKey>`，参数如下…"做一次性确认。不要继续 search，也不要单独停下来等用户确认 operationKey。
4. 若候选唯一但语义匹配度存疑（摘要与意图不完全对应）→ 展示该候选给用户，等用户明确确认后进入 Phase 2。
5. 若存在多条疑似候选无法区分 → 仅对难以区分的候选调用 `smartbi search <operationKey> --profile <name> --verbose --agent` 获取详细信息以消歧。MUST NOT 对所有 Top-N 逐个 search。
6. `search` 的关键词检索仅作为补充回退手段（例如用户提供了明确关键词锚点时），不作为默认第一步。

Phase 1 定位约束（MUST）：
- MUST 默认使用 `list` 路径定位接口，不得先走 `search` 作为主路径。
- `search --verbose` 仅用于消歧，不得对每个候选盲目执行。
- 存在多候选时 MUST 等在候选阶段让用户选择，不得替用户拍板。唯一且明确匹配时可直接进入 Phase 2（在 Phase 3 call 前做一次性确认）。

细节见 `references/discovery.md`。

## Phase 2 — Contract

```
smartbi describe <operationKey> --profile <name> --agent
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

**步骤 2 — 加载与穿透**：对识别到的文档路径，执行 `smartbi doc <path> --profile <name> --agent`，stdout 纳入上下文。文档中的引用链接继续递归加载，硬限制：
- **深度 ≤ 3**（初始文档为深度 0），**去重**（已加载路径不重复）
- 绝对路径 `/...` → 直接传给 `smartbi doc`；相对路径 → 基于当前文档路径解析；外部 URL → WebFetch

**步骤 3 — 文档优先，schema 兜底**：按 [全局约定 · 参数构造规范](#参数构造规范) 的优先级规则取值。文档有定义时以文档为准，不可用时以 schema 兜底。

MUST NOT 忽略链接或自行猜测文档内容。细节见 `references/describe.md`。

## Phase 3 — Execute

```
smartbi call <operationKey> -d @body.json --profile <name> --agent
```
（`<name>` 为本次操作环境；所有命令一律带 `--profile`，见全局约定「环境选择」）

- 参数构造、请求体格式、临时文件清理等底层规则见 [全局约定 · 参数构造规范](#参数构造规范)
- 前置参数依赖的子任务机制见 [全局约定 · 子任务机制](#子任务机制)
- 重试策略与幂等门控见 [全局约定 · 重试与幂等](#重试与幂等)
- 复杂参数组合策略见 `references/strategy.md`

细节见 `references/call.md`。

## Phase 4 — Diagnose

失败后 `smartbi describe <operationKey> --profile <name> --agent`；仍有契约歧义再加 `--include-raw-schema`。
诊断策略参考 `references/strategy.md`。

# Part 2: Scenario Guides（场景索引）

**入口先走 Step 0 — Scenario Router。** 将业务操作问句与下表比对：
- 命中 → 加载对应场景文件，按场景流程执行
- 未命中 → Part 1 通用流程
- 加载后场景判定不适用 → 回退 Part 1

| 场景 | 关键触发词 | 场景文件 |
|------|-----------|---------|
| S1 定时计划任务 | 每天/每周/定时/cron + 查询/统计/推送/ETL | `scenarios/schedule-task.md` |
| S2 消息推送 | 发送/推送/通知 + 企微/钉钉/飞书/邮件 | `scenarios/push-message.md` |
| 数据查询与洞察（扩展） | 模型/已有报表取数、指标查询、比较、归因、报告分析 | [scenarios/data-query.md](scenarios/data-query.md) |

触发词仅用于快速匹配；精确判定由场景文件 `## 触发` 节负责。仅命中时才加载对应文件。

场景随 OpenAPI 的扩展可持续追加；新增场景按类型完成端到端验证后才可声明支持，尚未验收的分支须标明边界。

> **开发者**：扩展场景在 `scenarios/` 中声明触发条件与执行路径，通过本表挂接；复用 Part 1 和现有参考，不复制安装、鉴权或接口调用框架。

---

## 常见错误速查

### CLI / 连接类

| 错误 | 原因 | 处理 |
|------|------|------|
| `command not found` (127) / `is not recognized` | 未安装 CLI | → Phase 0 标准安装 |
| `AUTH_FAILED` (401) | token 无效或已过期 | 让用户重新申请令牌；用 `smartbi profile show <name>` 诊断凭证来源后更新配置 |
| `FORBIDDEN` (403) | 用户无权限执行该 operation | 检查 `x-funcPerm` 要求，确认用户角色 |
| `Plain token is disabled by allowPlainToken=false`（AUTH_FAILED） | 字面量 token 被 `allowPlainToken: false` 拦截（配置通常被外部改动过） | 按 init.md 修复凭证来源；保留该 profile 的其他设置和其他环境，不擅自改为明文或覆盖初始化 |
| `KEYRING_UNAVAILABLE` | 配置了 `tokenKeyring: true` 但系统钥匙串不可用（无头/无桌面会话） | 恢复钥匙串可用性，或按用户选择更换凭证来源；遵循 init.md 保留现有配置 |
| `NETWORK_TIMEOUT` / `NETWORK_ERROR` | 服务不可达 | 检查 `baseUrl` 是否正确，网络是否通 |
| `UPSTREAM_UNAVAILABLE` (503) | SmartBI 服务未启动或过载 | 确认服务状态后重试 |
| `Config file not found` (INVALID_ARGUMENT) | 配置文件不存在 | → Phase 0 init 流程 |
| `Config file is invalid`（INVALID_ARGUMENT，附逐条 `- 路径: 原因`） | 配置内容不合法 | 按逐条摘要修正字段，保留现有环境和自定义设置，不用重新 init 覆盖 |
| `PROFILE_NOT_FOUND` | 指定的环境不存在 | `smartbi profile list` 列出现有环境让用户选择，或按 `references/profiles.md` 新建 |
| `SpecRejected` / `path not in spec` | sdk-server 路径前缀错误 | 确认 `serverType` 与 `baseUrl` 配置一致 |

### API 业务类

| 错误 | 原因 | 处理 |
|------|------|------|
| `getDataModelTrees` 的空 `modelIds` 返回 `[]` | 空数组不是“列出全部模型” | 用目录枚举或搜索找到实际模型 ID，再取字段树 |
| MQL `没有找到层次字段` | `dims` 可能用了技术名或缺少模型要求的层级路径 | 对照当前字段树/模型契约，使用已核实的维度层级标识；不猜英文 `refColumn` |
| MQL `表未找到` / SQL `DAO_ID_IS_NULL` | `from`/`FROM` 可能用了物理表名，或模型视图未解析 | 先核对字段树中的来源别名；仍不足时按需读 `getDataSet` 的 `views` 并验证逻辑别名，不盲改字段或切换查询方式 |
| `选择字段不能为空` | dims/metrics 空或不匹配 | 先调 `getDataModelTrees` 确认字段 label |
| `Failed to obtain two-dimensional data` | `showDataTable: true` 不兼容某些模型 | 改为 `false`，下载 s3Url 产物并识别真实格式，不预设 Parquet |
| `unsupported literal in MQL filter` | MQL `:param` 占位符不兼容 | 改为字面量 `'值'`，内部单引号双写 |
| `connector.remoteInvoke` 报错 | RMI 签名不匹配 | 调 `getTaskScriptEnv` 查看可用方法 |
| HTTP 500 / `Internal Server Error` | 服务端异常 | 记录 `tid`，用 `describe --include-raw-schema` 排查请求体 |

---

## 参考（按需加载）

| 文件 | 内容 |
|------|------|
| `references/init.md` | 安装与配置 |
| `references/profiles.md` | 多环境（profile）规范：确定/告知/配置/错误处理 |
| `references/discovery.md` | Phase 1 接口发现 |
| `references/describe.md` | Phase 2 契约理解 |
| `references/call.md` | Phase 3 执行调用 |
| `references/strategy.md` | 策略与常见模式（Phase 3 构造复杂参数或 Phase 4 诊断时加载） |
| `references/rhino-template.md` | MQL 取数 Rhino JS 模板（定时任务场景共用） |
| `references/doc-index.md` | domain → 文档路径索引（Phase 2 文档加载时参照） |
| `scenarios/schedule-task.md` | S1 定时计划任务 |
| `scripts/inject-script.mjs` | 脚本注入工具：将多行 JS 文件自动 JSON 转义后注入请求体 |
