# on.qutke.cn API 参考文档

基础 URL：`https://on.qutke.cn`

## 认证方式

两种模式：

- **已认证**：请求头中包含 `Authorization: Bearer <API_KEY>`。
- **匿名**：省略该请求头。站点 24 小时后过期，且有更低的使用限制。

### 可选的客户端标识头

可以在站点 API 调用中包含一个可选请求头：

- `X-OnQutke-Client: <agent>/<tool>`

示例：

- `X-OnQutke-Client: cursor/publish-sh`
- `X-OnQutke-Client: claude-code/publish-sh`
- `X-OnQutke-Client: codex/cli`
- `X-OnQutke-Client: openclaw/direct-api`

这帮助 on.qutke.cn 按客户端调试发布可靠性。缺失或无效的值会被忽略；发布请求不会因为缺少此头而被拒绝。

### 获取 API Key

有两种方式获取 API Key：

#### 方式 A：Agent 辅助注册

注册流程可以完全在 agent 内完成，无需用户打开浏览器。

**1. 通过邮箱请求一次性验证码：**

```bash
curl -sS https://on.qutke.cn/api/auth/agent/request-code \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```

响应：

```json
{
  "success": true,
  "requiresCodeEntry": true,
  "expiresAt": "2026-03-01T12:34:56.000Z"
}
```

**2. 用户从邮箱复制验证码**并粘贴给 agent。

**3. 验证代码并获取 API Key：**

```bash
curl -sS https://on.qutke.cn/api/auth/agent/verify-code \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","code":"ABCD-2345"}'
```

响应：

```json
{
  "success": true,
  "email": "user@example.com",
  "apiKey": "<API_KEY>",
  "isNewUser": true
}
```

验证码无效或已过期时返回 `400`。

**4. 将 API Key 保存到凭据文件：**

```bash
mkdir -p ~/.onqutke && echo "<API_KEY>" > ~/.onqutke/credentials && chmod 600 ~/.onqutke/credentials
```

#### 方式 B：控制台注册

用户也可以在 [on.qutke.cn](https://on.qutke.cn) 登录，从控制台复制 API Key。然后使用上述步骤 4 的命令保存到凭据文件。

### 存储 API Key

发布脚本按以下优先级读取 API Key（匹配第一个）：

1. `--api-key {key}` 参数（仅用于 CI/脚本场景——避免在交互中使用）
2. `$ONQUTKE_API_KEY` 环境变量
3. `~/.onqutke/credentials` 文件（推荐）

凭据文件是推荐的存储方式。避免在交互会话中通过 CLI 参数传递 Key。

## 接口列表

### 创建新站点

`POST /api/v1/publish`（别名：`POST /api/v1/artifact`）

创建一个随机 slug 的新站点。支持认证和匿名模式。

**请求体：**

```json
{
  "files": [
    {
      "path": "index.html",
      "size": 1234,
      "contentType": "text/html; charset=utf-8",
      "hash": "a1b2c3d4..."
    },
    {
      "path": "assets/app.js",
      "size": 999,
      "contentType": "text/javascript; charset=utf-8",
      "hash": "e5f6a7b8..."
    }
  ],
  "ttlSeconds": null,
  "viewer": {
    "title": "我的站点",
    "description": "由 agent 发布",
    "ogImagePath": "assets/cover.png"
  }
}
```

- `files`（必需）：`{ path, size, contentType, hash }` 数组。至少一个文件。路径应相对于站点根目录（例如 `index.html`、`assets/style.css`）——不要包含上层目录名如 `my-project/index.html`。
- `hash`（可选）：文件内容的 SHA-256 十六进制摘要（64 个小写字符）。更新已有站点时，hash 与上一版本匹配的文件会出现在 `upload.skipped[]` 而非 `upload.uploads[]` 中——无需上传。服务器在完成发布时自动复制。省略 `hash` 则使用默认行为（所有文件都需上传）。
- `ttlSeconds`（可选）：过期秒数。匿名站点忽略此项（始终为 24 小时）。
- `viewer`（可选）：自动预览器页面的元数据（仅在没有 `index.html` 时使用）。

**响应（已认证）：**

```json
{
  "slug": "a-big-apple-xj7d",
  "siteUrl": "https://a-big-apple-xj7d.on.qutke.cn/",
  "status": "pending",
  "isLive": false,
  "requiresFinalize": true,
  "note": "站点已创建，但此 slug 尚未上线。上传所有文件到 upload.uploads[]，然后 POST upload.finalizeUrl 并附带 {\"versionId\":\"...\"}。",
  "upload": {
    "versionId": "01J...",
    "uploads": [
      {
        "path": "index.html",
        "method": "PUT",
        "url": "https://<presigned-r2-url>",
        "headers": { "Content-Type": "text/html; charset=utf-8" }
      }
    ],
    "skipped": ["assets/app.js"],
    "finalizeUrl": "https://on.qutke.cn/api/v1/publish/a-big-apple-xj7d/finalize",
    "expiresInSeconds": 3600
  }
}
```

**此步骤仅创建了一个待处理的站点，尚未完成。**

- 您**必须上传** `upload.uploads[]` 中的每个文件。
- `upload.skipped[]` 中的文件与上一版本相同，将在完成发布时由服务器端复制。无需上传。
- 然后**必须完成发布**：向 `upload.finalizeUrl` 发送 `POST` 请求，请求体为 `{ "versionId": "..." }`。
- 对于全新的 slug，在完成发布之前 `siteUrl` 可能返回 404。
- 对于已有站点的更新，上一版本在完成发布切换到新版本之前保持在线。

**响应（匿名），额外字段：**

```json
{
  "claimToken": "abc123...",
  "claimUrl": "https://on.qutke.cn/claim?slug=a-big-apple-xj7d&token=abc123...",
  "expiresAt": "2026-02-19T01:00:00.000Z",
  "anonymous": true,
  "warning": "重要：保存 claimToken 和 claimUrl。它们仅返回一次且无法恢复。将 claimUrl 分享给用户以便他们永久保留站点。"
}
```

**重要：`claimToken` 和 `claimUrl` 仅返回一次且无法恢复。请始终保存 `claimToken` 并将 `claimUrl` 分享给用户，以便他们认领站点并永久保留。如果丢失认领令牌，站点将在 24 小时后过期且无法挽回。**

`claimToken`、`claimUrl` 和 `expiresAt` 仅在匿名站点中出现。已认证站点不包含这些字段。

---

### 上传文件

对于 `upload.uploads[]` 中的每个条目，将文件 PUT 到预签名 URL：

```bash
curl -X PUT "<presigned-url>" \
  -H "Content-Type: <content-type>" \
  --data-binary @<本地文件>
```

上传可以并行进行。预签名 URL 有效期为 1 小时。

---

### 完成发布

`POST /api/v1/publish/:slug/finalize`（别名：`POST /api/v1/artifact/:slug/finalize`）

将 slug 指针切换到新版本，使站点上线。

**请求体：**

```json
{ "versionId": "01J..." }
```

**认证：**

- 已拥有的站点：需要 `Authorization: Bearer <API_KEY>`。
- 匿名站点：完成发布无需认证。

**响应：**

```json
{
  "success": true,
  "slug": "a-big-apple-xj7d",
  "siteUrl": "https://a-big-apple-xj7d.on.qutke.cn/",
  "previousVersionId": null,
  "currentVersionId": "01J..."
}
```

---

### 更新已有站点

`PUT /api/v1/publish/:slug`（别名：`PUT /api/v1/artifact/:slug`）

请求体与创建相同。返回新的预签名上传 URL 和新的 `finalizeUrl`。
更新响应同样包含 `status: "pending"` 和 `isLive: false`，表示新版本在完成发布前不会上线。

**增量部署：** 在每个文件上包含 `hash`（SHA-256 十六进制）。hash 与上一版本匹配的文件会出现在 `upload.skipped[]` 而非 `upload.uploads[]` 中——无需上传。服务器在完成发布时复制。这是迭代开发的推荐方式。

**已拥有站点的认证：** 需要与所有者匹配的 `Authorization: Bearer <API_KEY>`。

**匿名站点的认证：** 在请求体中包含 `claimToken`：

```json
{
  "files": [...],
  "claimToken": "<claimToken>"
}
```

匿名更新不会延长原始过期时间。过期后返回 `410 Gone`。

---

### 认领匿名站点

`POST /api/v1/publish/:slug/claim`（别名：`POST /api/v1/artifact/:slug/claim`）

将所有权转移给已认证用户并移除过期时间。

**需要：** `Authorization: Bearer <API_KEY>`

**请求体：**

```json
{ "claimToken": "abc123..." }
```

**响应：**

```json
{
  "success": true,
  "slug": "a-big-apple-xj7d",
  "siteUrl": "https://a-big-apple-xj7d.on.qutke.cn/",
  "expiresAt": null
}
```

用户也可以通过在浏览器中访问 `claimUrl` 并登录来认领。

---

### 密码保护

为任意站点添加密码，访客在查看前必须验证。这是服务器端强制的——在密码验证之前不会向浏览器发送任何内容。站点下的所有文件都受保护，不仅仅是首页。

通过 `PATCH /api/v1/publish/:slug/metadata` 设置或更改密码：`{"password": "secret"}`。通过 `{"password": null}` 移除密码。也可以从控制台通过每个站点的 `⋯` 菜单管理密码。

密码保护在重新部署后仍然有效——它是元数据，不是内容。更改或移除密码会立即使所有现有会话失效。需要已认证站点（匿名站点不支持密码保护）。

---

### 复制站点

`POST /api/v1/publish/:slug/duplicate`

在新 slug 下创建站点的完整服务器端副本。所有文件在服务器端复制——无需客户端上传或完成发布步骤。新站点立即上线。

复制所有文件和预览器元数据。不复制密码保护、Handle/域名链接或 TTL。

**需要：** `Authorization: Bearer <API_KEY>`（必须拥有源站点）

**请求体：**（可选）

```json
{
  "viewer": {
    "title": "我的副本",
    "description": "a-big-apple-xj7d 的副本"
  }
}
```

- `viewer`（可选）：与源站点的预览器元数据浅合并。仅提供的字段被覆盖；未提供的字段保留源站点的值。如果完全省略 `viewer`，则按原样复制源站点的元数据。

**响应：**

```json
{
  "slug": "warm-lake-f3k9",
  "siteUrl": "https://warm-lake-f3k9.on.qutke.cn/",
  "sourceSlug": "a-big-apple-xj7d",
  "status": "active",
  "currentVersionId": "01J...",
  "filesCount": 36
}
```

| 状态码 | 条件                                             |
| ------ | ------------------------------------------------ |
| 401    | 缺少或无效的 API Key                             |
| 403    | API Key 与源站点所有者不匹配                      |
| 404    | 源 slug 不存在或已删除                            |
| 409    | 源站点处于 `pending` 状态（尚未完成发布）          |
| 429    | 超出速率限制                                      |

---

### 修改元数据

`PATCH /api/v1/publish/:slug/metadata`（别名：`PATCH /api/v1/artifact/:slug/metadata`）

更新标题、描述、og:image、TTL 或密码，无需重新上传文件。

**需要：** `Authorization: Bearer <API_KEY>`

**请求体：**

```json
{
  "ttlSeconds": 604800,
  "viewer": {
    "title": "更新后的标题",
    "description": "新描述",
    "ogImagePath": "assets/cover.png"
  },
  "password": "secret123"
}
```

所有字段均为可选。`ogImagePath` 必须引用当前站点内的图片文件。

- `password`：字符串设置或更改密码，`null` 移除密码，省略则不变。设置后，访客必须输入密码才能查看任何内容。服务器端强制——未验证不发送内容。更改或移除密码立即使所有现有会话失效。

**响应：**

```json
{
  "success": true,
  "effectiveForRootDocument": true,
  "note": "预览器元数据生效，因为此站点没有 index.html。",
  "passwordProtected": true
}
```

如果站点有 `index.html`，预览器元数据会被存储但站点自身的 HTML 控制浏览器展示。当提供了 `password` 字段时会包含 `passwordProtected`。

---

### 删除站点

`DELETE /api/v1/publish/:slug`（别名：`DELETE /api/v1/artifact/:slug`）

硬删除站点、所有版本和 slug 索引记录。

**需要：** `Authorization: Bearer <API_KEY>`

**响应：**

```json
{ "success": true }
```

---

### 列出站点

`GET /api/v1/publishes`（别名：`GET /api/v1/artifacts`）

返回已认证用户拥有的所有站点。

**需要：** `Authorization: Bearer <API_KEY>`

**响应：**

```json
{
  "publishes": [
    {
      "slug": "a-big-apple-xj7d",
      "siteUrl": "https://a-big-apple-xj7d.on.qutke.cn/",
      "updatedAt": "2026-02-18T...",
      "expiresAt": null,
      "status": "active",
      "currentVersionId": "01J...",
      "pendingVersionId": null
    }
  ]
}
```

---

### 获取站点详情

`GET /api/v1/publish/:slug`（别名：`GET /api/v1/artifact/:slug`）

返回您拥有的站点的元数据和完整文件清单。

**需要：** `Authorization: Bearer <API_KEY>`（仅所有者）

**响应：**

```json
{
  "slug": "a-big-apple-xj7d",
  "siteUrl": "https://a-big-apple-xj7d.on.qutke.cn/",
  "status": "active",
  "createdAt": "2026-02-18T...",
  "updatedAt": "2026-02-18T...",
  "expiresAt": null,
  "currentVersionId": "01J...",
  "pendingVersionId": null,
  "manifest": [
    {
      "path": "index.html",
      "size": 1234,
      "contentType": "text/html; charset=utf-8",
      "hash": "a1b2c3d4..."
    },
    {
      "path": "assets/app.js",
      "size": 999,
      "contentType": "text/javascript; charset=utf-8",
      "hash": "e5f6a7b8..."
    }
  ]
}
```

`manifest` 数组列出当前在线版本的所有文件及其路径、大小、内容类型和 hash（如有）。文件内容可从在线 `siteUrl` 获取（例如 `https://a-big-apple-xj7d.on.qutke.cn/index.html`）。

---

### 刷新上传 URL

`POST /api/v1/publish/:slug/uploads/refresh`（别名：`POST /api/v1/artifact/:slug/uploads/refresh`）

为待处理的上传返回新的预签名 URL（相同版本，不创建新版本）。

**需要：** `Authorization: Bearer <API_KEY>`

当预签名 URL 在上传过程中过期时使用（有效期为 1 小时）。

---

### 注册 Handle

`POST /api/v1/handle`

为 `handle.on.qutke.cn` 注册您的 Handle。需要付费计划（Hobby 或以上）。免费计划返回 403 并附带 `upgrade_url`。

**需要：** `Authorization: Bearer <API_KEY>`

**请求体：**

```json
{ "handle": "yourname" }
```

**响应：**

```json
{
  "handle": "yourname",
  "hostname": "yourname.on.qutke.cn",
  "namespace_id": "uuid"
}
```

Handle 规则：2-30 个字符，小写字母/数字/连字符，不能以连字符开头或结尾，保留名称被禁止。

---

### 获取当前 Handle

`GET /api/v1/handle`

返回您当前的 Handle 和链接。

**需要：** `Authorization: Bearer <API_KEY>`

---

### 更改 Handle

`PATCH /api/v1/handle`

将现有 Handle 更改为新的。需要付费计划（Hobby 或以上）。免费计划返回 403 并附带 `upgrade_url`。

**需要：** `Authorization: Bearer <API_KEY>`

**请求体：**

```json
{ "handle": "newname" }
```

---

### 删除 Handle

`DELETE /api/v1/handle`

删除您的 Handle 及其下的所有链接。

**需要：** `Authorization: Bearer <API_KEY>`

---

### 添加自定义域名

`POST /api/v1/domains`

为您的账户注册自定义域名。免费计划：1 个域名。Hobby 计划：最多 5 个域名。

**需要：** `Authorization: Bearer <API_KEY>`

**请求体：**

```json
{ "domain": "example.com" }
```

**响应（顶级域名示例）：**

```json
{
  "domain": "example.com",
  "namespace_id": "uuid",
  "status": "pending",
  "is_apex": true,
  "dns_instructions": {
    "type": "ALIAS",
    "name": "example.com",
    "target": "fallback.on.qutke.cn",
    "note": "添加一条 ALIAS 记录（有时称为 ANAME 或 CNAME 扁平化）指向 fallback.on.qutke.cn。"
  },
  "ownership_verification": {
    "type": "txt",
    "name": "_cf-custom-hostname.example.com",
    "value": "uuid-token"
  }
}
```

**按域名类型配置 DNS：**

- **子域名**（例如 `docs.example.com`）：添加一条 **CNAME** 记录指向 `fallback.on.qutke.cn`。
- **顶级域名**（例如 `example.com`）：
  1. 添加一条 **ALIAS** 记录指向 `fallback.on.qutke.cn`。（您的 DNS 提供商可能将其称为 ANAME 或 CNAME 扁平化。）
  2. 使用 `ownership_verification` 中的 `name` 和 `value` 添加一条 **TXT** 记录。

DNS 验证通过后，SSL 会自动配置。

---

### 列出自定义域名

`GET /api/v1/domains`

返回已认证用户的所有自定义域名，包括状态和链接。

**需要：** `Authorization: Bearer <API_KEY>`

**响应：**

```json
{
  "domains": [
    {
      "domain": "example.com",
      "namespace_id": "uuid",
      "status": "active",
      "ssl_status": "active",
      "is_apex": true,
      "created_at": "2026-03-09T...",
      "verified_at": "2026-03-09T...",
      "mounts": [{ "mount_path": "", "slug": "a-big-apple-xj7d" }]
    }
  ]
}
```

对于待处理的域名，此接口也会轮询 Cloudflare 的 SSL 验证状态并自动更新。顶级域名包含 `ownership_verification` 的 TXT 记录详情。

---

### 获取自定义域名状态

`GET /api/v1/domains/:domain`

返回特定自定义域名的详情。对待处理的域名触发按需验证。包含 `is_apex`、`ownership_verification`（顶级域名）和 `verification_errors`（如适用）。

**需要：** `Authorization: Bearer <API_KEY>`

---

### 删除自定义域名

`DELETE /api/v1/domains/:domain`

删除自定义域名及其下的所有链接。

**需要：** `Authorization: Bearer <API_KEY>`

**响应：**

```json
{ "deleted": true }
```

---

### 在 Handle 或自定义域名下创建链接

`POST /api/v1/links`

将站点 slug 链接到 Handle 或自定义域名下的某个位置。

**需要：** `Authorization: Bearer <API_KEY>`

**请求体：**

```json
{
  "location": "docs",
  "slug": "a-big-apple-xj7d"
}
```

使用空的 `location` 链接到根路径（`https://yourname.on.qutke.cn/`）。

要链接到自定义域名而非 Handle，添加 `domain` 参数：

```json
{
  "location": "",
  "slug": "a-big-apple-xj7d",
  "domain": "example.com"
}
```

这使 `https://example.com/` 提供该站点的服务。域名必须处于 active（已验证）状态。

---

### 列出 Handle 下的链接

`GET /api/v1/links`

列出当前 Handle 下的所有链接。

**需要：** `Authorization: Bearer <API_KEY>`

---

### 获取单个链接

`GET /api/v1/links/:location`

按位置获取单个链接。根位置使用 `__root__`。

**需要：** `Authorization: Bearer <API_KEY>`

---

### 更新单个链接

`PATCH /api/v1/links/:location`

更改某个位置指向的站点 slug。

**需要：** `Authorization: Bearer <API_KEY>`

**请求体：**

```json
{ "slug": "another-slug-x9f1" }
```

---

### 删除单个链接

`DELETE /api/v1/links/:location`

按位置删除链接。根位置使用 `__root__`。

**需要：** `Authorization: Bearer <API_KEY>`

要从自定义域名（而非 Handle）删除链接，添加 `?domain=example.com` 作为查询参数。

---

### 发起付费订阅

`POST /api/v1/billing/checkout`

为 Hobby 计划创建 Stripe 结账会话。

**需要：** `Authorization: Bearer <API_KEY>`（或浏览器会话认证）。

**响应：**

```json
{ "url": "https://checkout.stripe.com/..." }
```

---

### 打开账单管理

`POST /api/v1/billing/portal`

创建 Stripe 账单管理门户会话。

**需要：** `Authorization: Bearer <API_KEY>`（或浏览器会话认证）。

**响应：**

```json
{ "url": "https://billing.stripe.com/..." }
```

---

Handle 和链接的变更写入 Cloudflare KV，可能需要最多 60 秒在全球范围内生效。

---

## URL 结构

每个站点拥有自己的子域名：`https://<slug>.on.qutke.cn/`

资源路径从子域名根自然解析：

- `/styles.css`、`/images/a.jpg` 按预期解析
- 相对路径（`styles.css`、`./images/a.jpg`）同样有效

### 服务规则

1. 如果根目录存在 `index.html` → 作为文档提供。
2. 否则如果整个站点只有一个文件 → 提供自动预览页面（图片、PDF、视频、音频有富媒体预览器；其他文件提供下载页面）。
3. 否则如果任何子目录中存在 `index.html` → 提供找到的第一个。
4. 其他情况 → 提供自动生成的目录列表。文件夹可点击，图片以画廊形式渲染，其他文件带大小列出。无需 `index.html`。

直接文件路径始终有效：`https://<slug>.on.qutke.cn/report.pdf`

## 使用限制

|                | 匿名          | 已认证                           |
| -------------- | ------------- | -------------------------------- |
| 最大文件大小    | 250 MB        | 5 GB                             |
| 过期时间       | 24 小时       | 永久（或自定义 TTL）              |
| 速率限制       | 5 次/小时/IP  | 免费 60 次/小时，Hobby 200 次/小时 |
| 是否需要账户    | 否            | 是（在 on.qutke.cn 获取 Key）     |
