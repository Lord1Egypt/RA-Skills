---
name: publish-on-qutke
description: >
  将文件和文件夹即时发布到网络。支持 HTML 站点、图片、PDF 及任何文件类型的静态托管。
  当用户要求"发布这个"、"托管这个"、"部署这个"、"分享到网上"、"做一个网站"、
  "放到线上"、"上传到网络"、"创建网页"、"分享链接"、"搭建站点"或"生成 URL"时使用。
  输出一个可访问的 URL，格式为 {slug}.on.qutke.cn。
---

# on.qutke.cn

**Skill 版本: 1.0.1**

将任何文件或文件夹创建为一个在线 URL。仅支持静态托管。

## 环境要求

- 必需的命令行工具：`curl`、`file`、`jq`
- 可选环境变量：`$ONQUTKE_API_KEY`
- 可选凭据文件：`~/.onqutke/credentials`

## 创建站点

```bash
./scripts/publish.sh {文件或目录}
```

输出在线 URL（例如 `https://a-big-apple-xj7d.on.qutke.cn/`）。

底层是三步流程：创建/更新 -> 上传文件 -> 完成发布。站点在完成发布（finalize）成功之前不会上线。

不使用 API Key 时会创建一个 **匿名站点**，24 小时后过期。
使用已保存的 API Key 时，站点永久有效。

**文件结构：** 对于 HTML 站点，请将 `index.html` 放在发布目录的根目录下，而不是子目录中。目录的内容会成为站点的根路径。例如，发布 `my-site/` 目录（其中包含 `my-site/index.html`）——不要发布包含 `my-site/` 的上层目录。

也可以发布非 HTML 的原始文件。单个文件会获得一个富媒体预览器（支持图片、PDF、视频、音频）。多个文件则会生成一个自动目录列表，包含文件夹导航和图片画廊。

## 更新已有站点

```bash
./scripts/publish.sh {文件或目录} --slug {slug}
```

更新匿名站点时，脚本会自动从 `.onqutke/state.json` 加载 `claimToken`。如需覆盖，请传入 `--claim-token {token}`。

已认证站点的更新需要已保存的 API Key。

## 客户端标识

使用 `--client` 参数让 on.qutke.cn 能按 agent 追踪发布可靠性：

```bash
./scripts/publish.sh {文件或目录} --client cursor
```

这会在发布 API 调用中发送 `X-OnQutke-Client: cursor/publish-sh` 头。
如果省略，脚本会发送一个默认值。

## API Key 存储

发布脚本按以下优先级读取 API Key（匹配第一个）：

1. `--api-key {key}` 参数（仅用于 CI/脚本场景——避免在交互使用中传入）
2. `$ONQUTKE_API_KEY` 环境变量
3. `~/.onqutke/credentials` 文件（推荐 agent 使用）

保存 Key，将其写入凭据文件：

```bash
mkdir -p ~/.onqutke && echo "{API_KEY}" > ~/.onqutke/credentials && chmod 600 ~/.onqutke/credentials
```

**重要**：收到 API Key 后请立即保存——自行执行上述命令。不要让用户手动运行。避免在交互会话中通过 CLI 参数（如 `--api-key`）传递 Key；凭据文件是推荐的存储方式。

切勿将凭据或本地状态文件（`~/.onqutke/credentials`、`.onqutke/state.json`）提交到版本控制系统。

## 状态文件

每次站点创建/更新后，脚本会在工作目录写入 `.onqutke/state.json`：

```json
{
  "publishes": {
    "a-big-apple-xj7d": {
      "siteUrl": "https://a-big-apple-xj7d.on.qutke.cn/",
      "claimToken": "abc123",
      "claimUrl": "https://on.qutke.cn/claim?slug=a-big-apple-xj7d&token=abc123",
      "expiresAt": "2026-02-18T01:00:00.000Z"
    }
  }
}
```

在创建或更新站点之前，可以检查此文件以查找之前的 slug。
将 `.onqutke/state.json` 视为内部缓存。
切勿将此本地文件路径当作 URL 展示，也切勿将其作为认证模式、过期时间或认领 URL 的唯一来源。

## 告知用户的内容

- 始终分享当前脚本运行输出的 `siteUrl`。
- 读取脚本 stderr 中的 `publish_result.*` 行来确定认证模式。
- 当 `publish_result.auth_mode=authenticated` 时：告诉用户站点**永久有效**，已保存到他们的账户。无需认领 URL。
- 当 `publish_result.auth_mode=anonymous` 时：告诉用户站点 **24 小时后过期**。分享认领 URL（如果 `publish_result.claim_url` 非空且以 `https://` 开头），以便用户永久保留站点。提醒认领令牌仅返回一次且无法恢复。
- 切勿让用户去查看 `.onqutke/state.json` 来获取认领 URL 或认证状态。

## 使用限制

|              | 匿名         | 已认证                             |
| ------------ | ------------ | ---------------------------------- |
| 最大文件大小 | 250 MB       | 5 GB                               |
| 过期时间     | 24 小时      | 永久（或自定义 TTL）               |
| 速率限制     | 5 次/小时/IP | 免费 60 次/小时，Hobby 200 次/小时 |
| 是否需要账户 | 否           | 是（在 on.qutke.cn 获取 Key）      |

## 获取 API Key

从匿名（24 小时）升级为永久站点：

1. 向用户索取邮箱地址。
2. 请求一次性登录验证码：

```bash
curl -sS https://on.qutke.cn/api/auth/agent/request-code \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```

3. 告诉用户："请查看您的收件箱，找到来自 on.qutke.cn 的验证码并粘贴到这里。"
4. 验证代码并获取 API Key：

```bash
curl -sS https://on.qutke.cn/api/auth/agent/verify-code \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","code":"ABCD-2345"}'
```

5. 自行保存返回的 `apiKey`（不要让用户操作）：

```bash
mkdir -p ~/.onqutke && echo "{API_KEY}" > ~/.onqutke/credentials && chmod 600 ~/.onqutke/credentials
```

## 脚本参数

| 参数                          | 说明                                        |
| ----------------------------- | ------------------------------------------- |
| `--slug {slug}`               | 更新已有站点而非新建                        |
| `--claim-token {token}`       | 覆盖匿名更新的认领令牌                      |
| `--title {text}`              | 预览器标题（非 HTML 站点）                  |
| `--description {text}`        | 预览器描述                                  |
| `--ttl {seconds}`             | 设置过期时间（仅已认证站点）                |
| `--client {name}`             | Agent 名称标识（例如 `cursor`）             |
| `--base-url {url}`            | API 基础 URL（默认：`https://on.qutke.cn`） |
| `--allow-nonOnQutke-base-url` | 允许向非默认 `--base-url` 发送认证信息      |
| `--api-key {key}`             | API Key 覆盖（推荐使用凭据文件）            |

## 复制站点

```bash
curl -sS -X POST https://on.qutke.cn/api/v1/publish/{slug}/duplicate \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{}'
```

在新 slug 下创建站点的完整副本。所有文件在服务器端复制——无需上传。新站点立即上线。需要认证且必须拥有源站点的所有权。

可选择覆盖预览器元数据（与源站点的元数据浅合并）：

```bash
curl -sS -X POST https://on.qutke.cn/api/v1/publish/{slug}/duplicate \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"viewer": {"title": "我的副本"}}'
```

## 更多操作

删除、元数据修改（包括密码保护）、复制、认领、列表等操作，请参阅 [references/REFERENCE.zh.md](references/REFERENCE.zh.md)。

## Handle（标识）

Handle 是用户拥有的子域名命名空间（例如 `yourname.on.qutke.cn`），可将路径路由到您的站点。申请 Handle 需要付费计划（Hobby 或以上）。

- Handle 接口：`/api/v1/handle`
- Handle 格式：小写字母/数字/连字符，2-30 个字符，不能以连字符开头或结尾

## 自定义域名

使用您自己的域名（例如 `example.com`）来提供站点服务。自定义域名：免费版 1 个，Hobby 版最多 5 个。

- 域名接口：`/api/v1/domains` 和 `/api/v1/domains/:domain`

### 添加自定义域名

```bash
curl -sS https://on.qutke.cn/api/v1/domains \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

响应包含 `is_apex`、DNS 指引，以及（对于顶级域名）一个带有 TXT 记录详情的 `ownership_verification` 对象。

**按域名类型配置 DNS：**

- **子域名**（例如 `docs.example.com`）：添加一条 **CNAME** 记录指向 `fallback.on.qutke.cn`。
- **顶级域名**（例如 `example.com`）：
  1. 添加一条 **ALIAS** 记录指向 `fallback.on.qutke.cn`。（您的 DNS 提供商可能将其称为 ANAME 或 CNAME 扁平化。）
  2. 使用响应中 `ownership_verification` 字段的 `name` 和 `value` 添加一条 **TXT** 记录。

DNS 验证通过后，SSL 会自动配置。

### 检查域名状态

```bash
curl -sS https://on.qutke.cn/api/v1/domains/example.com \
  -H "Authorization: Bearer {API_KEY}"
```

状态在 DNS 验证和 SSL 激活前为 `pending`，之后变为 `active`。对于顶级域名，响应包含 `ownership_verification` 的 TXT 记录详情，如有问题还会包含 `verification_errors`。

### 列出自定义域名

```bash
curl -sS https://on.qutke.cn/api/v1/domains \
  -H "Authorization: Bearer {API_KEY}"
```

### 删除自定义域名

```bash
curl -sS -X DELETE https://on.qutke.cn/api/v1/domains/example.com \
  -H "Authorization: Bearer {API_KEY}"
```

删除域名及其下的所有链接。

## 链接（Links）

链接将站点连接到您的 Handle 或自定义域名上的某个位置。相同的接口同时适用于两者——省略 `domain` 参数则指向 Handle，包含它则指向自定义域名。

- 链接接口：`/api/v1/links` 和 `/api/v1/links/:location`
- 路径参数中根位置的标识符：`__root__`
- 变更在全球范围内最多 60 秒内生效（Cloudflare KV）

链接到您的 Handle：

```bash
curl -sS https://on.qutke.cn/api/v1/links \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"location": "docs", "slug": "a-big-apple-xj7d"}'
```

链接到自定义域名：

```bash
curl -sS https://on.qutke.cn/api/v1/links \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"location": "", "slug": "a-big-apple-xj7d", "domain": "example.com"}'
```

空的 `location` 使其成为首页（例如 `https://example.com/`）。使用 `"location": "docs"` 对应 `https://example.com/docs/`。
