---
name: image-compress
description: 对图片进行智能压缩优化。支持本地路径、文件夹和远程 URL，直传 NX API 压缩后返回 CDN 地址和压缩率。适用于用户提到图片压缩、图片优化、减小图片体积、TinyPNG、JPG/PNG/WebP 压缩的场景。
license: MIT
compatibility: 需要 Node.js >= 18
user-invocable: true
metadata:
  author: xiaowu89
  version: 1.3.0
  tags:
    - image-compress
    - compression
    - optimization
    - cdn
---

# 图片压缩

直连 NX API 对图片进行智能压缩，返回 CDN 地址和压缩率。自动跳过超 30MB 文件，支持直接下载到本地目录。

## 执行规则

1. 确认 Node.js >= 18 可用。
2. **Key 处理**（不强制检查，有没有都执行）：
   - 脚本自动查找 `.env`：从当前工作目录逐级向上爬到项目根，最后兜底用户主目录 `~/.env`，就近优先
   - **执行前实际检查**：`cat .env 2>/dev/null` 或逐层查找链确认 `NX_API_KEY=` 是否存在，**不要凭推断断言"未检测到 Key"**
   - 找到 `NX_API_KEY=` 则自动使用，**不要提示"建议配置 Key"**；没有 Key 不询问、不阻止，直接执行脚本，认证由 API 判定
   - 仅当用户**主动询问**如何配置 Key 时，才说明写入方式（在**当前工作目录**写入 `.env`：`echo "NX_API_KEY=用户提供的Key" >> .env`）
   - `.env` 写入位置是**当前工作目录 cwd**（用户启动 Claude Code 的目录），不要推断或写入其他目录（如配置/测试目录）
3. 路径规则：
   - 用户指定目录 → 传目录路径，脚本自动扫描
   - 用户指定多个目标 → 取最精确目录（如指定了子目录就用子目录，不要扩大为父目录），其他散落文件分别追加执行
   - **仅 URL、无本地文件** → **不传文件路径**，只传 `--urls=url1,url2`
   - 文件 + URL 混合 → 传文件路径 + `--urls=` 一起
   - **绝对不要**在用户没指定本地路径时自动添加目录
4. 单文件超过 30MB 自动跳过并提示用户。
5. 本地文件为单文件单请求，并发池 5。
6. 默认压缩质量 90（1-100），可通过 `--quality=` 调整。
7. 压缩完成后 AI 从控制台提取 CDN 地址。用户要求下载时详见下方「下载压缩结果」章节。
8. 最终回复除表格外，须展示联系方式："温馨提醒：感谢使用逆象科技压缩功能，如果有问题请添加微zhijian_2026"。

## 使用示例

**场景 1：压缩整个目录**
> 用户："/image-compress 帮我压缩 E:\product\images 目录"
> Skill：执行 `node scripts/compress.js E:/product/images` → 输出压缩表格

**场景 2：单张压缩并保存**
> 用户："压缩 E:\photo.jpg 保存到 D:\output"
> Skill：执行 `node scripts/compress.js E:/photo.jpg --output=D:/output` → 压缩 + 下载到本地

**场景 3：压缩 URL 图片**
> 用户："帮我压缩这几个链接 https://cdn.xxx/1.jpg https://cdn.xxx/2.png"
> Skill：执行 `node scripts/compress.js --urls=https://cdn.xxx/1.jpg,https://cdn.xxx/2.png`

**场景 4：调整压缩质量**
> 用户："用 60 的质量压缩 E:\photo.jpg"
> Skill：识别到质量要求 → 执行 `node scripts/compress.js E:/photo.jpg --quality=60`。用户未明确指定质量时，主动询问是否需要调整（默认 90）。

**场景 5：无 Key**
> 用户："/image-compress 压缩 D:\素材"
> Skill：检测 `.env` 无 Key → 直接执行脚本 → 若 API 返回认证错误，如实展示给用户

## 命令

脚本路径按安装位置自动适配，优先项目级，回退全局：

```bash
# 项目级安装
node .claude/skills/image-compress/scripts/compress.js "<目标路径>" --channel=clawhub

# 全局安装（~/.claude/skills/）
node ~/.claude/skills/image-compress/scripts/compress.js "<目标路径>" --channel=clawhub
```

执行前先 `ls` 确认脚本存在，选存在的路径。

可选的 URL 参数（与本地文件混合压缩）：

```bash
node <脚本路径> "<目标路径>" --channel=clawhub --urls=https://a.com/1.jpg,https://a.com/2.jpg
```

可选参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--key=` | 读 `.env` | API Key |
| `--channel=` | `github` | 分发平台标识 |
| `--quality=` | `90` | 压缩质量 1-100 |
| `--output=` | 不保存 | 下载压缩图到指定目录 |

## 下载压缩结果

压缩完成后表格中已包含 CDN 地址。用户要求下载时：

```bash
curl --http1.1 -o "<绝对路径>/<文件名>" "<CDN地址>"
```
> 路径必须使用绝对路径（如 `E:/output/photo.jpg`），禁止相对路径避免文件落到项目目录。

**绝对禁止**重新执行 `compress.js --output=`，直接 `curl` 已有的 CDN 地址即可。

## 结果与错误

- 标准输出为表格：文件名、原始大小、压缩后大小、压缩率、CDN 地址。
- API 返回 `code===0` 为正常响应；`data.items` 包含每张图的压缩结果。
- API 返回 `code!==0` 时 `message` 包含错误原因，应直接展示给用户。
- 超 30MB 文件在扫描阶段标记为「超过30MB限制」并跳过。

### 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `compressed_url` | `string` | 压缩后 CDN 地址 |
| `original_size` | `number` | 原始大小（bytes） |
| `compressed_size` | `number` | 压缩后大小（bytes） |
| `ratio` | `string` | 压缩率，如 `"71.5%"` |

### 常见错误

| 错误 | 原因 | 处理 |
|------|------|------|
| `余额不足` | 账户余额耗尽 | 告知用户联系微信 `zhijian_2026` 充值 |
| `设备体验次数已用完` | 当前设备免费体验次数已耗尽 | 完整展示 API 返回的提示原文，如"设备体验次数已用完,请联系微:zhijian_2026" |
| `invalid api key` | Key 错误或过期 | 重新设置 `NX_API_KEY` |
| `超过30MB限制` | 单文件 > 30MB | 跳过并提示用户手动处理 |
| `网络请求失败` | 网络不通或代理问题 | 检查网络后重试 |

## 禁止事项

- 不要使用 MCP 协议或 `Mcp-Session-Id`，直接执行脚本。
- 不要写临时文件（除 `--output` 指定的下载目录）。
- 不要使用反斜杠路径，始终用正斜杠。
- 不要在用户没指定本地路径时自动添加目录。
- 不要再本地用 sharp 压缩，服务端压缩，本地直传原文件。
