---
name: "☁️ TCED Cloud Drive | 腾讯云企业网盘"
description: "☁️ TCED Cloud Drive | 腾讯云企业网盘集成技能

Manage Tencent Cloud Enterprise Drive (TCED) via MCP tools. Upload, download, browse, search files across personal and team spaces with OAuth2 authentication.

通过 MCP 工具操作腾讯云企业网盘（TCED/SMH），支持文件上传、下载、浏览、搜索，多账号认证与多空间切换。

触发关键词：企业网盘、网盘、TCED、SMH、cloud drive、file upload、file download、file manager、cloud storage、文件上传、文件下载、云端文件、个人空间、团队空间。"
---

# 腾讯云企业网盘 (TCED) 技能

通过 tced-mcp MCP 工具操作腾讯云企业网盘，支持 OAuth2 授权认证、空间管理和文件操作。

## 前置要求

| 要求 | 说明 |
|------|------|
| **Node.js** | >= 18.0.0 |
| **npm / npx** | 随 Node.js 安装，用于获取和运行 `tced-mcp` |
| **浏览器** | 任意浏览器即可（可在本机或其他设备上打开授权链接） |
| **网络访问** | 需能访问 `pan.tencent.com`（授权页面）和 `api.tencentsmh.cn`（API 端点） |
| **本地凭据存储** | `~/.tced-mcp/auth.json` — 存储 OAuth2 Token 和配置（自动创建） |

> **⚠️ 凭据安全**：`~/.tced-mcp/auth.json` 中包含 OAuth2 AccessToken 和 RefreshToken。建议确保该文件权限为 `600`（仅所有者可读写）：
> ```bash
> chmod 600 ~/.tced-mcp/auth.json
> ```

## 概览

TCED MCP Server 基于 OAuth2 第三方授权模式，调用 `login` 获取授权链接，用户在浏览器中完成授权后，将授权码传回 `login(code)` 即可操作已授权的空间和文件。支持桌面和无界面服务器（headless）两种场景。

| 类别 | 工具 | 说明 |
|------|------|------|
| 认证 | `login` | 发起 OAuth2 授权（两阶段：获取授权 URL → 传入 code 完成登录） |
| 认证 | `logout` | 登出账号 |
| 认证 | `list_accounts` | 列出所有已登录账号 |
| 认证 | `switch_account` | 切换活跃账号 |
| 认证 | `current_account` | 查看当前账号信息 |
| 空间 | `list_authorized_spaces` | 列出已授权空间 |
| 空间 | `switch_space` | 切换到指定空间 |
| 空间 | `current_space` | 查看当前活跃空间 |
| 文件 | `upload_file` | 上传文件（本地文件或文本内容） |
| 文件 | `download_file` | 下载文件（获取链接或保存到本地） |
| 文件 | `file_info` | 查看文件/目录详情 |
| 文件 | `list_directory` | 列出目录内容 |
| 文件 | `search_files` | 搜索文件和目录 |

## 首次使用 — 自动设置

当用户首次要求操作企业网盘时，按以下流程操作：

### 步骤 1：检查 MCP 服务是否可用

尝试调用 `current_account` 检查 tced-mcp 是否已在 MCP 客户端中配置并运行。

- **如果可用**：跳到「OAuth2 授权登录」
- **如果不可用**：继续步骤 2

### 步骤 2：配置 MCP 客户端

tced-mcp 已发布到 npm，无需手动安装。只需在 MCP 客户端配置文件（如 `mcp.json`）中添加：

```json
{
  "mcpServers": {
    "tced-mcp": {
      "command": "npx",
      "args": ["-y", "tced-mcp@1.0.2"],
      "env": {
        "TCED_PAN_DOMAIN": "https://pan.tencent.com",
        "TCED_BASE_PATH": "https://api.tencentsmh.cn"
      }
    }
  }
}
```

> **⚠️ 供应链安全说明**：
> - `args` 中**必须锁定具体版本号**（如 `tced-mcp@1.0.2`），不要使用 `@latest`。锁定版本可防止包被劫持时自动拉取恶意版本。升级时应手动修改版本号并验证 changelog。
> - **必须配置 `env` 字段**，显式指定 `TCED_PAN_DOMAIN` 和 `TCED_BASE_PATH` 为官方生产地址。这两个环境变量会在每次启动时强制覆盖本地缓存（`~/.tced-mcp/auth.json`）中的域名配置，确保 API 请求始终指向可信端点。
> - **不要将 `env` 中的域名修改为非官方地址**，除非你完全了解风险——所有 API 请求（包含 OAuth2 Token）都会发送到配置的端点。

配置完成后重启 MCP 客户端使配置生效。

### 步骤 3：验证安装

也可以使用脚本快速检查环境：

```bash
{baseDir}/scripts/setup.sh --check
```

---

## OAuth2 授权登录

### 检查登录状态

调用 `current_account` 检查是否已登录。已登录则跳到「选择空间」，否则继续登录。

### 发起授权登录（两阶段）

**第一步**：调用 `login()`（不传参数），返回授权 URL。

- **有界面场景**：MCP 会自动尝试打开浏览器（如果打开失败会提示手动访问）
- **无界面场景（headless）**：将授权 URL 复制到任意设备的浏览器中打开

用户在网盘页面（`pan.tencent.com`）完成：
1. 登录企业网盘账号
2. 选择要授权的企业
3. **选择要授权的空间** — ⚠️ 每次授权只选一个空间，AccessToken 与该空间一对一绑定
4. 点击「同意授权」

授权成功后，页面会展示授权码（code），请复制该授权码。

**第二步**：调用 `login(code: "粘贴授权码")`，完成 token 交换。若只授权了一个空间则自动切换到该空间。

> **⚠️ 核心规则**：每个 AccessToken 只对应一个空间。如需操作其他空间，必须重新调用 `login` 授权目标空间。

> **⏰ 超时限制**：授权链接 5 分钟内有效。超时后需重新调用 `login()` 获取新链接。

### 选择空间（多空间场景）

如果授权了多个空间：
1. 调用 `list_authorized_spaces` 获取空间列表
2. 调用 `switch_space(spaceId)` 切换到目标空间

---

## 核心操作流程

### 浏览目录

```
list_directory(filePath: "docs", limit: 50)
```

支持 marker 翻页、排序和筛选，详见 `references/api_reference.md`。

### 搜索文件

```
search_files(keyword: "报告", scope: "fileName")
```

### 文件上传

```
upload_file(filePath: "远端路径", localFilePath: "/本地文件路径")
upload_file(filePath: "远端路径", content: "文件内容")
```

冲突策略：`rename`（默认自动重命名）、`overwrite`（覆盖）、`ask`（提示用户确认）。

### 文件下载

```
download_file(filePath: "远端文件路径")
download_file(filePath: "远端文件路径", localFilePath: "/本地保存路径")
```

### 查看文件信息

```
file_info(filePath: "文件/目录路径")
```

---

## 多账号与多空间管理

### AccessToken 与空间一对一绑定

- **一个 AccessToken = 一个空间**，切换空间需要对应的 AccessToken
- `switch_space` 切换时，若目标空间无有效 AccessToken，需重新 `login` 授权
- `switch_account` 切换账号后，AccessToken 和空间随之切换

### 多账号操作

- `list_accounts` — 查看已登录账号
- `switch_account(accountId)` — 切换活跃账号
- `logout(accountId?)` — 登出指定或当前账号

### Token 自动刷新

AccessToken 过期时自动通过 RefreshToken 刷新；RefreshToken 过期后需重新 `login` 授权。

---

## Resource 与 Prompt

- **Resource** `tced://status` — 查看 MCP Server 完整状态
- **Prompt** `quickstart` — 根据当前状态自动引导下一步操作

## 常见问题排查

### `Application authorization not found`

**现象**：浏览器授权成功，但回调后提示"换取令牌失败: Application authorization not found"。

**原因**：`~/.tced-mcp/auth.json` 中缓存的 `apiBasePath` 指向了错误的环境（如测试域名 `api.test.tencentsmh.cn`），导致用 code 换 token 时调用了错误的 API 端点，该环境没有注册对应的 OAuth2 应用。

**解决**：
1. 确保 `mcp.json` 中 `env.TCED_PAN_DOMAIN` 为 `https://pan.tencent.com`，`env.TCED_BASE_PATH` 为 `https://api.tencentsmh.cn`
2. 手动检查 `~/.tced-mcp/auth.json`，确认 `apiBasePath` 和 `panDomain` 是否指向生产环境
3. 刷新 MCP 连接，重新发起 `login`

> **⚠️ 安全提醒**：`~/.tced-mcp/auth.json` 中的 `apiBasePath` 和 `panDomain` 决定了所有 API 请求（包含 Token）的发送目标。如果被篡改为恶意地址，Token 会泄露。建议通过 `mcp.json` 的 `env` 字段固定域名，每次启动自动覆盖。

### npx 缓存旧版本

**现象**：已在 `mcp.json` 中更新了版本号（如从 `1.0.0` 改为 `1.0.1`），但 MCP 启动后行为还是旧版。

**原因**：npx 会缓存已下载的包到 `~/.npm/_npx/` 目录。

**解决**：
1. 手动清除缓存：`npm cache clean --force`
2. 刷新 MCP 连接（重启进程）
3. 确认 `mcp.json` 中的版本号已更新为目标版本

### 浏览器未唤起

**现象**：调用 `login` 后浏览器没有自动弹出。

**原因**：可能是 `open` 包版本不兼容，或者在无界面环境（SSH/Docker）下运行。

**解决**：这不影响使用。`login()` 返回的授权 URL 可以手动复制到任意设备的浏览器中打开，完成授权后将授权码通过 `login(code: "xxx")` 传回即可。

### MCP 进程未读取最新配置

**现象**：修改了 `~/.tced-mcp/auth.json` 但 MCP 行为没变。

**原因**：MCP 进程在启动时一次性读取配置到内存，运行中修改文件不会生效。进程的 `saveConfig()` 还可能把内存中的旧值写回文件，覆盖你的修改。

**解决**：修改配置后必须**刷新 MCP 连接**（重启进程）。推荐通过 `mcp.json` 的 `env` 字段固定域名（`TCED_PAN_DOMAIN` / `TCED_BASE_PATH`），这样每次启动都会强制覆盖本地缓存，避免手动编辑 `auth.json`。

> **注意**：不要直接编辑 `~/.tced-mcp/auth.json` 中的 `apiBasePath` 或 `panDomain` 字段来切换环境。正确做法是修改 `mcp.json` 的 `env` 配置，然后重启 MCP 进程。

---

## 使用规范

1. **操作前确认状态**：任何文件操作前，确保已登录且已选择空间
2. **路径格式**：云端路径使用相对路径（如 `docs/readme.txt`），不带前导斜杠
3. **下载链接有时效性**：`download_file` 返回的 URL 需尽快使用
4. **切换账号后空间随之切换**：`switch_account` 后需重新确认空间
5. **切换空间需对应 AccessToken**：操作新空间需重新 `login` 授权该空间
6. **错误处理**：工具返回 `isError: true` 时，先检查登录和空间状态
7. **大目录分页浏览**：`list_directory` 默认返回 50 项，使用 `marker` 翻页

## 工具详细参数

详细的工具参数定义和错误处理见 `references/api_reference.md`。
