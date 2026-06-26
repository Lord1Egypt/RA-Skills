# `list` / `search` 参考

本文件为 **Smartbi CLI Skill** 的附属参考，仅规范 `list` / `search` 用法；流程性 MUST 以上级 `SKILL.md` 为准。

**用途**：Phase 1（Discover）— 在最小输出下定位唯一 `operationKey`。按需查阅，勿一次性展开全部条目。

## 共同约定

- `--json`：成功时 `stdout` 为单行 JSON；失败时 `stderr` 默认可为人类可读。
- `--yaml`：成功时 `stdout` 为 YAML 文档；失败时 `stderr` 默认可为人类可读。
- `--agent`：默认成功 `stdout` 为 YAML（`--stream` 下为 NDJSON），且失败时 `stderr` 必须输出结构化 JSON（字段以当前 CLI 与对应 `smartbi.cli.*.v1.schema.json` 为准）。
- 自动化流程默认优先使用 `--agent`；仅在下游明确要求 JSON 时使用 `--json`。
- `--verbose`：在列表项中追加较长字段（如 `description`、`tags`、`consumes`、`produces`）。
- `--with-version`：在每个结果项中附加 `apiVersion`。
- `--with-root-version`：在顶层结果中附加 `rootVersion`。
- `--refresh`：本次强制刷新 registry 缓存，优先级高于配置中的 `checkIntervalSeconds`。
- `--config <path>`：指定配置文件路径（默认 `~/.smartbi/config.yaml`）。

## `smartbi list`

**用途**：枚举当前缓存中的 operation，适合浏览 domain/service 范围。

| 选项                              | 说明                      |
| ------------------------------- | ----------------------- |
| `--domain <domain>`             | 仅列出该 domain             |
| `--service <service>`           | 仅列出该 service            |
| `--verbose`                     | 输出扩展字段                  |
| `--with-version`                | 每个 item 附加 `apiVersion` |
| `--with-root-version`           | 顶层附加 `rootVersion`      |
| `--refresh`                     | 强制刷新缓存                  |
| `--json` / `--yaml` / `--agent` | 见上                      |

**输出契约（机器校验）**：`smartbi-cli/schemas/smartbi.cli.list.v1.schema.json`。

**典型用法**：

```bash
smartbi list --agent
smartbi list --domain demo --service file --agent
smartbi list --verbose --with-version --with-root-version --agent
```

## `smartbi search <keyword>`

**用途**：按关键词检索 operation，适合从自然语言或片段定位 `operationKey`。

| 选项                                                                                                                  | 说明                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `--domain` / `--service`                                                                                            | 与 list 相同，缩小范围                                                                                                                   |
| `--in <fields>`                                                                                                     | 可重复；检索字段：`operationKey`、`operationId`、`summary`、`path`、`tags`、`description`、`requestBodySchema`、`responseSchema`（逗号分隔或多次 `--in`） |
| `--fuzzy`                                                                                                           | 模糊匹配                                                                                                                             |
| `--case-sensitive`                                                                                                  | 大小写敏感                                                                                                                            |
| `--limit <n>`                                                                                                       | 最大条数（默认 20）                                                                                                                      |
| `--verbose` / `--with-version` / `--with-root-version` / `--refresh` / `--json` / `--yaml` / `--agent` / `--config` | 同 list                                                                                                                           |

**输出契约（机器校验）**：`smartbi-cli/schemas/smartbi.cli.search.v1.schema.json`。

**典型用法**：

```bash
smartbi search getAgentItems --in description,operationKey,operationId --agent
smartbi search order --in operationKey,summary --in description,operationKey,operationId --agent
smartbi search "支付" --in description,tags --fuzzy --limit 10 --agent
```

## 与 Skill 流程的衔接

- Phase 1 默认优先 `list` 并让大模型做候选重排；结果过大时先追加 `--domain` / `--service` 收敛。
- 候选唯一且语义明确匹配（意图与接口 summary 高度一致，无歧义）时，直接进入 Phase 2，在 Phase 3 `call` 前向用户展示"准备调用 `<operationKey>`，参数如下…"做一次性确认，无需单独暂停等用户确认 operationKey。
- 候选唯一但语义匹配度存疑时，展示候选给用户等明确确认后再进入 Phase 2。
- 仅在有多个疑似候选难以区分时，才对疑似候选调用 `smartbi search <operationKey> --verbose --agent` 以消歧。
- `search` 的关键词检索不作为默认第一步，仅在需要关键词锚点补充定位或消歧时使用。
- 若经消歧后仍存在多个候选 `operationKey`，必须先让用户选择，再进入 `describe`。
- 选定唯一 `operationKey` 后进入 Phase 2（`describe`），见 `references/describe.md`。

`search` 回退门禁（MUST）：

- `smartbi search` 仅作补充回退，不得替代默认 `list` 主路径。
- `search` 的 `<keyword>` 必须是短关键词，不得是整句业务问句。
- 若 `search` 0 命中，优先回到 `list` 路径并结合 `--domain` / `--service` 收敛。

检索字段门禁（MUST）：

- `smartbi search` 检索候选时，必须至少包含：`--in description,operationKey,operationId`
- 若用户额外指定其它 `--in` 字段，仍必须保证上述三字段必在

反例 / 正例：

```bash
# 反例（整句问句，命中率低）
smartbi search "大模型问句 交易记录数 交易金额 近3年" --in description,operationKey,operationId --agent

# 正例（拆解为短关键词，分批检索）
smartbi search "交易记录" --in description,operationKey,operationId --agent
smartbi search "交易金额" --in description,operationKey,operationId --agent
smartbi search "近3年" --in description,operationKey,operationId --fuzzy --agent
```

## 未命中处理（list 重排或 search 检索 0 候选时 MUST）

一旦 0 候选，MUST：

1. 向用户如实反馈。话术："在当前接口列表中未能匹配到与'<用户意图摘要>'直接对应的操作。"
2. 让用户提供更具体的业务关键词或场景说明，然后重新执行 Phase 1。
3. MUST NOT 在 0 候选时强行猜测一个不相关的 `operationKey`，不得进入 `describe` / `call`。

## 检索异常分支（LLM 友好）

- `search` 0 个候选：先放宽检索（`--fuzzy`、调整 `--in` 字段、缩短关键词），再检索一次。若仍 0 候选 → 按上节「未命中处理」执行。
- >5 个候选：优先追加 `--domain` / `--service` / `--limit 5` 收敛，再让用户选择。
- 多候选未收敛：必须进入“用户选择模板”，不得跳过。

## 默认策略：list 重排 → 消歧时 search 详查 → 用户确认

Discover 阶段默认执行：

1. 先执行 `smartbi list --agent`。
2. 将 `list` 返回的候选全集交给大模型做语义重排，产出 Top-N 候选 `operationKey`。
3. 若候选唯一且语义明确匹配（意图与 summary 高度一致）→ 直接进入 Phase 2，在 Phase 3 `call` 前做一次性展示确认（"准备调用 X，参数如下…"）。不要继续 search，也不要单独停下来等用户确认。
4. 若候选唯一但语义匹配度存疑 → 展示该候选，等用户明确确认后进入 Phase 2。
5. 若存在多条疑似候选无法区分 → 仅对**难以区分的候选**调用 `smartbi search <operationKey> --verbose --agent` 获取详细信息以消歧。MUST NOT 对所有 Top-N 逐个 search。
6. 消歧后仍有多条 → 按"用户选择模板"让用户确认。不得直接替用户拍板。
7. 若 list 重排后**无候选匹配用户意图** → 按「未命中处理」执行。

建议：

- 若结果过大，优先先加 `--domain` / `--service` 再 `list`，避免一次性灌入过多噪音。
- `search` 仅用于消歧，不应作为必经步骤对每个候选执行。
- `search <operationKey> --verbose --agent` 的详细输出可提供比 `list` 摘要更丰富的判断依据，仅用于消歧场景。

## 多候选时的用户选择模板

当候选 `operationKey` 大于 1 时，按以下最小信息展示给用户选择（不要直接替用户决定）：

```text
我找到了多个候选 operationKey，请选择一个：
1) <operationKey> | <method> <endpoint> | <summary>
2) <operationKey> | <method> <endpoint> | <summary>
3) <operationKey> | <method> <endpoint> | <summary>
...
请回复序号或完整 operationKey。
```

展示约束：

- 每个候选至少包含：`operationKey`、`method`、`endpoint`、`summary`。
- 默认最多展示前 5 个；若超过 5 个，先提示可追加筛选条件（如 `--domain` / `--service` / `--in` / `--limit`）再继续收敛。
- 用户未明确选择前，不得进入 `describe` 或 `call`。

## 首次环境（`init`）

无有效配置时，须先完成初始化再执行 `list` / `search`。  
完整安装、`init` 与配置要求见：`references/init.md`。

