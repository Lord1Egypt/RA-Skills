# Scrapling Fetch - 智能网页抓取工具

<div align="center">

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-green)](https://clawhub.com/skill/scrapling-fetch)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Price](https://img.shields.io/badge/price-$0.01%2Fcall-orange)](https://skillpay.me/dashboard/skills)

**绕过反爬机制的智能抓取工具 | 支持微信公众号、Medium、Cloudflare 等**

[English](#english) | [中文](#中文)

</div>

---

## 中文

### ✨ 特性

- ✅ **绕过反爬机制** - 支持 Cloudflare Turnstile、微信公众号等主流反爬
- ✅ **双引擎支持** - Scrapling（绕过反爬）+ Jina Reader（快速抓取）
- ✅ **自适应选择器** - 网站改版也能自动定位元素
- ✅ **付费集成** - 支持 SkillPay 计费系统，自动扣费
- ✅ **多格式输出** - JSON / Markdown / 纯文本
- ✅ **零配置启动** - `pip install` 即可使用

### 🚀 快速开始

#### 安装依赖

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装 Scrapling
pip install 'scrapling[all]'

# 安装浏览器引擎
playwright install chromium
```

#### 免费版本

```python
from scrapling.fetchers import StealthyFetcher

# 抓取微信公众号
url = "https://mp.weixin.qq.com/s/xxxxx"
page = StealthyFetcher.fetch(url, headless=True)

# 提取内容
title = page.css('h1.rich_media_title::text').get()
content = page.css('div.rich_media_content').get()
```

#### 付费版本（自动扣费）

```bash
# 配置 API Key
export BILLING_API_KEY="sk_your_key"

# 调用（自动扣 $0.01）
python3 fetch_paid.py "https://mp.weixin.qq.com/s/xxxxx" --user-id user123
```

### 💰 计费说明

| 项目 | 说明 |
|------|------|
| **单价** | $0.01 USDT / 次 |
| **计费模型** | 1 USDT = 1000 tokens |
| **最低充值** | 8 USDT |
| **支付方式** | BNB Chain USDT |
| **平台费** | 5% |

### 📊 使用场景

| 场景 | 推荐引擎 | 成功率 |
|------|---------|--------|
| 微信公众号 | Scrapling | >95% |
| Medium 博客 | Scrapling | >90% |
| Substack | Scrapling | >85% |
| 普通网站 | Jina Reader | >95% |
| 推特/微博 | ❌ | 需登录 |

### 🔧 API 接口

#### 查询余额

```bash
curl -X GET "https://skillpay.me/api/v1/billing/balance?user_id=xxx" \
  -H "X-API-Key: YOUR_API_KEY"
```

#### 扣费

```bash
curl -X POST "https://skillpay.me/api/v1/billing/charge" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"xxx","skill_id":"7b495410-fb3e-44ff-9c71-9cd1260bb8b9","amount":0.01}'
```

### 📦 安装为 OpenClaw 技能

```bash
# 从 ClawHub 安装
npx clawhub install scrapling-fetch

# 或手动安装
git clone https://github.com/your-repo/scrapling-fetch.git
cp -r scrapling-fetch ~/.openclaw/skills/
```

### 📈 性能对比

| 工具 | 微信公众号 | Medium | 速度 |
|------|-----------|--------|------|
| **Scrapling Fetch** | ✅ | ✅ | 3s |
| Jina Reader | ❌ 403 | ✅ | 1.4s |
| web_fetch | ❌ | ⚠️ | 1s |
| BeautifulSoup | ❌ | ❌ | - |

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 📄 License

MIT License

---

## English

### ✨ Features

- ✅ **Bypass Anti-Bot** - Support Cloudflare Turnstile, WeChat Official Accounts, etc.
- ✅ **Dual Engine** - Scrapling (anti-bot) + Jina Reader (fast)
- ✅ **Adaptive Selectors** - Auto-locate elements even when site changes
- ✅ **Billing Integration** - SkillPay support with auto-charging
- ✅ **Multiple Formats** - JSON / Markdown / Plain text
- ✅ **Zero Config** - Just `pip install` and go

### 🚀 Quick Start

```bash
# Install
pip install 'scrapling[all]'
playwright install chromium

# Usage
python3 fetch.py "https://example.com"
```

### 💰 Pricing

- **Price**: $0.01 USDT per call
- **Min Deposit**: 8 USDT
- **Payment**: BNB Chain USDT

### 📦 Install as OpenClaw Skill

```bash
npx clawhub install scrapling-fetch
```

---

<div align="center">

**Made with ❤️ by [Your Name]**

[ClawHub](https://clawhub.com/skill/scrapling-fetch) • [Documentation](#) • [Report Bug](https://github.com/your-repo/scrapling-fetch/issues)

</div>
