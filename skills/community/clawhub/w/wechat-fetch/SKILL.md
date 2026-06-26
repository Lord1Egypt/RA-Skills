---
name: wechat-fetch
description: 微信公众号文章抓取工具 v3.0 - Lite轻量版 + Playwright版，支持免登录、批量抓取、图片下载、多格式输出
version: "3.0.0"
author: jackyfan01
keywords:
  - "微信文章抓取"
  - "微信公众号"
  - "批量抓取"
  - "免登录"
  - "图片下载"
triggers:
  - "抓取微信文章"
  - "批量下载公众号"
  - "微信文章 v3"
---

# WeChat Fetch v3.0 - 微信文章抓取工具

微信公众号文章抓取工具 v3.0，在 v2.0 基础上新增：**免登录模式**、**批量抓取**、**图片下载**、**多格式输出**。

## 新增特性 (v3.0)

| 特性 | 说明 |
|------|------|
| ✅ **免登录模式** | 无需扫码登录，直接抓取公开文章 |
| ✅ **批量抓取** | 支持从文件读取多个 URL 批量下载 |
| ✅ **图片下载** | 自动下载文章图片到本地 |
| ✅ **多格式输出** | Markdown/HTML/JSON/TXT 四种格式 |

## 使用方法

### 版本选择

| 版本 | 适用场景 | 资源需求 | 批量抓取 |
|------|----------|----------|----------|
| **Lite 版** | 快速抓取、低内存环境 | 低（无需浏览器）| ✅ 支持 |
| **Playwright 版** | 需要 Cookie 登录、复杂页面 | 高（需 Chromium）| ✅ 支持 |

### 1. Lite 版（推荐）

```bash
# 基本用法
python3 scripts/wechat_fetch_lite.py "https://mp.weixin.qq.com/s/xxxxx"

# 指定输出格式
python3 scripts/wechat_fetch_lite.py "https://mp.weixin.qq.com/s/xxxxx" \
  --format html --output article.html

# 下载图片
python3 scripts/wechat_fetch_lite.py "https://mp.weixin.qq.com/s/xxxxx" \
  --download-images --output article.md

# 批量抓取
python3 scripts/wechat_fetch_lite.py --batch urls.txt --output ./articles \
  --format markdown --delay 3
```

### 2. Playwright 版（需 Cookie 登录时）

```bash
# 免登录模式
python3 scripts/wechat_fetch_v3.py "https://mp.weixin.qq.com/s/xxxxx" --no-login

# Cookie 模式（需预先登录）
python3 scripts/wechat_fetch_v3.py "https://mp.weixin.qq.com/s/xxxxx"

# 批量抓取（带重试）
python3 scripts/wechat_fetch_v3.py --batch urls.txt --output ./articles \
  --no-login --max-retries 3 --retry-delay 5
```

### 2. 批量抓取

```bash
# 创建 URL 列表文件 urls.txt
echo "https://mp.weixin.qq.com/s/xxx1" > urls.txt
echo "https://mp.weixin.qq.com/s/xxx2" >> urls.txt
echo "https://mp.weixin.qq.com/s/xxx3" >> urls.txt

# 批量抓取
python3 scripts/wechat_fetch_v3.py --batch urls.txt --output ./articles \
  --no-login --download-images --format markdown
```

### 3. Python API

**Lite 版（推荐）:**
```python
from scripts.wechat_fetch_lite import WeChatFetcherLite

fetcher = WeChatFetcherLite()

# 单篇抓取
result = fetcher.fetch_single(
    url="https://mp.weixin.qq.com/s/xxxxx",
    download_images=True,
    output_format="markdown"
)
```

**Playwright 版:**
```python
from scripts.wechat_fetch_v3 import WeChatFetcher

fetcher = WeChatFetcher()

# 单篇抓取
result = fetcher.fetch_single(
    url="https://mp.weixin.qq.com/s/xxxxx",
    no_login=True,
    download_images=True,
    output_format="markdown"
)

# 批量抓取
results = fetcher.fetch_batch(
    urls=["url1", "url2", "url3"],
    output_dir="./articles",
    no_login=True,
    download_images=True,
    output_format="json"
)
```

## 参数说明

### Lite 版参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 微信文章 URL | - |
| `-o, --output` | 输出文件路径 | - |
| `--batch` | 批量抓取文件（每行一个URL） | - |
| `--download-images` | 下载图片到本地 | False |
| `--format` | 输出格式 (markdown/html/json/txt) | markdown |
| `--timeout` | 超时时间（秒） | 30 |
| `--delay` | 请求间隔（秒） | 2 |

### Playwright 版参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 微信文章 URL | - |
| `-o, --output` | 输出文件/目录路径 | - |
| `--batch` | 批量抓取文件路径 | - |
| `--no-login` | 免登录模式 | False |
| `--download-images` | 下载图片到本地 | False |
| `--format` | 输出格式 (markdown/html/json/txt) | markdown |
| `--headless` | 无头模式 | True |
| `--timeout` | 超时时间（秒） | 30 |
| `--max-retries` | 最大重试次数（批量模式） | 3 |
| `--retry-delay` | 重试间隔（秒） | 5 |

## 输出格式对比

| 格式 | 说明 | 适用场景 |
|------|------|----------|
| **Markdown** | 标准 Markdown，含元数据 | 通用，推荐 |
| **HTML** | 完整 HTML 页面 | 网页展示 |
| **JSON** | 结构化数据 | 程序处理 |
| **TXT** | 纯文本 | 简单阅读 |

## 版本对比

| 特性 | Lite 版 | Playwright 版 (v3) | Cookie 模式 (v2) |
|------|---------|-------------------|-----------------|
| **资源需求** | 低 | 高 | 高 |
| **速度** | 快 | 中等 | 中等 |
| **稳定性** | 高 | 中 | 高 |
| **Cookie 登录** | ❌ | ✅ | ✅ |
| **批量抓取** | ✅ | ✅ | ❌ |
| **图片下载** | ✅ | ✅ | ✅ |
| **多格式输出** | ✅ | ✅ | ✅ |
| **重试机制** | ❌ | ✅ | ❌ |
| **推荐场景** | 日常使用 | 复杂需求 | 私密文章 |

## 批量抓取示例

```bash
# 1. 准备 URL 文件
cat > urls.txt << 'EOF'
https://mp.weixin.qq.com/s/article1
https://mp.weixin.qq.com/s/article2
https://mp.weixin.qq.com/s/article3
EOF

# 2. 执行批量抓取
python3 scripts/wechat_fetch_v3.py \
  --batch urls.txt \
  --output ./articles \
  --no-login \
  --download-images \
  --format markdown

# 3. 查看结果
ls ./articles/
# article_001.md  article_002.md  article_003.md  images/  batch_report.json
```

## 图片下载说明

使用 `--download-images` 参数时：
- 图片会下载到 `images/` 子目录
- Markdown 中的图片链接会替换为本地相对路径
- 支持常见格式：jpg, png, gif, webp

```
articles/
├── article_001.md
├── article_002.md
└── images/
    ├── image_001.jpg
    ├── image_002.png
    └── image_003.gif
```

## 故障排除

### 免登录模式抓取失败

**可能原因：**
- 文章需要登录才能查看
- 触发微信反爬机制
- 页面结构变化

**解决：**
- 尝试使用 Cookie 模式
- 增加 `--timeout` 时间
- 添加延迟避免频繁请求

### 图片下载失败

**可能原因：**
- 图片 URL 过期
- 网络问题
- 图片需要登录权限

**解决：**
- 使用 Cookie 模式
- 检查网络连接
- 手动下载缺失图片

### 批量抓取中断

**解决：**
- 查看 `batch_report.json` 了解失败详情
- 从失败位置继续抓取
- 调整请求间隔时间

## 更新日志

### v3.0.0 (2026-03-23)
- ✅ 新增 Lite 轻量版（无需浏览器）
- ✅ 新增免登录模式
- ✅ 新增批量抓取功能（Lite + Playwright）
- ✅ 新增图片下载功能
- ✅ 新增多格式输出（HTML/JSON/TXT）
- ✅ 优化代码结构，更易扩展
- ✅ 添加批量抓取报告
- ✅ 添加重试机制（Playwright 版）

### v2.0.1 (2026-03-20)
- ✅ 使用持久化浏览器上下文
- ✅ 复用已登录 Cookie
- ✅ 添加 Cookie 自动监控
- ✅ 支持无头模式

## 依赖

```bash
pip install playwright beautifulsoup4 requests
playwright install chromium
```

## 许可证

MIT-0 · Free to use, modify, and redistribute. No attribution required.
