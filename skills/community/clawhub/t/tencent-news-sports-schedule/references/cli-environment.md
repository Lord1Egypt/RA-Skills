# CLI 环境与失败处理

所有使用腾讯新闻 CLI 的 Skill 共用本流程。执行任何业务调用前读取；环境异常时，本流程优先于业务 Markdown 原文、仅输出 HTML、隐藏技术细节等格式要求。成功时继续遵守各 Skill 的业务规则。

## 入口与状态

在安装后的 Skill 根目录（包含 `SKILL.md`）执行，或使用该目录下脚本的绝对路径。源码目录需先打包补齐共享资源，不能把包装脚本缺失误判为 CLI 未安装。

| 平台 | 状态检查 | 业务调用 |
|---|---|---|
| macOS / Linux | `sh scripts/cli-state.sh status` | `sh scripts/run-cli.sh <command> [args]` |
| Windows | `powershell scripts/cli-state.ps1 status` | `powershell scripts/run-cli.ps1 <command> [args]` |

- `run-cli` 无参数、`-h`、`--help` 显示本地帮助并退出 0，无需 CLI 或 Key；`run-cli help` 在 CLI 可用时返回实际帮助，未安装时只显示本地用法，不能据此猜测业务命令。
- `cli-state` 无参数或 `status` 输出 JSON；`help`、`-h`、`--help` 显示本地用法。
- 检查 `success`、`status`、`error.code`、`cliExists`、`platform.cliSource`、`apiKey.status`、`update.needUpdate`。退出 0 只表示诊断执行完成；`ready` 只证明本地检测到 CLI 和 Key，不证明远端鉴权或业务成功。
- 除状态检查外，所有 CLI 调用走 `run-cli`，保留真实退出码。共享脚本仅注入当前 Skill 的 caller，不代填业务参数。

## 恢复流程

保持同一运行账号、PATH、HOME、安装目录、shell 和凭证上下文；新建目录、解压或切换源码不代表环境失效。已有本会话的有效状态可复用，发生鉴权错误或环境变化后重新检查。

1. **检查状态**：执行上表对应平台的状态命令。包装脚本缺失、执行失败或 JSON 无法解析时先核实完整包和脚本解释器，不能直接判为 CLI 未安装。
2. **缺少 CLI**：仅状态脚本确认 `cliExists: false` 时安装。`command not found` 可能只是 PATH 未命中；脚本还会检查固定安装目录。macOS / Linux：`curl -fsSL https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.sh | sh`；Windows：`irm https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1 | iex`。安装后在当前对话复查，无需让用户重开终端、重新提问；失败时提供 [安装指南](installation-guide.md)，不循环重装。
3. **需要更新**：`update.needUpdate: true`、CLI 明确提示版本过旧或当前帮助不支持所需能力时，按 [更新指南](update-guide.md) 更新并重新读帮助。测试环境先核实 `run-cli version` 的下载渠道；若指向 `/hub/`，不要执行会切回正式构建的更新，使用已核实的测试构建及同渠道校验文件。不能仅凭安装脚本位于 `/test/` 或版本号相同就认定构建正确；来源不明时说明缺口，不猜下载地址。
4. **Key 缺失先核实**：`apiKey.status: missing` 不等于用户从未配置。macOS / Linux 可执行以下命令，只列出配置文件名，不读取或记录 Key 值：

   ```sh
   grep -l TENCENT_NEWS_APIKEY ~/.zshrc ~/.zprofile ~/.bash_profile ~/.bashrc ~/.profile 2>/dev/null
   ```

   若命中，先按对应 shell 复查，例如 `SHELL=/bin/zsh sh scripts/cli-state.sh status`（`.zshrc` / `.zprofile` → zsh，`.bash_profile` / `.bashrc` → bash，`.profile` → sh）。CLI 可能按 `SHELL` 选择不同 RC 文件；无 `SHELL` 时可能读 `.profile`。命中只说明文件中出现变量名，不证明 Key 有效；以复查结果为准。成功后对所有后续 CLI 调用保持相同前缀；仍缺失则说明配置存在但当前进程未能读取，核实运行账号与 CLI 配置，不重复 `apikey-set`，不读取整份 RC、不自动 source 配置。Windows 不执行上述 POSIX 检查，保持原账号及 CLI 环境，用 `.ps1` 状态脚本复查。

   确认缺失后，引导用户访问 [API Key 获取页面](https://news.qq.com/exchange?scene=appkey)，由凭证持有人在**执行查询的同一设备或沙箱账号**的终端运行 `tencent-news-cli apikey-set YOUR_KEY`。`YOUR_KEY` 只供用户本地替换；不要索要、代填、回显或记录真实 Key，不自动打开浏览器。智能体只用 `cli-state status` 验证，不直接执行 `apikey-get` 或带真实 Key 的 `apikey-set`。只有用户明确要求时才清除 Key。
5. **鉴权失败或状态不明**：本地 `ready` 后的真实业务调用仍可能返回 401、403、无效/过期 Key 或 `verifyAPIKey failed`。这些都按下表处理，不解释为无数据或额度耗尽；其他未知错误不要猜原因。安装、更新或用户配置完成后可在同一对话复查并继续原问题。

远端沙箱不允许安装、配置凭证或联网时，说明具体限制及需要平台提供的条件，不能承诺在用户个人电脑配置就能恢复沙箱。更多手动操作见 [Key 配置指南](env-setup-guide.md)。

恢复环境不等于授权重试。是否重发业务请求、恢复分页或启动新查询，仍遵守目标能力的单次调用、重试及用户授权约束；例如高考推荐分页失败后不能续跑旧请求或重复 start，须按高考流程等待下一轮明确查询。

## 环境失败结果

本轮无法恢复时停止依赖 CLI 的业务调用，最终回复包含下面的 JSON 和对应平台的具体恢复步骤。按实际 Skill/能力填写 `capability`，按实际问题填写 `query`，输入含凭据先脱敏；不要照抄占位符。`data: null` 仅表示未取得业务结果，不代表命题为假、没有比赛、无预警、检索无证据或额度用完。

```json
{
  "success": false,
  "status": "environment_not_ready",
  "capability": "<本次能力>",
  "query": "<脱敏后的实际问题>",
  "data": null,
  "error": { "code": "CLI_NOT_INSTALLED", "message": "当前未检测到腾讯新闻 CLI，尚未执行业务查询。" },
  "nextSteps": ["按当前平台安装 CLI，然后重新检查环境。"]
}
```

| 已核实的原因 | error.code | 恢复步骤 |
|---|---|---|
| 状态脚本确认 CLI 不存在 | `CLI_NOT_INSTALLED` | 给出对应平台安装命令并复查 |
| 当前进程未检测到 Key | `API_KEY_MISSING` | 先排除 shell/账号差异，确实缺失再提供获取页面和本地配置命令 |
| 明确的 401/403、无效 Key、鉴权失败 | `API_KEY_UNAUTHORIZED` | 由用户在运行环境重新配置有权限且渠道匹配的 Key，再检查 |
| 包装脚本缺失/不可执行、诊断无法解析或其他环境错误 | `ENVIRONMENT_CHECK_FAILED` | 核实完整包、解释器、CLI 与配置，说明尚未确认的环节 |

只陈述脱敏后的已知原因，不展示原始错误、内部日志、traceid、Key 或凭证。不能用模型记忆、示例或其他数据源补业务结果；环境失败优先于额度、空结果、通用“数据加载失败”等业务话术，不生成假结果 HTML。帮助、诊断或打包通过均不等于真实业务或平台复审通过。

失败结果不附成功来源标识或订阅引导。复合请求仅标记失败的能力，并保留已成功获取的结果，不把部分成功改写成全部成功或全部无数据。
