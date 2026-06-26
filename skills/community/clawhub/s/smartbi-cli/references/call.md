# `call` 参考

本文件为 **Smartbi CLI Skill** 的附属参考；流程性 MUST 以上级 `SKILL.md` 为准。

**用途**：Phase 3（Execute）— 在已明确 `operationKey` 与参数来源的前提下发起 HTTP 调用。参数与 body **必须与** `describe` 中的 `callParameterPlan` 与 `requestBodySchema` 一致；未知字段值须先向用户确认。

自动化流程默认优先使用 `--agent`；仅在下游明确要求单行 JSON 时使用 `--json`。

## 参数构造依据（文档优先，schema 兜底）

构造每个字段的值时，按以下优先级确定取值来源：

1. **用户输入或上下文已知事实**：用户在对话中已明确提供的值
2. **文档内容**（优先）：Phase 2 加载的文档中定义的合法枚举值、字段语义、组合约束、完整示例
3. **`requestBodySchema`**（兜底）：文档不可用或未覆盖时，以 schema 的字段类型约束、必填/可选为准
4. **`callParameterPlan`**：CLI 标志映射
5. **`suggestedCall`**：仅供参考的命令模板，不应直接复用其占位值

文档有定义时以其为准，文档未覆盖时以 schema 为准；不应仅看字段名猜测语义或编造值。

## 命令形式

```bash
smartbi call <operationKey> [选项...] [--json|--yaml|--agent]
```

## 常用选项


| 选项                      | 说明                          |
| ----------------------- | --------------------------- |
| `--profile <name>`      | 使用配置中的指定 profile            |
| `-d, --data <json>`     | JSON 请求体；**必须**使用 `-d @file.json`（将 JSON 写入文件后传入 @ 路径） |
| `-F, --form <k=v\|k=@file>` | multipart 字段（可重复）      |
| `--path <k=v>`          | 路径参数（可重复）                   |
| `--query <k=v>`         | 查询参数（可重复）                   |
| `--header <k=v>`        | 请求头（可重复）                    |
| `--timeout <ms>`        | 超时（毫秒）                      |
| `--dry-run`             | 仅打印请求预览，不发送网络请求             |
| `--idempotent`          | 允许对**写请求**按策略自动重试（须业务上可幂等）  |
| `--stream`              | 流式响应（如 SSE）                 |
| `--stream-format <fmt>` | 流式解析提示（保留/按实现）              |
| `--max-events <n>`      | 流式最多处理事件/块数                 |
| `-o, --output <path>`   | 二进制响应写入文件                   |
| `--stdout`              | 二进制响应写入标准输出                 |
| `--refresh`             | 强制刷新 registry 缓存            |
| `--json` / `--yaml` / `--agent` | 与 list/search/describe 相同约定 |
| `--config <path>`       | 配置文件路径                      |


## 与 `describe` 的对应关系

- `--path` / `--query` / `--header`：与 `callParameterPlan` 中各分组的 `name`、`cli` 一致。
- `-d`：在 `body.kind === json` 且 `consumes` 含 JSON 类类型时使用；**必须**使用 `-d @file.json`，JSON 内容须满足 `requestBodySchema`。
- MUST NOT 使用内联 JSON（如 `-d '{"k":"v"}'` 或 `-d "{\"k\":\"v\"}"`）。
- `-F`：在 `body.kind === multipart` 时使用；文件字段遵循 schema 中 `format: binary` 等约定。
- **无 body**：`body.kind === none` 时不要强行带 `-d`/`-F`（除非 OpenAPI 另有约定且已在 describe 中体现）。

## 临时请求体文件（`-d @data.json` 等）的生命周期（MUST）

- 由代理/自动化**为本轮 `call` 新建**的 JSON 文件（例如 `data.json`、`*-body.json`）：在 **`smartbi call` 整段流程结束**后（含成功、失败、dry-run、重试耗尽）**MUST** 删除该文件，除非用户**明确要求保留**（例如留档审计）。
- MUST NOT 在任务收尾后长期遗留含业务参数或可能含敏感字段的临时 JSON；优先写入系统临时目录，或仓库内已 `.gitignore` 的路径，降低误提交风险。
- 若 `-d @` 指向的是**用户已有文件**（非本轮创建），MUST NOT 擅自删除。

## 成功响应中可观测字段

自动化场景下，除 HTTP 语义外，成功 JSON 中常关注：

- `status`：HTTP 状态码
- `tid`：追踪标识（若存在）
- `data`：业务载体；失败或业务错误时可能含 `data.success`、`data.error`（与 Phase 4 诊断字段一致）

具体形状以 `smartbi-cli/schemas/smartbi.cli.call.v1.schema.json` 与当前实现为准。

## 重试与幂等（与 CLI 实现对齐）

- **写方法**：`POST`、`PUT`、`PATCH`、`DELETE` 视为写请求。
- **是否允许写请求自动重试**：仅当 `--idempotent` 传入，或 describe 元数据中 `idempotent === true`（通常来自 OpenAPI `x-idempotent`）时，写请求才可进入与读请求相同的重试路径；否则写请求 **最多尝试 1 次**。
- **重试次数**：允许重试时，最多 **3 次** 尝试（含指数退避与抖动）。
- **可因 HTTP 状态触发的重试**（在仍有剩余次数时）：**429**、**502**、**503**。
- **网络类错误**：在 CLI 判定为可重试的网络超时/错误时，同样可在上述次数内退避重试。
- **代理义务**：不得对非幂等写请求假设可安全重放；须满足主 Skill 的幂等门控后再依赖 `--idempotent` 或元数据 `idempotent`。

## 前置条件与子任务（MUST）

执行 `call` 前，若 Phase 2 的 `describe` 输出表明某些参数值**无法由用户直接提供**，而需要先调用其他 smartbi 操作获取（例如：创建资源后得到 ID、查询列表后选取条目），则属于前置条件。

处理流程：

1. 识别前置条件：从 `callParameterPlan` 与 `requestBodySchema` 中判定哪些必填参数的值依赖其他 smartbi 操作。
2. 创建子任务：子任务内容为再次发动 `smartbi-cli` 技能，以用户原始业务意图描述该前置操作，获取所需的参数值。
3. 等待子任务完成，将返回结果填入当前 `call` 的参数。
4. 所有前置条件满足后，继续执行当前 `call`。

约束：

- MUST NOT 跳过前置条件直接用占位值/假值发起 `call`。
- MUST NOT 要求用户手动去查找前置数据（用户不知道接口映射关系），而应通过子任务自动完成。
- 若前置子任务失败，应向用户报告失败原因并暂停当前 `call`。

### 退出机制（MUST）

为防止无限递归或子任务爆炸，子任务链受以下硬限制保护。任一限制触发时，MUST 立即停止所有自动化子任务处理，执行**用户升级流程**。

**术语定义：**

- **调用链**：从原始 `call` 到当前深度的全链路所有节点（含兄弟子任务）。同一调用链内的已完成结果可跨节点复用。
- **参数意图**：子任务所要获取的具体参数值及其用途描述（如"查询项目A的ID"与"查询项目B的ID"属于不同参数意图，即使使用同一 operationKey）。

**硬限制：**

| 限制项 | 阈值 | 作用域 | 说明 |
|--------|------|--------|------|
| 深度上限 | ≤ 3 | 全链路 | 原始 `call` 为深度 0，每嵌套一层子任务深度 +1 |
| 数量上限 | ≤ 5 | 每个父 call | 单个父 call 最多产生 5 个直接前置子任务 |
| 去重 | 复用 | 同一调用链 | 同一 `operationKey` + 相同参数意图的前置操作已完成时，直接复用结果，不重复发起 |

**用户升级流程（触发任一硬限制时 MUST 执行）：**

1. 停止所有子任务处理，不继续发起新的 `smartbi call`。
2. 向用户输出以下信息：
   - **触发原因**：说明触发了哪条限制（深度/数量/重复），当前计数是多少。
   - **前置条件清单**：列出当前 `call` 所有已识别但尚未满足的前置参数，格式为「参数名：需要什么值（可通过哪个 operationKey 获取）」。
   - **已完成的前置结果**：列出已通过子任务成功获取的参数名及其值，供用户参考和复用。
3. 请用户选择后续操作：
   - 直接提供缺失参数的值（推荐）
   - 指定其中部分前置条件继续自动处理
   - 跳过某个非必填的前置条件
4. MUST NOT 在用户未响应前自行继续。

### 深度追踪（MUST）

每次发动子任务时，MUST 在子任务 prompt 中显式标注当前深度。子任务 prompt 模板：

```
[前置子任务 | 深度 {N}/3] 为父操作 "{parentOperationKey}" 获取参数 "{paramName}"。
用户原始意图：{userIntent}。
完成后将获取到的值返回，填入父 call 的 {paramName} 字段。
```

若子任务识别到自身已达到深度上限（深度 = 3）且仍需进一步前置操作，MUST 立即触发用户升级流程而非继续嵌套。

## 输出契约（机器校验）

- `smartbi-cli/schemas/smartbi.cli.call.v1.schema.json`

与 CLI 行为或 schema 不一致时，以**当前安装的 `smartbi call --help` 与上述 schema 文件**为准。