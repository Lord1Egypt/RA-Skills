---
name: weread-import
description: 将微信读书的划线与想法导出为 Markdown 文件，通常写入 Obsidian 阅读目录。适用于用户要求导入或同步微信读书笔记、导出单本或全部书籍、重新渲染已有笔记、验证删除归档行为、调整模板/合并逻辑/frontmatter tags，或需要通过官方 Gateway、浏览器登录态、手动 Cookie 运行微信读书导出时。
---

# weread-import

通过 `scripts/run.sh` 运行 CLI。首次执行时会自动安装依赖。

## 默认策略

1. 默认使用官方 Gateway 后端，需要环境变量 `WEREAD_API_KEY`。
2. `WEREAD_API_KEY` 获取路径：打开微信读书 App 最新版 -> 我的 -> 右上角设置按钮 -> 微信读书 Skill -> 快速配置第 2 步 -> 获取 API Key。
3. 未配置 `WEREAD_API_KEY` 时，提示用户配置并复述获取路径，同时展示 Gateway、受管浏览器、外部 Chrome、手动 Cookie 四种可选路径；不要自行切换到 Cookie。
4. Gateway 已配置但网络失败、HTTP 5xx、网关不可达或接口不支持时，自动回退 web 后端。
5. 用户显式传入 `--cookie-from` 或 `--cookie` 时，视为老用户旧链路，自动使用 web 后端；若显式 `--api-backend gateway`，则 Gateway 优先并忽略 cookie 参数。
6. 修改模板、合并逻辑或 frontmatter 后，先输出到临时目录验证。
7. 验证通过后，再对真实目录执行。
8. 目的是重新渲染或验证时，加上 `--force` 跳过增量检查。

详细命令模板见 `references/workflows.md`。

## 推荐命令

```bash
# 导入单本书
bash ./scripts/run.sh --book "自卑与超越" --output "/path/to/Reading"

# 导入全部书
bash ./scripts/run.sh --all --output "/path/to/Reading"

# 强制重新渲染
bash ./scripts/run.sh --book "自卑与超越" --output "/path/to/Reading" --force

# 覆盖 frontmatter tags
bash ./scripts/run.sh --book "自卑与超越" --output "/path/to/Reading" --tags "reading/weread,book"

# 明确不使用官方 Gateway，改用旧浏览器/Cookie 链路
bash ./scripts/run.sh --all --no-gateway --cookie-from browser-managed --output "/path/to/Reading"
```

## Agent 决策表

| 场景 | 行为 |
|------|------|
| 新用户 / 常规导入 | 使用默认 Gateway 命令：`bash ./scripts/run.sh --all --output "/path/to/Reading"` |
| 缺少 `WEREAD_API_KEY` | 报告 CLI 给出的可选项，并复述获取路径：微信读书 App 最新版 -> 我的 -> 右上角设置按钮 -> 微信读书 Skill -> 快速配置第 2 步 -> 获取 API Key；不要替用户选择 |
| 老用户命令含 `--cookie-from` 或 `--cookie` | 直接执行，CLI 会按旧 web 后端运行，并提示 Gateway 升级优势 |
| 用户明确不用 Gateway | 使用 `--no-gateway --cookie-from browser-managed`，或按用户指定的 cookie/browser 参数执行 |
| Gateway 临时不可用 | 允许 CLI 自动回退 web 后端，报告最终 backend |
| Gateway 鉴权失败或 `upgrade_info` | 不回退，报告原始错误和升级/配置要求 |
| 定时任务 | 新任务推荐 Gateway 固定命令；已有旧 cron 命令继续执行，不要自动改参数或加 `--force` |

## 可用参数

- `--all`
- `--book <title>`
- `--book-id <id>`
- `--output <dir>`
- `--mode <api>`
- `--api-backend <gateway|web>`
- `--no-gateway`
- `--cookie <cookie>`
- `--cookie-from <manual|browser-live|browser-managed>`
- `--force`
- `--tags <a,b,c>`

## 定时任务

定时 / 自动执行场景下，必须严格遵守以下规则。

### 固定命令

```bash
bash ./scripts/run.sh --all --output "/path/to/Reading"
```

原样执行，禁止修改参数。不要添加 `--force`、不要替换 Gateway 为硬编码 cookie、不要省略 `--output`。

### 前置条件

- 默认 Gateway 需要 `WEREAD_API_KEY`。
- 显式 `--cookie-from` / `--cookie` 的老命令会按 web 后端执行，不要求 `WEREAD_API_KEY`。
- `--no-gateway` / web 后端下，`browser-live` 需要外部 Chrome CDP 已运行且已登录微信读书。
- `--no-gateway` / web 后端下，`browser-managed` 会自动拉起隔离浏览器；首次需要用户在该独立窗口里登录微信读书。
- 如果 CDP 未运行或登录已过期，命令会以非零 exit code 退出 — 这是预期行为，不要尝试修复。

### 禁止事项

- 禁止加 `--force` — 增量跳过是定时场景的正确行为，不是 bug。
- 禁止用 `--cookie '...'` 硬编码 cookie — cookie 会过期，应优先使用 Gateway 或浏览器模式。
- 禁止在失败后自行重试、变更参数、或尝试其他方式绕过错误。

### 错误处理

- exit code 0 = 成功，直接报告结果。
- exit code 非 0 = 失败，将完整错误输出报告给用户，不做任何额外操作。
- 鉴权失败时，不要立刻断言用户已退出登录。先按 `references/workflows.md` 的验证流程区分登录态、CDP 环境和浏览器上下文问题。

## 运行须知

- 默认后端为官方 Gateway，调用 `https://i.weread.qq.com/api/agent/gateway`。
- `run.sh` 在 `browser-managed` 下会自动拉起隔离 Chrome；`browser-live` 下只校验外部 CDP，不会自动拉起浏览器。
- Chrome 146+ 要求非默认 `--user-data-dir` 才能开启远程调试，`open-chrome-debug.sh` 会自动处理。
- `browser-managed` 默认使用 `~/.weread-import-profile-isolated`，不会同步默认 Chrome 的整份登录态。
- `browser` 仍然可用，但仅作为 `browser-managed` 的兼容别名。
- 如需保留旧的整份 profile 同步行为，显式设置 `WEREAD_PROFILE_SYNC_MODE=legacy`。
- 浏览器 cookie / 浏览器上下文请求在 CDP 会话结束后会正确关闭 Playwright 连接，不会关闭用户自己的 Chrome。
- API 请求自动附加时间戳防缓存，减少因 CDN 缓存导致的鉴权失败。
- API 鉴权失败会自动刷新当前 session 重试；浏览器模式下的书籍详情接口会复用浏览器上下文。
- 官方口径中 `noteCount` 是划线数，`reviewCount` 是想法/点评数，`bookmarkCount` 是书签数；书签只统计，不导出正文。
- 合并统计支持新增 / 更新 / 保留 / 删除四种分类。
- 被删除的条目会归档到 `## 已删除`，而非直接丢弃。
- 元信息由 YAML frontmatter 承载，正文中不重复。
- Skill 在脚本层面自包含，但运行环境需提供 Node.js 和 Playwright。

## 环境变量

参见 `env.example.md`。

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `WEREAD_API_KEY` | 官方 Gateway API Key | - |
| `WEREAD_API_BACKEND` | API 后端：`gateway` 或 `web` | `gateway` |
| `WEREAD_GATEWAY_SKILL_VERSION` | 官方 Gateway skill 版本 | `1.0.3` |
| `WEREAD_COOKIE` | 手动 Cookie | - |
| `WEREAD_IMPORT_MODE` | 导出模式 | `api` |
| `WEREAD_CDP_URL` | Chrome CDP 地址 | `http://127.0.0.1:9222` |
| `WEREAD_OUTPUT` | 输出目录 | `./out/weread` |
| `WEREAD_TAGS` | Frontmatter tags | `reading,weread` |
| `WEREAD_USER_AGENT` | 自定义 UA | Chrome 146 |

## 资源

- GitHub: https://github.com/gnixner/weread-import

### scripts/
- `scripts/run.sh`：Skill 执行入口（首次自动安装依赖；`browser-managed` 自动拉起隔离 Chrome，`browser-live` 只校验外部 CDP）
- `scripts/open-chrome-debug.sh`：启动隔离的 Chrome 远程调试；`legacy` 模式下才同步默认 Profile 登录态
- `scripts/prepare-staging-skill.sh`：生成隔离的 staging skill 目录，供发版前安装态验证使用

### references/
- `references/workflows.md`：推荐工作流、验证流程与常见问题处理
