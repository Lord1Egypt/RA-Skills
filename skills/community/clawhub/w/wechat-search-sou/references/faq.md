# 常见问题与环境配置

> **何时读**：排障、配 TOKEN、查落盘或 Windows 拼参时再读。日常执行不必每次打开。

## 环境

- Node.js 16.14.0+，Windows / Linux / macOS；必需环境变量 `GUAIKEI_API_TOKEN`（16–256 位字母、数字、下划线或连字符）。
- Windows cmd：`set GUAIKEI_API_TOKEN=你的TOKEN`
- Windows PowerShell：`$env:GUAIKEI_API_TOKEN="你的TOKEN"`
- Linux/macOS：`export GUAIKEI_API_TOKEN=你的TOKEN`
- 可选：`GUAIKEI_API_HOST` 覆盖 API 域名（默认 `www.guaikei.com`）。

## Windows 引号 / 拆参

Agent 在 Windows 上最常见的失败不是业务错，而是 **shell 把参数拆坏**，技能报 `INVALID_ARGS` / `INVALID_KEYWORD`。

**硬规则**

- **cmd.exe：只用双引号** `"` 包含空格、中文的参数；**不要用单引号** `'`。
- PowerShell：含空格/中文参数也优先双引号；勿照搬 bash 单引号去 cmd。
- **Windows / 弱模型优先 `--json-args`**：业务字段放进一个 JSON 对象；**不可**与传统 flag 混用。
- 关键词以 `-` 开头：写成 `--keyword=-AI`，或 `node scripts/wechat/article-cli.js -- -AI`，或 JSON 里 `"keyword":"-AI"`。

**症状 → 处理**

| 症状 | 先做什么 |
| --- | --- |
| `INVALID_ARGS` / 参数解析错误，且命令里有空格中文 | 整段改成双引号包参数后 **只重试一次**；仍失败 → `--json-args` |
| 关键词被拆成多段 | 同上；或直接 `--json-args` |
| 混用了 bash 示例里的单引号 | 全部换成双引号，或改用 `--json-args` |

**可复制例（已 cd 到技能目录）**

```bat
REM cmd
node scripts\wechat\article-cli.js --keyword "AI 教程" --sort 1 --limit 10
node scripts\wechat\video-cli.js --keyword "AI 教程" --sort 2 --limit 10
```

```powershell
# PowerShell
node scripts/wechat/article-cli.js --keyword "AI 教程" --sort 1 --limit 10
node scripts/wechat/video-cli.js --keyword "AI 教程" --sort 2 --limit 10
```

**`--json-args`（与其它 flag 互斥）**

键名用 schema 字段名（`keyword` / `sort` / `limit`…），不要写 `--keyword`。

```bat
REM cmd
node scripts\wechat\article-cli.js --json-args "{\"keyword\":\"AI 教程\",\"sort\":1,\"limit\":10}"
```

```powershell
# PowerShell：外层单引号包整段 JSON
node scripts/wechat/article-cli.js --json-args '{"keyword":"AI 教程","sort":1,"limit":10}'
```

**绝对路径（推荐；未 cd / cwd 不是技能根时必用）**

`<SKILL_ROOT>` = 含本技能 `SKILL.md` 的那一层真实目录（以当前会话安装位置为准）。勿套用其它宿主的示例路径，勿用 frontmatter `name` 冒充目录名。

```bat
REM cmd
node "<SKILL_ROOT>\scripts\wechat\article-cli.js" --keyword "AI 教程" --limit 10
```

```powershell
# PowerShell
node "<SKILL_ROOT>/scripts/wechat/article-cli.js" --keyword "AI 教程" --limit 10
```

> 默认不落盘。需要留底时加 `--save`（或 `--save=true`）或设 `GUAIKEI_ENABLE_LOG=1`；`--save=false` / `0` 显式关闭 CLI 落盘（env 仍开时以 env 为准）；非法值报错。写入系统临时目录 `wechat-guaikei/logs/当天日期/`（与 cwd 无关）。旧技能目录 `logs/` 不再写入，可自行删除。

## FAQ

- **`Cannot find module`**：用上一节 `node "<SKILL_ROOT>/scripts/wechat/…"`；或先 `cd` 到 `<SKILL_ROOT>` 再用相对路径。
- **调用失败**：退出码 3 = token；2 = 参数；1 = 业务/网络等。详见 `SKILL.md`。
- **包月超限**：`PLAN_LIMIT`；文章/视频搜索包月最多 20；禁止同参重试。取数成功或 empty 时，信封顶层可能带 `cost`（花费**估算**：包月为 `1`，按次为条数×单价）；错误响应无此字段。

参数详表：[options.md](options.md)。
