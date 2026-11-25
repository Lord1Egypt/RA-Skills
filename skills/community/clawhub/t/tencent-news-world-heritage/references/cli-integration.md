# CLI 接入：`tencent-news-cli wiyun`

本文件记录本 skill 依赖的 CLI 能力的核实结果。执行业务调用前先读本文件；具体命令、参数与输出仍以当次 `help wiyun` 为准。

## 工具与来源

- 可执行名称：`tencent-news-cli`（Windows 为 `tencent-news-cli.exe`），子命令 `wiyun`。
- 用途：文遗云图知识库问答，`help wiyun` 自述为「基于星辰后台「文遗云图·知识库」智能体检索并生成回答」。
- 后端智能体：星辰后台「文遗云图·知识库」，智能体 ID `UTR2026063018255100`；本 skill 通过 CLI 调用，不直接访问智能体接口。
- 适用系统：macOS / Linux / Windows，随 CLI 构建分发；本 skill 通过共享的 `scripts/run-cli.sh`（或 `run-cli.ps1`）调用。

## 安装与版本

- 安装与更新按包内 [`installation-guide.md`](installation-guide.md) 与 [`update-guide.md`](update-guide.md)，检测用 `sh scripts/cli-state.sh status`。
- **已验证可用构建**：`v1.0.18`，`build_date` 为 `2026-10-21T11:14:45`，`version` 返回的下载根地址为 `https://mat1.gtimg.com/qqcdn/qqnews/cli/test`（即 **test 渠道构建**）。
- **最低支持版本未知**：未对 v1.0.18 之前的构建做过探测，不推断更早版本是否包含 `wiyun`。判断方式是实际执行 `sh scripts/run-cli.sh help wiyun`，帮助中存在该子命令才算具备能力；仅凭版本号或 `need_update: false` 不能证明。

## 下载渠道

| 项目 | formal（hub） | test |
|---|---|---|
| CDN 根地址 | `https://mat1.gtimg.com/qqcdn/qqnews/cli/hub` | `https://mat1.gtimg.com/qqcdn/qqnews/cli/test` |
| SHA-256 清单 | `https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/checksums.txt` | `https://mat1.gtimg.com/qqcdn/qqnews/cli/test/checksums.txt` |
| API Key 获取页 | `https://news.qq.com/exchange?scene=appkey` | `https://test.news.qq.com/exchange?scene=appkey&testApi=1` |
| 消耗流水 | `https://news.qq.com/exchange?scene=points` | `https://test.news.qq.com/exchange?scene=points&testApi=1` |

平台与架构的完整下载清单见 [`installation-guide.md`](installation-guide.md)。

**未验证项**：`wiyun` 是否存在于 **formal（hub）渠道**的当前构建。本文件所有实测均来自 test 渠道的 v1.0.18；正式发布前需另行核实 hub 构建的帮助输出。

## 身份与配置

- 环境变量 / 配置项：`TENCENT_NEWS_APIKEY`，由用户通过 `tencent-news-cli apikey-set <KEY>` 写入本机配置；智能体只通过 `scripts/cli-state.sh status` 检查状态，不执行 `apikey-get`、不读取或回显明文 Key。
- 配置排查规则见 [`env-setup-guide.md`](env-setup-guide.md)：`SHELL` 为空读 `~/.profile`，bash 读 `~/.bash_profile`，zsh 读 `~/.zshrc`。
- 本能力为单独计费服务，可能受账号额度限制；额度不足与鉴权失败要分开报告，不把任一类错误推断为「无数据」。

## 调用契约

```
tencent-news-cli wiyun [查询内容] [flags]
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| 位置参数 `[查询内容]` | string | 二选一 | 空 | 可直接传入查询内容，与 `--query` 等价；两者都不传时报错 |
| `--query` | string | 是（与位置参数二选一） | 空 | 查询内容，例如 `--query "乐山大佛"` |
| `--format` | string | 否 | `text` | `text`：回答文本（末尾可能附带 traceid 诊断行）；`json`：输出接口完整响应 |
| `--caller` | string | 由脚本注入 | — | **禁止手动传入**，`run-cli` 会按 `SKILL.md` 的 `name` 与 `version` 自动注入 |

约束：查询内容为空字符串时，CLI 直接输出「缺少必填参数」并打印用法，不发起远端调用。

## 输出契约

- `text`（默认）：stdout 输出回答正文（Markdown 文本），末尾可能附带独立的 `traceid: <追踪标识>`（或中文冒号）诊断行。退出码 0 时，展示前按 SKILL.md 的 Phase 4 仅剥离该末尾诊断行，保留其余正文原文；剥离后为空不算有效回答。
- `json`：stdout 输出 OpenAI 风格的单个响应对象，已核实字段：

  | 字段 | 说明 |
  |---|---|
  | `object` | 固定为 `chat.completion.chunk` |
  | `id` | 本次响应 ID |
  | `session_id` | 会话 ID，多轮追问时可作为上下文标识 |
  | `model` | 后端实际模型标识，例如 `hy3` |
  | `created` | 响应时间戳 |
  | `choices[0].delta.content` | 回答正文，与 text 模式内容一致 |
  | `choices[0].finish_reason` | 结束原因，正常为 `stop` |
  | `usage` | token 统计（实测为 0，不作为计费依据） |

- 失败/参数错误：错误信息与用法输出到 stdout 与 stderr，退出码非 0；不输出业务正文。
- 无已知的 `wiyun` 专属错误码；鉴权、权限、网络等错误按 [`cli-environment.md`](cli-environment.md) 的统一分类处理。

## 失败处理

- 缺少查询内容：补齐 `--query`，仅在用户重新发起提问时再调用，不自动重试或猜测意图。
- 401 / 403 / 无效或过期 Key：按 `API_KEY_UNAUTHORIZED` 处理，由用户在运行环境重新配置渠道匹配的 Key。
- 未安装 CLI、Key 缺失：按 `CLI_NOT_INSTALLED` / `API_KEY_MISSING` 处理。
- 成功返回但正文与问题无关：如实说明未查到对应内容，不用其他数据源补答案。

## 操作影响

- 只读查询：不写入业务数据、不发消息、不发布内容、不删除任何资源。
- 每次调用会消耗对应账号的查询额度；本能力单独定价，重复调用会重复计费，因此遵守 SKILL.md 中的调用预算（单次提问不超过 3 次）。

## 最小调用

```sh
sh scripts/run-cli.sh help wiyun
sh scripts/run-cli.sh wiyun --query "乐山大佛"
```

预期：`help wiyun` 输出子命令说明与 `--query` / `--format` 参数；第二条返回乐山大佛相关的正文回答。

## 验证证据

- 2026-10-27 在平台已配置的 test CLI（`v1.0.18`，build 2026-10-21）上执行 `help`、`version`、`wiyun "乐山大佛"`（text）、`wiyun --query "乐山大佛" --format json`，均成功返回，正文非空，JSON 字段与上表一致。
- 同日执行 `wiyun --query ""`：按预期输出「缺少必填参数」与用法，非静默成功。
- **未验证**：formal（hub）渠道构建是否包含 `wiyun`；v1.0.18 之前版本的支持情况；该能力的计费/额度规则（仅知需求单标注「单独定价」）。
- CLI 侧变更来源（实现该子命令的 MR / 提交 / 发布说明）尚未取得，`skill.json` 的 `cli.changeRef` 待补。
