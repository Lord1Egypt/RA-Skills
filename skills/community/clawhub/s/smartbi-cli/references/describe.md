# `describe` 参考

本文件为 **Smartbi CLI Skill** 的附属参考；流程性 MUST 以上级 `SKILL.md` 为准。

**用途**：Phase 2（Contract）与 Phase 4（Diagnose）— 读取契约与诊断信息。按 Skill 要求，**默认只消费最小字段集**；其余字段仅在升级诊断时查阅。

## 命令形式

```bash
smartbi describe <operationKey> [--json] [--yaml] [--agent] [--include-raw-schema] [--refresh] [--config <path>]
```


| 选项                     | 说明                                                                       |
| ---------------------- | ------------------------------------------------------------------------ |
| `--json`               | 成功时 `stdout` 单行 JSON；失败时 `stderr` 默认可为人类可读                               |
| `--yaml`               | 成功时 `stdout` 输出 YAML 文档；失败时 `stderr` 默认可为人类可读                     |
| `--agent`              | 默认成功 `stdout` 为 YAML，失败时 `stderr` 必须输出结构化 JSON；成功体可含 Agent 侧重字段（见下节） |
| `--include-raw-schema` | 附加 `requestBodySchemaRaw`、`responseSchemaRaw`（保留 OpenAPI 侧 `$ref` 等，供调试） |
| `--refresh`            | 强制刷新 registry 缓存                                                         |
| `--config`             | 配置文件路径                                                                   |


## Phase 2 必读字段（与 Skill 对齐）

执行 `describe --agent` 后，消费以下字段：

- **`callParameterPlan`**：path/query/header/cookie/body 分组与 CLI 示意；无某类参数时，对应键可能省略（仅 `body`、`checklist` 恒在）。
- **`requestBodySchema`**：请求体结构（仅 body，不含 path/query/header）；与 `callParameterPlan` 共同约束如何组 `call -d` / `-F`。
- **`consumes` / `produces`**：媒体类型。
- **`suggestedCall`**：单行命令模板（占位符与示例，**不能替代**用户对未知字段的确认）。

字段值规则仍以主 Skill 为准：**用户输入或上下文已知事实优先；其次以文档为依据，schema 兜底**（详见主 Skill「文档优先级原则」）。

## 文档加载（优先获取，不可用时兜底）

`describe` 完成后，应主动按主 Skill Phase 2「文档加载」步骤 1 识别文档来源，通过 `smartbi doc <path> --agent` 加载并递归穿透。文档有定义时以其为基准理解 schema；文档不可用或未覆盖的字段，直接使用 schema。

文档路径索引见 `references/doc-index.md`，各 domain 的主要文档目录可从该文件快速定位。

**递归限制（MUST）**：
- 递归深度 ≤ 3 层（初始文档为深度 0，最多穿透到深度 3）。
- 已加载路径（绝对路径规范化后）不重复加载，防止循环引用。
- 超出深度的链接在当前上下文中跳过，不报错。

## `--agent` 额外字段（诊断与摘要）

在 `--agent` 成功响应中，通常还包含（具体以当前 CLI 与 `smartbi-cli/schemas/smartbi.cli.describe.v1.schema.json` 为准）：

- `summary`、`description`、`requiredAll`、`llmBrief`、`constraintsHints`
- 以及 `idempotent`、`deprecated` 等元信息

用于压缩上下文下的理解与排错，**不替代**完整 `requestBodySchema`。

## Phase 4 升级

1. 先根据调用失败结构中的 `code`、`status`、`hint`、`details` 等定位（见主 Skill）。
2. 需要更紧凑的必填与约束提示时，使用 **`describe <operationKey> --agent`**。
3. 仅在仍有契约歧义时，使用 **`describe <operationKey> --agent --include-raw-schema`**。

## 输出契约（机器校验）

- `smartbi-cli/schemas/smartbi.cli.describe.v1.schema.json`

与 CLI 行为或 schema 不一致时，以**当前安装的 `smartbi describe --help` 与上述 schema 文件**为准。
