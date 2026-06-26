---
name: wx-mp-push
description: 自动化微信公众号文章发布，通过 API 创建和管理文章草稿，支持 Markdown 和 HTML 两种输入格式，自动 MD→HTML 转换，支持封面图和正文图片自动上传。用于：发布文章到公众号、创建内容草稿、自动化内容工作流、或设置定时发布系统。
---

# 微信公众号发布器

自动化工具，支持通过 API 发布文章到微信公众号。支持 **Markdown 和 HTML 两种输入格式**，内置 MD→微信HTML 转换器，包含自动 Access Token 管理、多账号支持、封面图和正文图片自动上传、图片 URL 替换和草稿创建功能。

## 快速开始

### 前置要求

用户需要：

- 微信公众号（已认证的订阅号或服务号）
- 微信开发者ID（AppID）和开发者密码（AppSecret），在基本配置中获取
- Python 3.x（Python版本）
- 在微信后台启用功能：access_token、草稿、素材权限

### 配置指南

当用户请求发布到微信时，引导他们完成：

1. **创建配置文件**：复制 `config.example.json` 为 `config.json`
2. **填写凭证**：编辑 `config.json` 填入 AppID 和 AppSecret
3. **安装依赖**：
   - Python: `pip install httpx`
4. **测试连接**：用示例内容运行脚本

### 获取 AppID 和 AppSecret

引导用户：

1. 登录：https://mp.weixin.qq.com
2. 导航：开发 → 基本配置
3. 复制：开发者ID (AppID) 和 开发者密码 (AppSecret)

## 使用模式

### 常见用户请求

**直接发布**：

- "将这篇文章发布到我的公众号"
- "为这个内容创建草稿"
- "发布这篇文章，使用这张封面图"
- "这篇文章里有本地图片，帮我上传并替换"

**定时发布**：

- "下周一上午9点发布这个文章"（创建草稿，用户稍后手动发送）
- "每周五早上发布文章"（使用 OpenClaw cron 任务触发脚本）

**内容格式化**：

- "将这篇 markdown 文章格式化后发布到微信"
- "将这篇博客转换为微信格式并创建草稿"
- "上传这张图片作为封面，正文里的图片也要上传"

**图片处理**：

- "帮我上传这几张图片到公众号"
- "文章里的本地图片自动替换成微信 URL"

### 正文图片自动上传

**智能检测：**

脚本会自动扫描 HTML 内容中的 `<img>` 标签：

- **本地路径**：自动上传并替换为微信素材 URL
- **外部 URL**：自动上传并替换为微信素材 URL

**示例 HTML：**

```html
<section class="article-content">
  <p>这是第一段内容。</p>
  <img src="./images/photo1.jpg" />
  <!-- ✅ 会自动上传 -->
  <p>第二段内容...</p>
  <img src="https://example.com/pic.png" />
  <!-- ⏭️ 跳过，已是 URL -->
  <img src="local.png" />
  <!-- ✅ 会自动上传 -->
</section>
```

**执行后自动变成：**

```html
<section class="article-content">
  <p>这是第一段内容。</p>
  <img src="https://mmbiz.qpic.cn/xxx1/..." />
  <p>第二段内容...</p>
  <img src="https://mmbiz.qpic.cn/xxxx" />
  <img src="https://mmbiz.qpic.cn/xxx2/..." />
</section>
```

### 执行方式

**方法 1：从 Markdown 文件发布（推荐）**

```bash
# 直接发布 .md 文件，自动转 HTML + 上传所有图片
python publish_article.py "文章标题" article.md --from-md --thumb cover.jpg

# 指定图片目录和作者
python publish_article.py "文章标题" article.md --from-md --thumb cover.jpg --content-dir ./images --author "张三"

# 直接传入 Markdown 字符串
python publish_article.py "文章标题" "# Hello **World**" --from-md
```

**方法 2：从 HTML 文件发布**

```bash
python publish_article.py "文章标题" article.html --from-file --thumb cover.jpg --content-dir ./images
```

**方法 3：直接传入 HTML 内容**

```bash
python publish_article.py "标题" "<h1>Hello</h1><p>World</p>"
```

**方法 2：通过 OpenClaw Cron**

创建 cron 任务触发脚本执行：

```bash
python scripts/publish_article.py "定时文章" "<HTML内容>" \
  --config config.json \
  --thumb cover.jpg \
  --content-dir ./images
```

**方法 3：先生成，再发布**

1. 使用 AI 生成文章内容（可包含本地图片路径）
2. 格式化为微信支持的 HTML
3. 执行发布脚本，自动处理所有图片

## 脚本参考

主要发布脚本位于 `scripts/`：

- **publish_article.py**: Python 实现，使用 httpx，支持命令行参数
- **config.example.json**: 配置模板
- **README.md**: 详细的设置和使用说明

**选择版本的考虑：**

- 如果用户偏好 Python 生态或已有 Python 环境，使用 Python 版

## 配置文件格式

config.json 支持多个微信公众号账号：

```json
{
  "wechat": {
    "defaultAccount": "account1",
    "accounts": {
      "account1": {
        "name": "账号名称",
        "appId": "your_app_id",
        "appSecret": "your_app_secret",
        "type": "subscription",
        "enabled": true
      },
      "account2": { ... }
    },
    "apiBaseUrl": "https://api.weixin.qq.com",
    "tokenCacheDir": "./.tokens"
  }
}
```

**关键字段：**

- `appId`: 微信 App ID
- `appSecret`: 微信 App Secret（注意安全保管）
- `type`: "subscription"（订阅号）或 "service"（服务号）
- `enabled`: true/false 启用或禁用账号

## 图片上传支持

### 封面图

- **格式**：JPG、JPEG、PNG
- **大小限制**：不超过 64MB
- **建议尺寸**：900 × 383 像素（2.35:1 比例）
- **用途**：文章列表显示的封面

### 正文图片

- **格式**：JPG、JPEG、PNG、BMP、GIF
- **大小限制**：不超过 2MB（单张）
- **用途**：嵌入在文章内容中
- **自动处理**：脚本自动上传并替换为微信素材 URL

### 使用方式

**1. 封面图单独设置：**

```bash
python publish_article.py "标题" "内容" --thumb cover.jpg
```

**2. 正文图片自动上传：**
只需在 HTML 中使用本地路径，脚本自动处理：

```html
<p>段落</p>
<img src="./img/photo.jpg" />
```

**3. 文字内容 + 多张图片：**

```html
<h1>我的文章</h1>
<p>开头内容...</p>
<img src="header.jpg" />
<p>中间内容...</p>
<img src="diagram.png" />
<p>结尾内容...</p>
<img src="footer.jpg" />
```

### 图片路径说明

**相对路径**（推荐）：

- 默认从当前目录查找
- 可通过 `--content-dir` 指定基础目录
- 示例：`<img src="photo.jpg" />`、`<img src="./images/pic.png" />`

**绝对路径**：

- 直接使用完整路径
- 示例：`<img src="/Users/name/Pictures/photo.jpg" />`

**外部 URL**：

- 不上传，保持原样
- 示例：`<img src="https://example.com/img.jpg" />`

## 文章内容格式

微信需要特定的 HTML 格式：

**基本结构：**

```html
<section class="article-content">
  <p>段落内容...</p>
  <h2>章节标题</h2>
  <p>更多内容...</p>
  <img src="local-img.jpg" />
</section>
```

**重要要求：**

- 使用 `<section class="article-content">` 包裹内容
- 只使用闭合标签（不要使用 `<br/>` 这样的自闭合标签）
- 推荐使用 HTTPS 图片链接
- 避免复杂 CSS（微信有限制）
- 正文图片会自动处理，无需手动上传

## Markdown 支持（自动转换）

**直接发布 Markdown 文件，无需手动转换 HTML！**

脚本内置 MD→微信HTML 转换器，使用 `--from-md` 参数即可：

```bash
python publish_article.py "文章标题" article.md --from-md --thumb cover.jpg
```

### 支持的 Markdown 语法

| 语法             | 转换效果                                             |
| ---------------- | ---------------------------------------------------- | --- | --- | ------------------ |
| `# ~ ######`     | 标题（h1 带下划线装饰，h2 带左边框）                 |
| `**加粗**`       | `<strong>加粗</strong>`                              |
| `*斜体*`         | `<em>斜体</em>`                                      |
| `~~删除线~~`     | `<del>删除线</del>`                                  |
| `![alt](url)`    | 图片（保留所有图片，URL 直接使用，本地路径自动上传） |
| `[text](url)`    | 链接                                                 |
| `- 列表项`       | 无序列表                                             |
| `1. 列表项`      | 有序列表                                             |
| `> 引用`         | 带左边框的引用块                                     |
| `---`            | 分割线                                               |
| 表格 (`          | ---                                                  | --- | `)  | 带边框的 HTML 表格 |
| `` `行内代码` `` | 灰色背景代码样式                                     |
| `代码块`         | 带背景的代码块                                       |

### 图片处理规则

- **外部 URL 图片**（`https://...`）：直接保留在 HTML 中
- **本地路径图片**（`./img/photo.jpg`）：自动上传到微信素材库并替换 URL
- **使用 `--from-md` 时**：自动将 `--content-dir` 设为 .md 文件所在目录

### 使用示例

```bash
# 最简单的用法
python publish_article.py "我的文章" article.md --from-md

# 完整参数
python publish_article.py "文章标题" article.md \
  --from-md \
  --thumb cover.jpg \
  --content-dir ./images \
  --author "作者名" \
  --config config.json
```

---

## 故障排除

**常见错误和解决方案：**

| 错误码         | 原因                 | 解决方案                                                     |
| -------------- | -------------------- | ------------------------------------------------------------ |
| 40001          | AppID/AppSecret 无效 | 检查 config.json 中的凭证                                    |
| 40004          | 不支持的媒体类型     | 检查图片格式，封面图只支持 JPG/PNG，正文支持 JPG/PNG/BMP/GIF |
| 40005          | 不支持的文件类型     | 确认上传的是图片文件                                         |
| 40164          | IP 未在白名单中      | 将服务器 IP 添加到微信白名单                                 |
| 41005          | 媒体文件为空         | 检查图片文件是否损坏                                         |
| 45009          | API 调用频率超限     | 等待或降低频率                                               |
| Token 过期     | 缓存问题             | 删除 .tokens/ 文件夹重试                                     |
| 图片上传失败   | 文件过大             | 封面图<64MB，正文图<2MB                                      |
| 图片路径不存在 | 找不到文件           | 检查路径是否正确，使用 `--content-dir` 指定目录              |

**调试提示：**

1. 检查配置文件存在且是有效 JSON 格式
2. 验证网络连接
3. 确保凭证格式正确（无多余空格）
4. 检查微信后台 API 权限是否启用
5. 验证图片文件存在且格式正确
6. 确认图片大小不超过限制
7. 使用相对路径时检查 `--content-dir` 设置

## 安全注意事项

**重要安全实践：**

1. **保护 AppSecret**：永远不要在脚本中硬编码，始终使用配置文件
2. **Git 忽略**：将 config.json 添加到 .gitignore
3. **Token 缓存**：为 `.tokens/` 目录设置安全权限
4. **用户责任**：明确告知用户凭证安全的重要性
5. **图片安全**：上传的图片会保存到公众号素材库，注意隐私
6. **备份数据**：重要图片请备份，微信素材库有容量限制

## 与 OpenClaw 集成

**集成选项：**

1. **一次性发布**：用户请求发布，执行一次脚本
2. **定时发布**：使用 `cron` 工具安排定期文章发布
3. **工作流集成**：结合文章生成技能实现端到端自动化
4. **消息通知**：发布后通过 `message` 工具发送成功/失败通知
5. **批量处理**：批量上传图片，批量创建草稿

**每周定时发布的 Cron 任务示例：**

```json
{
  "name": "每周微信文章",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 5",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "trigger_wechat_publish"
  }
}
```

当收到系统事件时，Agent 会执行发布脚本。

## 功能特性

**当前支持：**

- ✅ 通过 API 创建文章草稿
- ✅ 管理带缓存的 Access Token
- ✅ 支持多个微信公众号账号
- ✅ 上传封面图片到素材库
- ✅ **自动上传正文图片并替换 URL**
- ✅ 智能检测本地图片和外部 URL
- ✅ 自动图片格式和大小验证
- ✅ 支持封面图 JPG/JPEG/PNG（最大 64MB）
- ✅ 支持正文图 JPG/JPEG/PNG/BMP/GIF（最大 2MB）
- ✅ **内置 Markdown → 微信HTML 转换器**（`--from-md`）
- ✅ 支持标题、加粗、斜体、删除线、列表、引用、表格、代码块、分割线
- ✅ MD 文件中的图片全部保留（URL 直接使用，本地路径自动上传）

**未来扩展：**
后续版本可考虑添加：

- 视频素材上传支持
- 图片库管理（查询、删除）
- 文章草稿管理（编辑、删除）
- 图片 CDN 加速
