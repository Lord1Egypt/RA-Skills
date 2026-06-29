# zsxq-post-fetch

知识星球帖子抓取助手，用于在 ClawHub / Clawdbot / OpenClaw 技能目录中调用脚本读取用户已授权账号可访问的知识星球内容。

默认后端已经迁移到官方 [`zsxq-cli`](https://github.com/unnoo/zsxq-skill)：

- 认证走 `zsxq-cli auth login`，OAuth token 由官方 CLI 存入系统 Keychain。
- `fetch_topics.js` 默认调用 `zsxq-cli group +list --json`、`group +topics --json`、`topic +detail --json`。
- 旧的 `api.zsxq.com/v2` + `ZSXQ_TOKEN` 直连逻辑仅作为显式 legacy fallback 保留。

## 功能

- 抓取指定星球最新帖子，支持 `all` 和 `digests`
- 按关键词搜索指定星球主题，并下载匹配帖子的附件
- 通过帖子 ID 或完整链接查询单条帖子详情
- 按日期范围抓取帖子，遇到早于开始日期的帖子自动停止翻页
- 列出当前账号已加入的星球
- 使用 `groups.json` 管理多个星球
- 使用 `--markdown` 按日期导出 Markdown
- 可选下载图片和文件附件，并用相对路径写入 Markdown
- legacy HTTP fallback 保留指数退避、随机抖动和附件下载签名 URL 逻辑

## 文件结构

```text
zsxq-post-fetch/
├── SKILL.md
├── README.md
├── fetch_topics.js
├── install.sh
├── package.json
├── config.json
├── groups.json
├── docs/
├── references/
│   └── api-reference.md
└── test/
    └── fetch_topics.helpers.test.js
```

## 环境要求

- Node.js 18 或更高版本
- 官方 `zsxq-cli`
- 已通过官方 CLI 登录的知识星球账号

验证本地环境：

```bash
bash install.sh
npm test
```

`install.sh` 会检测 `zsxq-cli`，缺失时尝试执行 `npm install -g zsxq-cli`。脚本不会自动登录；如果 `zsxq-cli auth status` 未通过，请手动运行：

```bash
zsxq-cli auth login
```

## 安装

### 从 ClawHub 安装

```bash
clawhub install zsxq-post-fetch
```

### 手动安装

```bash
git clone https://github.com/chenmuwen0930-rgb/openclaw-skill-zsxq ~/.openclaw/skills/zsxq-post-fetch
bash ~/.openclaw/skills/zsxq-post-fetch/install.sh
```

## 配置

### 1. 后端选择

默认使用官方 CLI 后端：

```json
{
  "backend": "cli",
  "attachment_dir": "~/.openclaw/workspace/zsxq",
  "download_attachments": true
}
```

只有在你明确需要旧 HTTP 直连 fallback 时才使用：

```bash
export ZSXQ_BACKEND=http
export ZSXQ_TOKEN="your_zsxq_access_token"
```

也可以在 `config.json` 中设置：

```json
{
  "backend": "http"
}
```

环境变量 `ZSXQ_BACKEND` 优先级高于 `config.json.backend`。

### 2. 附件和 Markdown 根目录

默认读取 `config.json` 的 `attachment_dir`。也可以用环境变量覆盖：

```bash
export ZSXQ_ATTACHMENT_DIR="~/.openclaw/workspace/zsxq"
```

优先级为：`ZSXQ_ATTACHMENT_DIR` -> `ATTACHMENT_DIR` -> `config.json` 的 `attachment_dir`。

### 3. 星球配置

编辑 `groups.json`：

```json
[
  {
    "group_id": "YOUR_GROUP_ID",
    "name": "你的星球名称",
    "scope": "digests",
    "max_topics": 20
  }
]
```

不确定 `group_id` 时，先确保已登录官方 CLI，然后运行：

```bash
node fetch_topics.js groups
```

## 使用

在 Clawdbot / OpenClaw 中直接询问即可触发，例如：

```text
帮我看看知识星球最新有什么内容
```

也可以直接运行脚本。

### 抓取帖子

```bash
node fetch_topics.js topics <group_id> [count] [scope] [--markdown]
```

示例：

```bash
node fetch_topics.js topics YOUR_GROUP_ID 20 all --markdown
```

### 抓取精华帖

```bash
node fetch_topics.js digests <group_id> [count] [--markdown]
```

CLI 后端会读取官方 CLI 返回的帖子列表并按 `digested` / `is_digested` 字段过滤。如果官方 CLI 输出不包含精华标记，脚本会返回 `digests_unavailable_from_cli`，不会自动改用 legacy HTTP。

### 按关键词搜索并下载

```bash
node fetch_topics.js search <group_id> <keyword> [count] [--markdown] [--download-attachments]
```

示例：

```bash
node fetch_topics.js search YOUR_GROUP_ID "SpaceX IPO" 20 --markdown --download-attachments
```

默认通过官方 MCP tool `search_topics` 搜索主题，再用 `topic +detail` 补全帖子和附件信息。`count` 是对官方搜索单次返回结果的客户端截断；当前官方 CLI 未文档化 `search_topics` 的分页参数。

`--download-attachments` 会强制下载匹配帖子的附件；`--markdown` 会把匹配帖子按日期写入 Markdown。

### 查询单条帖子

```bash
node fetch_topics.js topic <group_id> <topic_id_or_url> [--markdown]
```

示例：

```bash
node fetch_topics.js topic YOUR_GROUP_ID 82811454228448260 --markdown
node fetch_topics.js topic YOUR_GROUP_ID https://wx.zsxq.com/topic/82811454228448260
```

参数仍保留 `group_id` 以兼容旧接口；CLI 后端实际使用 `zsxq-cli topic +detail --topic-id`。

### 按日期范围抓取

```bash
node fetch_topics.js topics-by-date <group_id> <start_date> [end_date] [count] [--markdown]
```

示例：

```bash
node fetch_topics.js topics-by-date YOUR_GROUP_ID 2026-06-01 2026-06-13 50 --markdown
```

### 列出已加入星球

```bash
node fetch_topics.js groups
```

## 输出

默认输出 JSON 到 stdout。加 `--markdown` 后，Markdown 会按帖子日期切分并保存到：

```text
<attachment_dir>/<group_id>/<YYYY-MM-DD>.md
```

图片和文件附件会保存到对应日期目录：

```text
<attachment_dir>/<group_id>/<YYYY-MM-DD>/
```

附件文件名会加 `topic_id` 前缀避免同一天重名，例如：

```text
82255281882211890_image_1.jpg
82255281882211890_report.pdf
```

Markdown 中会优先使用相对路径引用本地附件：

```markdown
![82255281882211890_image_1.jpg](2026-06-13/82255281882211890_image_1.jpg)
[82255281882211890_report.pdf](2026-06-13/82255281882211890_report.pdf)
```

## legacy HTTP fallback

只有显式设置 `ZSXQ_BACKEND=http` 或 `config.json.backend = "http"` 时，脚本才会使用旧的 `api.zsxq.com/v2` 直连逻辑。该路径要求：

```bash
export ZSXQ_TOKEN="your_zsxq_access_token"
```

`ZSXQ_TOKEN` 仅用于 legacy fallback。不要把真实 token 写入 Git、README、`groups.json`、`config.json` 或发布包。

## 1059 与风控

默认后端使用官方 `zsxq-cli` 的 OAuth/Keychain 认证路径，避免继续模拟非官方客户端访问私有 API。项目不实现伪造官方客户端、伪造 TLS/header 指纹或绕过风控的逻辑。

如果你显式启用 legacy HTTP fallback 并遇到 `code: 1059`，说明知识星球已识别并阻止非官方客户端访问。推荐回到默认 CLI 后端：

```bash
unset ZSXQ_BACKEND
zsxq-cli auth login
node fetch_topics.js groups
```

## 安全与隐私

- 默认认证完全交给官方 `zsxq-cli`，脚本不读取或输出 Keychain token
- `ZSXQ_TOKEN` 只用于 legacy HTTP fallback
- 不在仓库中存放真实 token、cookie、API key、secret 或个人账号凭证
- `groups` 子命令会暴露当前账号已加入的星球列表，只在用户明确需要时运行
- 批量抓取会把私有帖子内容交给当前 agent 处理，应确保符合组织的数据和合规要求

## 发布前检查

```bash
npm test
rg -n "(api[_-]?key|token|secret|password|cookie|authorization|bearer|zsxq_access_token)" .
clawhub skill publish . --slug zsxq-post-fetch --name "Zsxq Post Fetch" --version 1.2.0 --changelog "Add keyword search and attachment download workflow"
```

`rg` 命令会命中说明文档和测试里的占位词，这些需要人工确认不是硬编码凭证。

## License

MIT
