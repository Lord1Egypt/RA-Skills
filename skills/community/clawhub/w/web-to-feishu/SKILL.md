---
name: web-to-feishu
label: 网页内容转飞书/ima文档
description: >
  将任意网页链接或本地文件一键转为结构化 Markdown，并保存到飞书云文档或腾讯 ima 笔记。
  支持的信源：(1) X/Twitter 推文、长文 Article、Thread 线程；(2) 微信公众号文章；
  (3) YouTube 视频；(4) 任意 HTML 网页；(5) 本地文件：PDF、Word、PPT、Excel、图片、音频等。
  工作流：自动识别 URL/文件类型 → 路由到最佳抓取工具 → 结构化 Markdown → 选择性保存到飞书/ima。
  触发词：转文档、抓网页存飞书、网页转文档、web to feishu、url转文档、文件转飞书、存到ima。
  当用户提供任意 URL 或本地文件并要求转存为文档时触发。
---

# 网页内容转飞书/ima文档

将任意网页链接或本地文件一键转为结构化 Markdown，并保存到飞书云文档或腾讯 ima 笔记。

## 支持的信源

| 信源 | URL 特征 | 抓取方式 |
|------|---------|---------|
| X/Twitter | `x.com` / `twitter.com` | x-tweet-fetcher |
| 微信公众号 | `mp.weixin.qq.com` | markitdown-plus |
| YouTube | `youtube.com` / `youtu.be` | markitdown-plus |
| 任意网页 | 其他 `http(s)://` 链接 | markitdown-plus |

### 本地文件支持

| 类型 | 扩展名 |
|------|--------|
| PDF | `.pdf` |
| Word | `.docx` / `.doc` |
| PowerPoint | `.pptx` / `.ppt` |
| Excel | `.xlsx` / `.xls` |
| 图片 | `.png` `.jpg` `.jpeg` `.gif` `.webp` |
| 音频 | `.mp3` `.wav` `.m4a` `.flac` |
| 数据 | `.csv` `.json` `.xml` |

## 输出目的地

| 目的地 | 环境变量 | 说明 |
|--------|---------|------|
| Markdown 文件 | 无 | 默认选项，始终生成 |
| 飞书云文档 | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` | 参考 `references/feishu-setup.md` |
| 腾讯 ima | `IMA_CLIENT_ID` + `IMA_API_KEY` | **云端 API**，无需本地客户端，参考 `references/ima-setup.md` |

## 安全配置

⚠️ **凭证必须通过环境变量配置**，禁止硬编码：

### 飞书配置

```bash
# 设置环境变量
$env:FEISHU_APP_ID = "your_app_id"
$env:FEISHU_APP_SECRET = "your_app_secret"
```

参考 [references/feishu-setup.md](references/feishu-setup.md) 获取凭证。

### ima 配置

```bash
# 设置环境变量
$env:IMA_CLIENT_ID = "your_client_id"
$env:IMA_API_KEY = "your_api_key"
```

参考 [references/ima-setup.md](references/ima-setup.md) 获取凭证。

## 工作流

### 步骤 1：转换为 Markdown

```bash
python3 scripts/web_to_md.py --url "<url_or_path>" --output <output.md>
```

路由逻辑：
- **X/Twitter** → x-tweet-fetcher 抓取 JSON → tweet_to_md.py 结构化转换
- **其他所有** → markitdown-plus 直接转换

### 步骤 2：存入目的地

#### 飞书云文档

```python
from scripts.feishu_client import FeishuClient

client = FeishuClient()
result = client.create_document(title="文档标题", content_md=markdown_content)
print(f"文档 URL: {result['url']}")
```

#### 腾讯 ima

```python
from scripts.ima_client import IMAClient

client = IMAClient()
result = client.create_note(title="笔记标题", content=markdown_content)
print(f"笔记 URL: {result['url']}")
```

### 验证连接

```bash
# 验证飞书
python scripts/feishu_client.py --action test

# 验证 ima
python scripts/ima_client.py --action test
```

## 故障处理

| 问题 | 解决方案 |
|------|---------|
| x.com SSL 超时 | x-tweet-fetcher 使用 FxTwitter API 中转 |
| markitdown 模块丢失 | `pip install markitdown` |
| 微信反爬拦截 | markitdown 自动用移动端 UA 重试 |
| 飞书凭证无效 | 检查 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` |
| ima 凭证无效 | 检查 `IMA_CLIENT_ID` 和 `IMA_API_KEY` |

## 依赖

| 依赖 | 安装 |
|------|------|
| markitdown-plus | `pip install markitdown` |
| x-tweet-fetcher | 克隆到 `~/.aily/workspace/skills/x-tweet-fetcher` |
| requests | `pip install requests` |
| python-dotenv | `pip install python-dotenv` |
