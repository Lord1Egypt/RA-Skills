# WeChat Fetch v3.0

微信公众号文章抓取工具 v3.0，在 v2.0 基础上新增：**Lite 轻量版**、**免登录模式**、**批量抓取**、**图片下载**、**多格式输出**。

## 快速开始

### Lite 版（推荐，低资源）

```bash
# 安装依赖
pip install beautifulsoup4 requests

# 单篇抓取
python3 scripts/wechat_fetch_lite.py "https://mp.weixin.qq.com/s/xxxxx"

# 指定格式
python3 scripts/wechat_fetch_lite.py "https://mp.weixin.qq.com/s/xxxxx" --format json

# 批量抓取
python3 scripts/wechat_fetch_lite.py --batch urls.txt --output ./articles --delay 3
```

### Playwright 版（需浏览器）

```bash
# 安装依赖
pip install playwright beautifulsoup4 requests
playwright install chromium

# 单篇抓取（免登录模式）
python3 scripts/wechat_fetch_v3.py "https://mp.weixin.qq.com/s/xxxxx" --no-login

# 批量抓取（带重试）
python3 scripts/wechat_fetch_v3.py --batch urls.txt --output ./articles \
  --no-login --max-retries 3 --retry-delay 5
```

## 特性

- ✅ **Lite 轻量版** - 无需浏览器，低资源消耗
- ✅ **免登录模式** - 无需扫码，直接抓取
- ✅ **批量抓取** - 支持多 URL 批量下载（双版本）
- ✅ **图片下载** - 自动下载文章图片
- ✅ **多格式输出** - Markdown/HTML/JSON/TXT
- ✅ **重试机制** - Playwright 版支持自动重试

## 版本选择

| 版本 | 适用场景 | 资源需求 | 批量抓取 |
|------|----------|----------|----------|
| **Lite** | 快速抓取、低内存环境 | 低 | ✅ |
| **Playwright** | 需要 Cookie、复杂页面 | 高 | ✅ |

## 详细文档

见 [SKILL.md](SKILL.md)

## 许可证

MIT-0
