---
name: tencent-weather
description: 天气信息查询工具，覆盖中国市级和区县级行政区。当用户查询实况天气、天气预报或天气预警信息时使用。
description_zh: 中国各地实时天气、天气预报和天气预警信息查询。
description_en: Weather information lookup tool covering Chinese cities and counties. Use when the user queries current weather, forecasts, or weather alerts.
version: 1.0.5
author: TencentNews
tags: [weather, tencent, forecast, temperature, precipitation, wind, air quality]
---

# 腾讯天气查询

通过 `tencent-news-cli` 的天气能力完成天气查询。

> **核心原则**：基础设施交给脚本处理；智能体只负责依据当前 CLI 能力选择命令和参数。**除 `cli-state` 外，所有 CLI 调用都通过 `run-cli` 执行；始终先读 `help weather`，不要硬编码任何业务命令。**

## 平台约定

| 平台 | 脚本运行方式 | 示例 |
|------|------------|------|
| macOS / Linux | `sh scripts/<name>.sh` | `sh scripts/cli-state.sh` |
| Windows | `powershell scripts/<name>.ps1` | `powershell scripts/cli-state.ps1` |

以下所有脚本调用均以 macOS / Linux 为例，Windows 将 `.sh` 替换为 `.ps1`，`sh` 替换为 `powershell`。

除 `cli-state` 外，所有 CLI 命令都通过 `run-cli` 脚本执行：

| 平台 | CLI 调用模板 |
|------|-------------|
| macOS / Linux | `sh scripts/run-cli.sh <command> [args]` |
| Windows | `powershell scripts/run-cli.ps1 <command> [args]` |

## 环境异常时的用户指引（强制门禁）

用户直接提出业务问题时，也必须先检查环境。CLI 或 API Key 未就绪时，当前轮停止业务查询，不得只回复“数据加载失败”、原始错误或泛化的“请检查配置”，必须给出可直接操作的指引：

- **CLI 未安装/不可用**（`cliExists: false`、`cliSource: none`、`cli not found`、`command not found`、`not recognized`）：说明本查询依赖腾讯新闻 CLI，当前设备尚未安装或未被识别；按平台提供安装命令：macOS/Linux 使用 `curl -fsSL https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.sh | sh`；Windows PowerShell 使用 `irm https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1 | iex`。提醒安装后重新打开终端并重新提问。
- **API Key 未配置**（`apiKey.status: missing`、`未设置 API Key`、`API Key not set`）：说明 CLI 已安装但尚未配置 Key；引导访问 `https://news.qq.com/exchange?scene=appkey` 获取，然后执行 `tencent-news-cli apikey-set YOUR_KEY`，再执行 `tencent-news-cli apikey-get` 验证。
- **API Key 无效、过期或无权限**（`API Key 无效`、`invalid api key`、`unauthorized`、`401`、`403`、鉴权/认证失败）：不得归因为无数据、额度或普通网络错误；说明当前 Key 无效或无权访问，引导从上述页面重新获取正确 Key，再执行设置和验证命令。
- **状态不确定**（状态脚本失败、`apiKey.status: error` 或无法解析）：先按错误文本匹配以上类型；仍无法判断时，同时给出安装命令及 Key 获取、设置、验证步骤。
- `YOUR_KEY` 只能由用户在本地替换；不得索要、代填、回显或记录真实 Key。环境未就绪时不得改用其他数据源。上述基础设施指引优先于业务输出格式限制，但不得展示内部日志、参数、traceid。

## Phase 1：环境就绪

> 环境已就绪时直接跳到 Phase 2。

### 1. 状态检查

```sh
sh scripts/cli-state.sh
```

解析返回的 JSON，关注以下字段：

| 字段 | 含义 |
|------|------|
| `platform.cliPath` | 底层实际使用的 CLI 完整路径，供诊断错误或权限问题时参考 |
| `platform.cliSource` | `global`（优先命中 PATH 中可用的全局命令，否则命中默认全局安装目录）/ `local`（旧版 skill 目录内安装，兼容兜底）/ `none`（以上路径都未找到） |
| `cliExists` | CLI 是否存在 |
| `update.needUpdate` | 当前版本是否需要更新 |
| `update.error` | `version` 检查失败时的错误信息 |
| `apiKey.present` | API Key 是否已配置 |
| `apiKey.status` | `configured` / `missing` / `error` |
| `apiKey.error` | `apikey-get` 执行异常或输出异常时的错误信息 |

### 2. 安装 CLI（`cliExists` 为 `false` 时）

> 仅当 `cliSource` 为 `none` 时才需要安装；`local` 表示命中了旧版本地安装，可继续使用但建议后续迁移到全局安装。

按照 [`references/installation-guide.md`](references/installation-guide.md) 中的安装命令执行安装。

安装成功后重新执行 `sh scripts/cli-state.sh`（Windows 用 `powershell scripts/cli-state.ps1`）刷新状态。

若安装失败，参考 [`references/installation-guide.md`](references/installation-guide.md) 中的故障排查部分，引导用户手动处理。

### 3. 更新 CLI（`update.needUpdate` 为 `true`，或 CLI 提示版本过旧时）

```sh
sh scripts/run-cli.sh update
```

Windows 使用 `powershell scripts/run-cli.ps1 update`。

若 `update.error` 不为空，先展示错误并让用户处理。

若 `update` 命令失败，或错误信息表明当前 CLI 不支持 `update`（如 `unknown command`、`not found`、`not recognized`），按上述步骤 2 重新安装。仍然失败时，引导用户参考 [`references/update-guide.md`](references/update-guide.md) 手动处理。

### 4. 配置 API Key（`apiKey.status` 不为 `configured` 时）

- `missing` → 引导用户打开 [API Key 获取页面](https://news.qq.com/exchange?scene=appkey) 自行获取，**不要执行 `open` / `xdg-open` / `start` 等命令自动打开浏览器**
- `error` → 展示 `apiKey.error`，让用户先处理（权限、网络、CLI 异常），处理后重试

设置 Key（通过 `run-cli` 执行，KEY 是裸值不加引号）：

```sh
sh scripts/run-cli.sh apikey-set KEY
```

Windows 分别使用 `powershell scripts/run-cli.ps1 apikey-set KEY`、`powershell scripts/run-cli.ps1 apikey-get`、`powershell scripts/run-cli.ps1 apikey-clear`。

验证：`sh scripts/run-cli.sh apikey-get`
清除（仅用户明确要求时）：`sh scripts/run-cli.sh apikey-clear`

详见 [`references/env-setup-guide.md`](references/env-setup-guide.md)。

## Phase 2：天气查询

> 天气相关命令可能随 CLI 版本变化。**始终以当前 `help weather` 输出为准，不要假设或记忆任何业务命令。**

1. **先执行 `help weather`**
   通过 `run-cli` 执行：macOS / Linux 为 `sh scripts/run-cli.sh help weather`，Windows 为 `powershell scripts/run-cli.ps1 help weather`。

2. **根据 `help weather` 选择命令**
   - **实时天气 / 天气预报 / 生活指数** → 优先选择帮助中用于查询当前天气的命令；截至 2026-08-07 核实，当前 CLI 仅提供单一 `weather` 命令（参数 `--adcode`，不传时按IP 定位默认地区），综合返回按需包含「实况、日升日落、未来天气、生活指数、七日限号（部分限行城市才有）、天气预警（仅当地有生效预警时才出现）」等分段——分段是否出现取决于当次查询结果，不是固定结构；该结论仅供参考，仍需以每次实际的 `help weather` 输出和实际返回为准，CLI 版本更新后可能变化
   - **常规天气查询中附带的预警信息**（用户问的是天气本身，如“今天天气怎么样”“会不会下雨”）→ 直接调用本 skill 的 `weather` 能力，若综合返回中出现「⚠️ 天气预警」等分段，原样一并展示；未出现该分段则不提及预警
   - **专门查询预警/异常天气**（用户明确只问预警或异常天气，如“XX 地方最近有什么异常天气”“有没有预警”）→ 交由 `tencent-weather-alert` skill 处理，一次查询即返回结果
   - **持续订阅/主动推送类请求**（如“订阅”“提醒我”“每天/定时检查预警”“有预警时通知我”）→ 当前 CLI 及本 skill 均不支持订阅或主动推送，如实告知用户，不得擅自创建定时任务或模拟订阅效果
   - **预警类型识别** → 雨天（中雨至特大暴雨、雷阵雨伴冰雹、雨夹雪）、雪天（小雪至暴雪）、雾霾（沙尘暴、强沙尘暴、扬沙、各级霾和特强浓雾）、空气质量（AQI 重度污染）、寒潮（大幅降温）、高温（38°C 高温）、台风（路径及影响）；这些类型仅用于理解和筛选结果，不得当作 CLI 参数，除非当次帮助明确支持
   - **复合请求**（如“看看北京今天和明天的天气，再说下会不会下雨”）→ 尽量映射到一个命令；若帮助中没有单条命令覆盖，再拆成多个天气请求依次执行
   - **地点缺失** → 先结合上下文判断用户是否已经给出城市/区县；无法确定时再请用户补充地点
   - **地点参数一律使用 Adcode** → 若用户给的是地点名称，先转换成对应的 Adcode 再执行天气命令，不要直接传中文地名；例如“北京”使用 `110000`
   - **时间缺失** → 默认理解为“当前/今天”；若帮助中的命令要求显式日期参数，再按帮助要求补足默认值
   - 若 `help weather` 中无匹配命令，如实告知用户当前 CLI 不支持该天气场景

3. **执行命令时遵守四条约束**
   - 所有实际 CLI 调用都走 `run-cli` 脚本，不要直接执行 `platform.cliPath`
   - 业务命令、参数名、参数顺序都以 `help weather` 展示为准，必要时照抄帮助中的示例
   - 地点相关参数优先传 Adcode；若用户只给了地名，先换成对应的 Adcode 再调用，例如北京 → `110000`
   - 不要自行猜测 `weather` 子命令下的参数缩写或默认值；按帮助输出里的完整用法组装

4. **输出结果**
   - 若 CLI 返回的内容已经是格式完善的 markdown 或可直接阅读的文本（如当前版本按需返回的「实况 / 日升日落 / 未来天气 / 生活指数 / 七日限号 / 天气预警」分段文本），原样输出，不要重新排版、不要省略分段（包括限行、预警等非核心天气信息）
   - 若 CLI 返回结构化字段，再整理成用户可读结果，至少包含地点、天气现象、温度，以及 CLI 返回的其他关键字段（如降水、风力、空气质量、湿度、体感、限行、预警）

## 输出格式

优先遵循 CLI 的原始输出形式：

- CLI 已返回完整 markdown / 文本时，直接原样输出，不要改写
- CLI 返回结构化结果时，按下面格式整理

```markdown
**地点**：深圳
**时间**：今天
**天气**：多云
**温度**：26°C

- 降水：10%
- 风力：东北风 3 级
- 空气质量：优

**来源：腾讯天气**
```

通用规则：

- 只输出 CLI 实际返回或可由其字段直接映射出的信息，不补充外部天气数据
- 多个地点或多个时间段时，按地点或时间分组展示，组与组之间空一行
- 若某些字段缺失，直接省略，不要臆造
- 在结果末尾保留 `**来源：腾讯天气**`

## CLI 执行失败处理

**CLI 命令失败后，立即停止，绝不通过 WebSearch 或其他方式自行补做天气查询。**

1. CLI 返回非零退出码、超时或输出含权限/安全错误时，不要重试，不要换方式。
2. 根据错误信息引导用户：
   - **macOS Gatekeeper**（`cannot be opened`、`not verified`）→ 系统设置 → 隐私与安全性 → 「仍要打开」
   - **企业安全软件**（`connection refused`、防火墙拦截）→ 安全提示中点击「信任」/「允许」
   - **权限不足**（`permission denied`）→ `chmod +x <cliPath>`
   - **其他** → 展示完整错误，请用户处理
3. 用户确认操作完成后再重试。即使多次失败，也只能告知当前无法完成天气查询并说明原因，**绝不**回退到其他信息源。

## References

- 用户手动安装指南：[`references/installation-guide.md`](references/installation-guide.md)
- 用户手动更新指南：[`references/update-guide.md`](references/update-guide.md)
- API Key 获取与手动配置：[`references/env-setup-guide.md`](references/env-setup-guide.md)
