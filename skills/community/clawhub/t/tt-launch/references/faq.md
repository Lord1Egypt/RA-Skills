# 常见问题与环境配置

> **何时读**：排障、配 TOKEN、查落盘或 Windows 拼参时再读。日常执行不必每次打开。

## 环境

- Node.js 16.14.0+，Windows / Linux / macOS；必需环境变量 `GUAIKEI_API_TOKEN`（16–256 位字母、数字、下划线或连字符）。
- Windows cmd：`set GUAIKEI_API_TOKEN=你的TOKEN`
- Windows PowerShell：`$env:GUAIKEI_API_TOKEN="你的TOKEN"`
- Linux/macOS：`export GUAIKEI_API_TOKEN=你的TOKEN`

## Windows 引号 / 拆参

Agent 在 Windows 上最常见的失败不是业务错，而是 **shell 把参数拆坏**，技能报 `INVALID_ARGS` / `INVALID_KEYWORD` / `INVALID_URL`。

**硬规则**

- **cmd.exe：只用双引号** `"` 包含空格、中文、URL 的参数；**不要用单引号** `'`。
- PowerShell：含空格/中文参数也优先双引号；勿照搬 bash 单引号去 cmd。
- **Windows / 弱模型优先 `--json-args`**：业务字段放进一个 JSON 对象；**不可**与传统 flag 混用。
- 关键词以 `-` 开头：写成 `--keyword=-AI`，或 `node scripts/tiktok/search-cli.js -- -AI`，或 JSON 里 `"keyword":"-AI"`。

**症状 → 处理**

| 症状 | 先做什么 |
| --- | --- |
| `INVALID_ARGS` / 参数解析错误，且命令里有空格中文或 URL | 整段改成双引号包参数后 **只重试一次**；仍失败 → `--json-args` |
| 关键词被拆成多段、或 URL 的 `?`/`&` 丢失 | 同上；或直接 `--json-args` |
| 混用了 bash 示例里的单引号 | 全部换成双引号，或改用 `--json-args` |

**可复制例（已 cd 到技能目录）**

```bat
REM cmd
node scripts\tiktok\search-cli.js --keyword "AI tutorial" --sort 1 --limit 20
node scripts\tiktok\comment-cli.js --url "https://www.tiktok.com/@user/video/1234567890123456789" --limit 40
```

```powershell
# PowerShell
node scripts/tiktok/search-cli.js --keyword "AI tutorial" --sort 1 --limit 20
node scripts/tiktok/comment-cli.js --url "https://www.tiktok.com/@user/video/1234567890123456789" --limit 40
```

**`--json-args`（与其它 flag 互斥）**

键名用 schema 字段名（`keyword` / `url` / `sort` / `limit`…），不要写 `--keyword`。

```bat
REM cmd
node scripts\tiktok\search-cli.js --json-args "{\"keyword\":\"AI tutorial\",\"sort\":1,\"limit\":20}"
```

```powershell
# PowerShell：外层单引号包整段 JSON
node scripts/tiktok/search-cli.js --json-args '{"keyword":"AI tutorial","sort":1,"limit":20}'
```

**绝对路径（推荐；未 cd / cwd 不是技能根时必用）**

`<SKILL_ROOT>` = 含本技能 `SKILL.md` 的那一层真实目录（以当前会话安装位置为准）。勿套用其它宿主的示例路径，勿用 frontmatter `name` 冒充目录名。

```bat
REM cmd
node "<SKILL_ROOT>\scripts\tiktok\search-cli.js" --keyword "AI tutorial" --sort 1 --limit 20
```

```powershell
# PowerShell
node "<SKILL_ROOT>/scripts/tiktok/search-cli.js" --keyword "AI tutorial" --sort 1 --limit 20
```

> 成功结果默认不落盘；`--save`（或 `=true`/`1`）或 `GUAIKEI_ENABLE_LOG=1` 时写系统临时目录 `tiktok-guaikei/logs/`；`--save=false`/`0` 关闭 CLI 侧落盘（env 仍开时以 env 为准）；非法值报错。旧变量 `TT_GUAIKEI_ENABLE_LOG` 已废弃。

## FAQ

- **`Cannot find module`**：用上一节 `node "<SKILL_ROOT>/scripts/tiktok/…"`；或先 `cd` 到 `<SKILL_ROOT>` 再用相对路径。
- **调用失败**：退出码 3 = token；2 = 参数；1 = 业务/网络等。详见 `SKILL.md` 与 [options.md](options.md)。
- **包月超限**：`PLAN_LIMIT`；搜索/作品 ≤30、评论 ≤40；禁止同参重试。取数成功或 empty 时，信封顶层可能带 `cost`（花费**估算**：包月为 `1`，按次为条数×单价）；错误响应无此字段。

参数详表：[options.md](options.md)。
