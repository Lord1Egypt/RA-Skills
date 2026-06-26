# TCED MCP Server API Reference

## 认证工具

### login

发起 OAuth2 授权登录。自动唤起浏览器打开网盘授权页面，用户在浏览器中完成授权后自动完成 token 交换。

无参数。

**⚠️ 环境要求**：需要有图形界面环境（桌面系统），不支持无界面服务器（Linux SSH/Docker 等）。

**流程**：
- 启动本地 HTTP 服务器（端口 19526）等待回调
- 唤起网盘页面，用户在网盘页面中完成登录和授权
- 用户授权后网盘自动回调，MCP 用 code 换取 access_token
- 5 分钟超时
- 如已有有效登录，返回当前账号信息

### logout

登出指定账号或当前账号。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| accountId | string | 否 | 要登出的账号 ID（默认当前账号） |

### list_accounts

列出所有已登录的账号。无参数。

返回：账号 ID、名称、组织信息、AccessToken/RefreshToken 状态、登录时间、是否为当前活跃账号。

### switch_account

切换当前活跃账号。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| accountId | string | 是 | 要切换到的账号 ID |

注意：切换后 AccessToken 切换到目标账号的 Token（该 Token 绑定了对应的空间），空间也随之切换。

### current_account

查看当前活跃账号的详细信息。无参数。

返回：账号 ID、名称、OpenId、登录时间、AccessToken/RefreshToken 状态及过期时间、授权范围、关联组织、当前空间信息。

---

## 空间管理工具

### list_authorized_spaces

列出所有已授权的空间。无参数。

返回：空间名称、空间 ID、LibraryId、空间类型（个人空间/企业空间/协作空间）、团队 ID（团队空间特有）。

**注意**：每个 AccessToken 与一个空间一对一绑定。切换到不同空间需要对应空间的 AccessToken，如没有则需重新 `login` 授权该空间。

### switch_space

切换到指定的已授权空间。必须先通过 `list_authorized_spaces` 获取可用空间列表。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| spaceId | string | 是 | 目标空间 ID（从 list_authorized_spaces 中获取） |

切换后自动创建 SMHClient 并配置好 libraryId、spaceId、accessToken。

**重要**：如果目标空间不在 `list_authorized_spaces` 返回的列表中，需重新调用 `login` 唤起网盘页面授权该空间。

### current_space

查看当前活跃空间的详细信息。无参数。

返回：空间名称、类型、空间 ID、LibraryId、AccessToken 状态。

---

## 文件操作工具

> **前置条件**：所有文件操作要求已选择空间（通过 `switch_space`），否则返回错误。

### upload_file

上传文件到当前空间。支持从本地文件上传或直接提供文本内容上传。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| filePath | string | 是 | 云端目标文件路径（如 `docs/readme.txt`） |
| localFilePath | string | 否 | 本地文件路径（与 content 二选一） |
| content | string | 否 | 直接提供文件内容（与 localFilePath 二选一） |
| conflictStrategy | enum | 否 | 冲突策略：`ask`/`rename`(默认)/`overwrite` |

- **localFilePath 模式**：使用 `SMHClient.createUploadTask()` + 事件驱动完成上传
- **content 模式**：使用 `SMHClient.file.simpleUploadFile()` 接口
  - 返回 200 + confirmKey 表示需要继续处理
  - 返回 201 表示秒传成功

### download_file

下载文件。可获取下载链接，或直接下载到本地指定路径。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| filePath | string | 是 | 云端文件路径 |
| localFilePath | string | 否 | 本地保存路径（提供时直接下载到本地） |
| historyId | string | 否 | 历史版本 ID（获取特定版本） |
| purpose | enum | 否 | 用途：`download`/`preview` |

- **localFilePath 模式**：使用 `SMHClient.createDownloadTask()` + 事件驱动下载到本地
- **无 localFilePath**：调用 `SMHClient.file.downloadFile()` 获取带时效性的下载 URL

### file_info

查看文件或目录的详细信息。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| filePath | string | 是 | 文件/目录路径（根目录传空字符串 `""`） |

返回：名称、路径、类型、Inode、创建时间、修改时间、大小、内容类型、ETag、CRC64、文件类型、标签。

### list_directory

列出目录下的文件和子目录。使用 marker 分页模式。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| filePath | string | 否 | 目录路径（根目录传空字符串或不传） |
| limit | number | 否 | 返回数量限制（默认 50，最大 100） |
| marker | string | 否 | 翻页标识（从上次返回的 nextMarker 获取） |
| orderBy | enum | 否 | 排序字段：`name`/`modificationTime`/`size`/`creationTime` |
| orderByType | enum | 否 | 排序方式：`asc`/`desc` |
| filter | enum | 否 | 筛选：`onlyDir`=仅目录 / `onlyFile`=仅文件 |

返回：文件/目录列表（名称、类型、大小、修改时间），以及 nextMarker（如有更多内容）。

### search_files

搜索当前空间中的文件和目录。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 搜索关键词 |
| scope | enum | 否 | 搜索范围：`fileName`(默认)/`ext`/`contentType`/`tag` |
| limit | number | 否 | 返回数量限制（默认 20，最大 100） |
| marker | string | 否 | 翻页标识 |

返回：匹配的文件/目录列表（名称、类型、大小、路径），以及 nextMarker（如有更多结果）。

---

## Resource

### tced://status

返回 MCP Server 完整状态的 Markdown 文档，包含：
- 认证模式（OAuth2 第三方授权）
- App ID
- 认证状态（当前账号、OpenId、AccessToken/RefreshToken 状态、授权范围、账号数量）
- 空间状态（当前空间名称、ID、LibraryId）
- 已授权空间列表

---

## Prompt

### quickstart

快速入门指南。根据当前状态自动引导下一步操作：
- 未登录 → 引导调用 `login` 唤起网盘页面授权
- 已登录未选空间 → 引导选择空间
- 已就绪 → 展示所有可用工具

---

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TCED_PAN_DOMAIN` | 网盘域名 | `https://pan.tencent.com` |
| `TCED_BASE_PATH` | API 基础路径 | `https://api.tencentsmh.cn` |

> **⚠️ 安全说明**：这两个环境变量决定了所有 API 请求（包含 OAuth2 Token）的发送目标。**必须**在 `mcp.json` 的 `env` 中显式配置为官方生产地址，不要指向非可信域名。配置的值会在启动时持久化到本地凭据文件 `~/.tced-mcp/auth.json`。

---

## 错误处理

所有工具在出错时返回 `isError: true` 和错误信息。常见错误：

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| 未选择空间 | 文件操作前未调用 switch_space | 按流程选择空间 |
| OAuth2 Token 无效 | AccessToken 过期且无法自动刷新 | 重新调用 login 授权 |
| 刷新令牌已过期 | RefreshToken 也已过期 | 重新调用 login 授权 |
| 本地文件不存在 | localFilePath 路径错误 | 检查本地文件路径 |
| 文件不存在 | 云端路径错误 | 检查文件路径 |
| 端口已被占用 | 端口 19526 被其他程序占用 | 关闭占用端口的程序或等待占用释放 |
| 授权超时 | 5 分钟内未完成授权 | 重新调用 login |
| 权限不足 | 无操作权限 | 确认授权范围包含所需权限 |

---

## 故障排查

### 端口 19526 被占用

`login` 启动本地 HTTP 服务器监听 OAuth2 回调，如端口被占用：

1. 查找占用进程：`lsof -i :19526`（macOS/Linux）或 `netstat -ano | findstr 19526`（Windows）
2. 如果是之前未关闭的 tced-mcp 进程，终止该进程后重试
3. 如果是其他程序占用，关闭该程序或等待其释放端口

### OAuth2 回调超时

`login` 调用后 5 分钟内未完成授权会超时：

1. 确认浏览器已正常打开网盘授权页面
2. 检查网络连接是否正常（需能访问 `pan.tencent.com`）
3. 确认已在网盘页面点击「同意授权」
4. 超时后直接重新调用 `login` 重试

### Token 刷新失败

AccessToken 过期时自动通过 RefreshToken 刷新。如刷新失败：

1. RefreshToken 已过期 → 重新调用 `login` 授权
2. 网络异常导致刷新请求失败 → 检查网络后重试操作，系统会自动重试刷新
3. 调用 `current_account` 查看 Token 状态，确认是否需要重新授权

### 文件操作返回错误

1. 先调用 `current_space` 确认已选择空间
2. 如未选择空间，调用 `list_authorized_spaces` + `switch_space` 选择
3. 检查云端路径格式：使用相对路径，不带前导斜杠（如 `docs/file.txt` 而非 `/docs/file.txt`）
4. 上传时如遇同名文件冲突，调整 `conflictStrategy` 参数
