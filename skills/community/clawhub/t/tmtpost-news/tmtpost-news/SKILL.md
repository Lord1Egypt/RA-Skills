---
name: tmtpost-news
description: 获取7×24 财经科技新闻资讯和深度报道，聚焦财经、科技、商业、创投等领域的资讯报道和深度分析。支持热门文章、最新文章、最新快讯查询。当用户需要搜索财经、科技、商业、创投等领域热点资讯和深度报道时使用。
description_zh: 钛媒体文章和快讯，支持热门文章、最新文章、最新快讯查询。
description_en: TMTPost news and articles with hot articles, latest articles, latest brief news
version: 1.0.0
author: TMTPost
tags: [news, tmtpost, tech, business, startup, venture capital]
---

# 钛媒体文章订阅

通过 `tmtpost-news-cli` 获取钛媒体文章内容。

> **核心原则**：基础设施（安装、更新、Key 配置）交给脚本处理；智能体只负责选择子命令和参数——始终先读 `help`，不要硬编码。

## 平台约定

| 平台 | 脚本运行方式 | 示例 |
|------|------------|------|
| macOS / Linux | `sh scripts/<name>.sh` | `sh scripts/cli-state.sh` |
| Windows | `bun scripts/<name>.ts` | `bun scripts/cli-state.ts` |

> Windows 需先确保 `bun` 可用。若不可用：`powershell -c "irm bun.sh/install.ps1 | iex"`，安装后重启终端确认 `bun --version`。

以下所有脚本调用均以 macOS / Linux 为例，Windows 将 `.sh` 替换为 `.ts`，`sh` 替换为 `bun`。

CLI 命令本身不要依赖 `cli-state` 返回的模板字符串，直接根据 `platform.cliPath` 组装：

| 平台 | CLI 命令模板 |
|------|-------------|
| macOS / Linux | `"<cliPath>" <subcommand> [args]` |
| Windows PowerShell | `& "<cliPath>" <subcommand> [args]` |

## Phase 1：环境就绪

> 环境已就绪时直接跳到 Phase 2。

### 1. 状态检查

```sh
sh scripts/cli-state.sh
```

解析返回的 JSON，关注以下字段：

| 字段 | 含义 |
|------|------|
| `platform.cliPath` | CLI 完整路径，后续所有命令使用此路径 |
| `platform.cliSource` | `global`（用户已全局安装）/ `local`（技能目录下载）/ `none`（未找到） |
| `cliExists` | CLI 是否存在 |
| `update.needUpdate` | 当前版本是否需要更新 |
| `update.error` | `version` 检查失败时的错误信息 |
| `apiKey.present` | API Key 是否已配置 |
| `apiKey.status` | `configured` / `missing` / `error` |
| `apiKey.error` | `apikey-get` 执行异常或输出异常时的错误信息 |

### 2. 安装 CLI（`cliExists` 为 `false` 时）

> `cliSource` 为 `global` 时跳过此步。

```sh
sh scripts/install-cli.sh
```

安装/更新完成后，重新执行 cli-state.sh，用最新的 apiKey.status 决定是否进入 Step 4。

### 3. 更新 CLI（`update.needUpdate` 为 `true`，或 CLI 提示版本过旧时）

```sh
"<cliPath>" update
```

Windows PowerShell 使用 `& "<cliPath>" update`。

始终使用 `platform.cliPath` 组装命令。若 `update.error` 不为空，先展示错误并让用户处理。

若 `update` 命令失败，或错误信息表明当前 CLI 不支持 `update`（如 `unknown command`、`not found`、`not recognized`），立即改为执行安装脚本覆盖：

```sh
sh scripts/install-cli.sh --force
```

Windows：

```sh
bun scripts/install-cli.ts --force
```

解析安装脚本返回的 JSON，并把后续命令切换到新返回的 `platform.cliPath`。只有覆盖安装也失败时，才引导用户参考 [`references/update-guide.md`](references/update-guide.md) 手动处理。
安装/更新完成后，重新执行 cli-state.sh，用最新的 apiKey.status 决定是否进入 Step 4。

### 4. 配置 API Key（`apiKey.status` 不为 `configured` 时）

- `missing` → 引导用户前往钛媒体平台自行获取 API Key，**不要执行 `open` / `xdg-open` / `start` 等命令自动打开浏览器**
- `error` → 展示 `apiKey.error`，让用户先处理（权限、网络、CLI 异常），处理后重试

设置 Key（命令前缀使用 `platform.cliPath`，KEY 是裸值不加引号）：

```sh
"<cliPath>" apikey-set KEY
```

Windows PowerShell 分别使用 `& "<cliPath>" apikey-set KEY`、`& "<cliPath>" apikey-get`、`& "<cliPath>" apikey-clear`。

验证：`"<cliPath>" apikey-get`
清除（仅用户明确要求时）：`"<cliPath>" apikey-clear`

详见 [`references/env-setup-guide.md`](references/env-setup-guide.md)。

## Phase 2：获取文章

> CLI 更新频繁，子命令和参数可能随版本变化。**始终以当前 `help` 输出为准，不要假设或记忆任何子命令。**

1. **执行 `help`**
   使用 `platform.cliPath` 自行拼命令：macOS / Linux 为 `"<cliPath>" help`，Windows PowerShell 为 `& "<cliPath>" help`。

2. **理解意图，映射子命令**
   - **单一请求**（如"看热门文章"）→ 映射到一个子命令
   - **复合请求**（如"看热门文章和科技新闻"）→ 拆解为多个意图，分别映射，依次调用
   - 若 `help` 中无匹配子命令，如实告知用户当前不支持

3. **执行并输出**——按下方格式呈现结果

## 输出格式

### 单类型请求

```markdown
1. **标题文字**

   来源：作者名称

   摘要内容……

   [查看原文](https://…)

2. **标题文字**

   来源：作者名称

   摘要内容……

   [查看原文](https://…)

**来源：钛媒体**
```

### 多类型请求

按类型分组，每组用二级标题标明类别：

```markdown
## 热门文章

1. **标题文字**
   ...

2. **标题文字**
   ...

## 科技资讯

1. **标题文字**
   ...

2. **标题文字**
   ...

**来源：钛媒体**
```

### 通用规则

- **标题**：`序号. **标题**`，序号从 1 开始，多类型时每组序号独立
- **来源**：`来源：` 后跟 CLI 返回的作者名称；无该字段时省略
- **摘要**：来源下方紧跟；无摘要字段时省略
- **原文链接**：有链接则输出 `[查看原文](URL)`，无则不输出
- 其他有价值字段（发布时间、标签等）可在来源下方补充
- 多条新闻间用空行分隔
- `**来源：钛媒体**` 在所有内容末尾出现一次
- 某个类型获取失败时，在该分组下说明原因，继续输出其余分组
- 当输出的内容不完全符合用户的需求时，你需要帮用户过滤掉无用的新闻。

## CLI 执行失败处理

**CLI 命令失败后，立即停止，绝不通过 WebSearch 或其他方式获取新闻替代。**

1. CLI 返回非零退出码、超时或输出含权限/安全错误时，不要重试，不要换方式。
2. 根据错误信息引导用户：
   - **macOS Gatekeeper**（`cannot be opened`、`not verified`）→ 系统设置 → 隐私与安全性 → 「仍要打开」
   - **企业安全软件**（`connection refused`、防火墙拦截）→ 安全提示中点击「信任」/「允许」
   - **权限不足**（`permission denied`）→ `chmod +x <cliPath>`
   - **其他** → 展示完整错误，请用户处理
3. 用户确认操作完成后再重试。即使多次失败，也只能告知无法获取并说明原因，**绝不**回退到其他信息源。

## References

- API Key 获取与手动配置：[`references/env-setup-guide.md`](references/env-setup-guide.md)
- 用户手动更新指南：[`references/update-guide.md`](references/update-guide.md)
