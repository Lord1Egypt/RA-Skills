---
name: tencent-agent-storage
version: 1.0.8
author: shawnmzhang
license: MIT
description: |
  Cloud file storage, upload, backup, and file management tool for Tencent Agent Storage (专属网盘).
  Manages the user's personal cloud drive: upload files, list files, download, share links, preview, and backup.
  MUST trigger when the user mentions ANY of the following concepts:
  【云盘/网盘相关 — Cloud Drive Access】
  - "网盘", "云盘", "云空间", "龙虾盘", "龙虾云盘", "龙虾网盘", "龙虾空间"
  - "专属云盘", "专属网盘", "专属空间", "我的云盘", "我的网盘", "我的龙虾"
  - "打开网盘", "打开云盘", "进入网盘", "进入云盘", "看看云盘", "看看网盘"
  - "cloud drive", "my drive", "open drive", "lobster drive"
  【文件列表/查看 — File Listing & Browsing】
  - "列出文件", "有哪些文件", "看看文件", "文件列表", "我的文件"
  - "云盘里有什么", "空间里有啥", "查看云空间", "云空间文件"
  - "list files", "show files", "my files", "what files", "browse files"
  【上传/备份 — Upload & Backup】
  - "上传文件", "上传某个文件", "确定上传", "传到云空间", "上传到云空间"
  - "备份到云", "备份文件", "保存到云", "存到网盘", "传到网盘", "存到云盘", "传到云盘"
  - "文件传一下", "帮我传个文件", "把这个存一下"
  - "upload", "backup", "save to cloud", "back up"
  【发送/传输给用户 — Send & Deliver Files】
  - "把文件发给我", "整理好发我", "发到手机", "传到手机"
  - "做完了发我一份", "弄好了发给我", "完成后把文件给我"
  - "导出之后发我", "生成完发给我看看", "跑完了把结果给我"
  - "send file", "send to phone", "deliver file", "give me the file"
  【链接/分享 — Links & Sharing】
  - "生成下载链接", "做成链接", "给我下载链接"
  - "生成个链接发给同事", "发到群里", "分享文件", "分享给别人", "发个链接"
  - "download link", "share file", "share link", "generate link"
  【文件状态查询 — File Status Check】
  - "这个云文件还在吗", "之前上传的文件还能下吗", "链接过期了能重新生成吗"
  - "is file still there", "can I still download", "regenerate link"
  【文件搜索/检索 — File Search】
  - "搜索文件", "搜一下", "找文件", "找一下", "查找", "检索文件"
  - "搜索云盘", "在云盘里搜", "帮我找个文件", "有没有叫xxx的文件"
  - "search files", "find file", "search cloud"
  【隐式触发 — Implicit Triggers】
  - When a task produces output files (reports, exports, generated content) that need to be delivered to the user
  - When the user's intent implies needing a file on another device, even without explicitly saying "upload"
  - When MyClaw/agent needs to upload files to generate download links
  - Any mention of file transfer, cloud storage, or personal file space in the conversation context
metadata: {}
---

# Tencent Agent Storage (云文件上传备份工具)

将本地文件上传至 Tencent Agent Storage，自动生成下载链接和图片预览。上传的文件存储在用户独有的云盘空间中，支持跨端访问——无论是手机、电脑还是平板，用户都可以随时随地查看和下载自己的文件。

## When to Use

Agent **MUST** activate this skill when any of the following conditions are met:

- User mentions cloud drive keywords: 网盘、云盘、云空间、龙虾盘、专属网盘、cloud drive, my drive
- User requests file listing or browsing: 列出文件、有哪些文件、list files, show files
- User requests upload or backup: 上传文件、备份到云、存到网盘、upload, backup, save to cloud
- User asks to send/deliver files: 把文件发给我、发到手机、send file, deliver file
- User requests links or sharing: 生成下载链接、分享文件、download link, share link
- User queries file status: 这个云文件还在吗、链接过期了、is file still there
- User requests file search: 搜索文件、找文件、检索文件、搜索云盘、search files, find file
- **Implicit**: A task produces output files that need to be delivered to the user, or the user's intent implies needing a file on another device

## Quick Reference

| Command | Usage | Description |
|---------|-------|-------------|
| `upload` | `node scripts/agent-storage.js upload '<json>'` | Upload local file to cloud, returns download link |
| `uploadDir` | `node scripts/agent-storage.js uploadDir '<json>'` | Upload entire folder to cloud, preserving directory structure |
| `info` | `node scripts/agent-storage.js info '<json>'` | Get file info and regenerate download link |
| `list` | `node scripts/agent-storage.js list '<json>'` | List files in a cloud directory |
| `search` | `node scripts/agent-storage.js search '<json>'` | Search files by name |
| `mkdir` | `node scripts/agent-storage.js mkdir '<json>'` | Create a directory in cloud storage |

## Setup

### Prerequisites

此 skill 需要 **Node.js ≥ 14** 和 **npm**。Agent 在首次执行前**必须检测运行环境**：

```bash
node --version   # 期望输出 v14.x 或更高
npm --version
```

如果 `node` 命令不存在或版本低于 14，直接安装：

根据用户系统自动选择安装方式：

```bash
# macOS (Homebrew)
brew install node

# macOS (无 Homebrew)
curl -o node.pkg "https://nodejs.org/dist/v20.18.0/node-v20.18.0.pkg" && sudo installer -pkg node.pkg -target / && rm node.pkg

# Linux (Debian/Ubuntu)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs

# Linux (其他发行版 / 通用)
curl -fsSL https://nodejs.org/dist/v20.18.0/node-v20.18.0-linux-x64.tar.xz | sudo tar -xJ -C /usr/local --strip-components=1

# Windows (PowerShell, 管理员)
winget install OpenJS.NodeJS.LTS

# Windows (无 winget)
# 下载安装包: https://nodejs.org/dist/v20.18.0/node-v20.18.0-x64.msi 并运行

# 跨平台 (已有 nvm)
nvm install --lts
```

此 skill 还依赖 `smh-node-sdk` npm 包（**要求 ^1.0.8**）。**必须在使用前完成安装**（二选一）：

```bash
# 方式一：全局安装（推荐）
npm install -g smh-node-sdk@^1.0.8

# 方式二：本地安装到项目目录
npm install smh-node-sdk@^1.0.8
```

> 脚本会按以下顺序查找 SDK：当前项目 node_modules → 全局 node_modules。如果未找到，脚本会报错并提示安装命令。

### About the upload script

此 skill 的运行脚本位于 `scripts/agent-storage.js`。Agent 直接通过 `node scripts/agent-storage.js <command> '<json>'` 调用，**无需额外写入临时文件**。脚本源码可在 `scripts/` 目录中审阅。

### Credential configuration

凭证从以下配置文件中自动加载（优先级从高到低）。

> **安全说明**：脚本仅读取配置文件中 `smh_` 前缀的环境变量（`smh_libraryId`、`smh_accessToken` 等），不会访问配置文件中的其他字段或敏感信息。

> **关于 token 权限**：Tencent Agent Storage 的文件上传和下载链接生成 API 要求 `space_admin` 级别的 accessToken，这是 Tencent Agent Storage 服务端对文件写入操作的最低权限要求。

**模式一：直接凭证（accessToken）**

凭证文件查找顺序（先找到者优先）：

1. **通用配置** — `~/.tencentAgentStorage/.env`
2. **OpenClaw** — `~/.openclaw/openclaw.json` 的 `env` 字段
3. **Hermes** — `~/.hermes/.env`

**通用配置（推荐）** — 在 `~/.tencentAgentStorage/.env` 中配置：

```env
# ~/.tencentAgentStorage/.env
smh_basePath=https://api.tencentsmh.cn
smh_libraryId=smhxxx-xxxxx
smh_spaceId=space-xxxxx
smh_accessToken=<your-access-token>
```

**OpenClaw** — 在 `~/.openclaw/openclaw.json` 的 `env` 字段中配置：

```json
{
  "env": {
    "smh_basePath": "https://api.tencentsmh.cn",
    "smh_libraryId": "smhxxx-xxxxx",
    "smh_spaceId": "space-xxxxx",
    "smh_accessToken": "<your-access-token>"
  }
}
```

**Hermes** — 在 `~/.hermes/.env` 中配置：

```env
smh_basePath=https://api.tencentsmh.cn
smh_libraryId=smhxxx-xxxxx
smh_spaceId=space-xxxxx
smh_accessToken=<your-access-token>
```


---

## Procedure

Agent uses this skill in any scenario that requires uploading files to the cloud.

### Complete flow

```
User triggers file upload
  → Step 1: Identify the local file path(s)
  → Step 2: Run upload script (loop for batch)
  → Step 3: Extract downloadUrl from JSON output (signed COS URL)
  → Step 4: Deliver the download link with execution notice
```

> **IMPORTANT**: 默认使用 `conflictStrategy: "rename"` 上传。当云端已存在同名文件时，脚本会自动重命名（如 `file(1).pdf`），确保上传始终成功并返回正确的下载链接。**只有用户明确说了 "覆盖"/"替换" 时，才使用 `conflictStrategy: "overwrite"`；用户明确要求先确认时，才使用 `conflictStrategy: "ask"`。**

### Step 2: Upload

**Single file (默认):**

```bash
node scripts/agent-storage.js upload '{"localPath":"/path/to/file.pdf","conflictStrategy":"rename"}'
```

**Upload to specific directory:**

```bash
node scripts/agent-storage.js upload '{"localPath":"/path/to/photo.jpg","remotePath":"photos/photo.jpg","conflictStrategy":"rename"}'
```

**User explicitly requested overwrite:**

```bash
node scripts/agent-storage.js upload '{"localPath":"/path/to/report.pdf","conflictStrategy":"overwrite"}'
```

**Batch upload:**

```bash
node scripts/agent-storage.js upload '{"localPath":"/path/to/file1.pdf","conflictStrategy":"rename"}'
node scripts/agent-storage.js upload '{"localPath":"/path/to/file2.docx","conflictStrategy":"rename"}'
```

#### Conflict handling

When using `conflictStrategy: "rename"` (默认), if a same-name file already exists, the script automatically renames the file (e.g. `file(1).pdf`) and completes the upload, ensuring a valid download link is always returned.

When using `conflictStrategy: "ask"`, if a same-name file already exists, the script returns `{"success":false,"conflict":true}`. Agent must then ask the user:

> 云端已存在同名文件 `{filename}`，你想怎么处理？
>
> 1. 🔄 覆盖 — 替换云端文件
> 2. 📝 重命名 — 自动改名上传（如 file(1).pdf）
> 3. ❌ 取消 — 不上传

**三种策略对照：**

| Strategy | Behavior | When to use |
|----------|----------|-------------|
| `rename` (**默认**) | 同名文件存在时自动重命名，确保上传成功并返回正确链接 | 大多数场景，需要保证用户拿到下载链接 |
| `overwrite` | 直接覆盖已有文件 | 用户明确说 "覆盖", "替换", "更新文件" |
| `ask` | 同名文件存在时返回错误，Agent 询问用户 | 用户明确要求先确认时 |

### Step 4: Deliver link + execution notice

After every successful upload, include this notice alongside the download link(s):

> 链接已生成，链接有效期 2 小时，可直接在浏览器或手机中打开。

**链接输出规则（MUST）：**
1. **必须使用带 COS 签名的直链**（`downloadUrl` 字段），域名为 `*.tencentsmhuc.cn`，参数含 `q-sign-algorithm` 和 `q-signature`
2. **禁止输出含 `accessToken` 的中转链接**（如 `https://api.tencentsmh.cn/...?access_token=...`），这会泄露凭证
3. **链接必须完整输出，禁止任何形式的截断、省略或缩写**——不能用 `...`、`<省略>` 等替代任何部分。签名链接通常很长，这是正常的

**Single file example:**

> 链接已生成，链接有效期 2 小时，可直接在浏览器或手机中打开。
>
> 已上传文件: report.pdf  大小: (2.3 MB)
> 下载链接: {脚本返回的完整 downloadUrl，原样输出，不得截断}

**Batch example:**

> 链接已生成，链接有效期 2 小时，可直接在浏览器或手机中打开。
>
> 📎 report.pdf (2.3 MB) — {完整 downloadUrl}
> 📎 photo.jpg (1.1 MB) — {完整 downloadUrl}

---

## File Size Support

**There is NO file size limit.** The upload script supports files of any size, including multi-GB videos.

- **Small files (≤ 50 MB)**: Single-part upload.
- **Large files (> 50 MB)**: Multipart upload — the file is read in 5 MB chunks, never loaded entirely into memory.

---

## Commands

所有命令输出 JSON 到 stdout。

### upload

```bash
node scripts/agent-storage.js upload '<json>'
```

**JSON 参数：**
- `localPath`（必填）：本地文件绝对路径，支持 `~` 展开
- `remotePath`（可选）：云端目标路径，省略则上传到根目录并保留原文件名
- `conflictStrategy`（可选）：`rename`（默认）| `ask` | `overwrite`
- `purpose`（可选）：`download`（默认，链接点击触发下载）| `preview`（链接在浏览器内预览）
- `expireHours`（可选）：链接有效期，单位为小时，默认 `2`（即 2 小时）

**Output:**

```json
{
  "success": true,
  "upload": {
    "localFile": "/path/to/photo.jpg",
    "remotePath": "photo.jpg",
    "fileSize": 2048576,
    "fileSizeHuman": "2.0 MB",
    "uploadTime": "3.2s",
    "rapidUpload": false
  },
  "downloadUrl": "https://smhxxxxx.gz-c1.smhshare.com/s/xxxxxxxxxx"
}
```

### uploadDir

```bash
node scripts/agent-storage.js uploadDir '<json>'
```

**JSON 参数：**
- `localPath`（必填）：本地文件夹绝对路径，支持 `~` 展开
- `remotePath`（可选）：云端目标目录路径，省略则使用本地文件夹名称
- `conflictStrategy`（可选）：`rename`（默认）| `overwrite`

**说明：**
- 递归上传整个文件夹，自动保留目录结构
- 会先在云端创建对应的目录层级，再逐个上传文件
- 文件按顺序上传（不并行），避免 API 过载

**Output:**

```json
{
  "success": true,
  "uploadDir": {
    "localPath": "/path/to/my-folder",
    "remotePath": "my-folder",
    "totalFiles": 5,
    "successCount": 5,
    "failCount": 0,
    "totalSize": 10485760,
    "totalSizeHuman": "10.0 MB",
    "uploadTime": "8.5s"
  },
  "files": [
    { "file": "doc.pdf", "size": 2048576, "sizeHuman": "2.0 MB", "success": true },
    { "file": "images/photo.jpg", "size": 1048576, "sizeHuman": "1.0 MB", "success": true }
  ]
}
```

### info

```bash
node scripts/agent-storage.js info '<json>'
```

**JSON 参数：**
- `remotePath`（必填）：云端文件路径
- `purpose`（可选）：`download`（默认，链接点击触发下载）| `preview`（链接在浏览器内预览）
- `expireHours`（可选）：链接有效期，单位为小时，默认 `2`（即 2 小时）
- `basePath` / `libraryId` / `spaceId` / `accessToken`（可选）：直接传参模式凭证

**Output:**

```json
{
  "success": true,
  "remotePath": "report.pdf",
  "downloadUrl": "https://smhxxxxx.gz-c1.smhshare.com/s/xxxxxxxxxx",
  "fileInfo": {
    "name": "report.pdf",
    "size": 2048576,
    "type": "application/pdf",
    "creationTime": "2026-03-13T10:00:00Z",
    "modificationTime": "2026-03-13T10:00:00Z"
  }
}
```

### list

```bash
node scripts/agent-storage.js list '<json>'
```

**JSON 参数：**
- `dirPath`（可选）：目录路径，默认 `/`
- `limit`（可选）：最大返回数量，默认 50

### search

```bash
node scripts/agent-storage.js search '<json>'
```

**JSON 参数：**
- `keywords`（必填）：搜索关键字，字符串或字符串数组（数组元素间为"或"关系）
- `scope`（可选）：搜索范围目录路径，如 `photos`；不填则搜索整个空间
- `limit`（可选）：最大返回数量，默认 20，取值范围 [1, 100]
- `marker`（可选）：分页标识，用于获取后续页
- `inExtnames`（可选）：限定文件后缀，字符串或字符串数组，如 `["pdf","docx"]`
- `excludeExtnames`（可选）：排除文件后缀，字符串或字符串数组
- `fileTypes`（可选）：文件类型过滤，取值 `all` | `dir` | `file` | `symlink`

> **注意**：搜索仅支持按文件名匹配（`type: "filename"`），不支持全文内容检索。

**Output:**

```json
{
  "success": true,
  "keywords": ["报告"],
  "type": "filename",
  "total": 3,
  "nextMarker": null,
  "results": [
    {
      "name": "周报告.pdf",
      "type": "file",
      "size": 2048576,
      "sizeHuman": "2.0 MB",
      "contentType": "application/pdf",
      "creationTime": "2026-03-13T10:00:00Z",
      "modificationTime": "2026-03-13T10:00:00Z",
      "text": null,
      "textPage": null,
    }
  ]
}
```

### mkdir

```bash
node scripts/agent-storage.js mkdir '<json>'
```

**JSON 参数：**
- `dirPath`（必填）：要创建的文件夹路径，如 `photos` 或 `docs/2026`
- `conflictStrategy`（可选）：`rename`（默认）| `ask` | `overwrite`

**Output:**

```json
{
  "success": true,
  "dirPath": "photos",
  "message": "文件夹 \"photos\" 创建成功"
}
```

---

## Full Example

```bash
# Step 0: 安装 smh-node-sdk（首次使用前执行一次）
npm install -g smh-node-sdk@^1.0.8

# Step 1: 上传文件
node scripts/agent-storage.js upload '{"localPath":"/path/to/report.pdf","conflictStrategy":"rename"}'

# Step 2: 查询文件信息
node scripts/agent-storage.js info '{"remotePath":"report.pdf"}'

# Step 3: 列出云端文件
node scripts/agent-storage.js list '{"dirPath":"/","limit":20}'

# Step 4: 搜索文件（按文件名）
node scripts/agent-storage.js search '{"keywords":"report"}'

# Step 5: 上传整个文件夹
node scripts/agent-storage.js uploadDir '{"localPath":"/path/to/my-folder","conflictStrategy":"rename"}'

# Step 6: 创建文件夹
node scripts/agent-storage.js mkdir '{"dirPath":"photos"}'
```

---

## Pitfalls

### Error handling

所有命令输出 JSON 到 stdout。错误也以 JSON 返回：`{"success": false, "error": "..."}`

| 错误 | 处理方式 |
|------|---------|
| 上传失败（`success: false`） | 告诉用户："文件上传失败：{具体原因}。你可以稍后再试，或者检查网络连接。" |
| 同名冲突（`conflict: true`） | 询问用户选择覆盖、重命名或取消 |
| 文件不存在 | 让用户确认路径 |
| 网络错误 | 重试 2 次，间隔 3s；仍失败告知用户 |
| 配置缺失 | 提示用户在 `~/.tencentAgentStorage/.env`、`~/.openclaw/openclaw.json` 的 `env` 字段或 `~/.hermes/.env` 中添加 `smh_*` 配置 |

**上传失败对话模板**（当 `success: false` 时必须使用）：

> ❌ 文件上传失败：{error 中的具体原因}。
>
> 你可以：
> 1. 🔄 重试 — 重新上传这个文件
> 2. ❌ 取消 — 暂时不上传

### Prohibited actions

- **NEVER** 在 `success: false` 时展示下载链接
- **NEVER** 在上传失败时不告知用户，必须明确提示"文件上传失败"及原因
- **NEVER** 硬编码或暴露 SMH 凭证给用户
- **NEVER** 未经用户主动要求就上传其本地个人文件
- **NEVER** 跳过执行通知："链接已生成，有效期 2 小时，可直接在浏览器或手机中打开"
- **NEVER** 在用户未明确要求覆盖时使用 `conflictStrategy: "overwrite"`
- **NEVER** 把含 `accessToken` 的中转链接（如 `https://api.tencentsmh.cn/...?access_token=...`）发给用户。返回给用户的**必须是带 COS 签名的直链**（域名为 `*.tencentsmhuc.cn`，参数含 `q-sign-algorithm` 和 `q-signature`），即脚本输出的 `downloadUrl` 字段
- **NEVER** 截断、省略或用 `...` 缩写链接。发给用户的下载链接/预览链接**必须是脚本返回的完整 URL**，一个字符都不能少。链接通常很长（含签名参数），这是正常的，**必须原样完整输出**

### Common mistakes

- 用户说"上传文件"但没指定路径 → 追问："你要上传哪个文件？告诉我文件路径或文件名就行。"
- 用户说"确定上传 xxx"或"把 xxx 发给我" → 直接执行上传（`conflictStrategy: "rename"`）
- **同名文件冲突**：默认使用 `conflictStrategy: "rename"`，自动重命名保证上传成功。只有用户明确要求覆盖时才用 `overwrite`，用户明确要求先确认时才用 `ask`
- 文件默认上传到云空间根目录，用户可通过 `remotePath` 参数指定目标路径
- 下载链接为通过 SDK `infoFile({ purpose: 'download' })` 获取的带签名 COS 直链（`https://bucket-xxxxx.tencentsmhuc.cn/...?q-sign-algorithm=sha1&q-signature=...`），可直接在浏览器或手机中打开预览/下载，**有效期约 2 小时**。**必须原样完整输出此链接，禁止截断或省略任何部分**
- 批量上传按顺序处理（不并行），避免 API 过载
- **执行通知**：每次上传完成后必须告知用户："链接已生成，有效期 2 小时，可直接在浏览器或手机中打开"

---

## Verification

Upload was successful when ALL of the following are true:

1. Script output contains `"success": true`
2. `downloadUrl` field is present and non-empty
3. Agent delivered the download link to the user with the execution notice: "链接已生成，有效期 2 小时，可直接在浏览器或手机中打开"

To verify a previously uploaded file still exists:

```bash
node scripts/agent-storage.js info '{"remotePath":"<filename>"}'
```

If the response contains `"success": true`, the file is accessible and a fresh download link is returned.
