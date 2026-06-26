---
name: scrapling-fetch
version: 1.1.0
description: 强力网页内容抓取工具，自动绕过反爬机制（Cloudflare Turnstile、微信公众号等）。使用场景：(1) 微信公众号文章抓取 (2) Medium/Substack 等反爬平台 (3) 需要绕过 Cloudflare 的网站 (4) 常规网页抓取失败时的备选方案。Triggers: "抓取网页", "爬取内容", "公众号文章", "绕过反爬", "微信公众号链接", "无法访问", "403错误", "cloudflare", "反爬"。
---

# Scrapling Fetch - 自适应网页抓取

## 快速开始

### 微信公众号（自动绕过反爬）

```bash
~/.openclaw/workspace/.venv/bin/python3 \
  ~/.openclaw/workspace/skills/scrapling-fetch/scripts/fetch.py \
  "https://mp.weixin.qq.com/s/xxxxxx"
```

### 普通网页（快速模式）

```bash
~/.openclaw/workspace/.venv/bin/python3 \
  ~/.openclaw/workspace/skills/scrapling-fetch/scripts/fetch.py \
  "https://example.com" \
  --fast
```

### 输出格式

默认输出 JSON：
```json
{
  "title": "文章标题",
  "author": "作者",
  "content": "正文内容（Markdown格式）",
  "word_count": 1234
}
```

加 `--text` 参数只输出纯文本。

---

## 工具选择策略

| 网站类型 | 推荐工具 | 原因 |
|---------|---------|------|
| 微信公众号 | Scrapling | 自动绕过反爬 ✅ |
| Medium/Substack | Scrapling | 绕过反爬机制 |
| Cloudflare 保护 | Scrapling | 支持 Turnstile 绕过 |
| 普通技术博客 | Jina（--fast） | 速度快（1.4秒） |
| GitHub/静态页面 | web_fetch | 无需额外工具 |

---

## 脚本说明

### fetch.py

**核心功能：**
- 自动检测网站类型
- 绕过主流反爬机制
- 提取干净的 Markdown 内容
- 支持图片链接保留

**参数：**
- `url` - 必填，目标网址
- `--fast` - 使用 Jina Reader（适合普通网页）
- `--text` - 只输出纯文本（默认 JSON）
- `--max-chars` - 最大字符数（默认 50000）

**示例：**
```bash
# 抓取微信文章
python3 fetch.py "https://mp.weixin.qq.com/s/xxxxx"

# 快速抓取普通网页
python3 fetch.py "https://blog.example.com" --fast

# 限制长度
python3 fetch.py "https://example.com" --max-chars 10000
```

---

## 使用场景

### 1. AI 内容创作流程

```
用户发链接 → scrapling-fetch 抓取 → AI 消化 → 生成内容
```

### 2. 研究资料收集

```bash
# 批量抓取多篇公众号文章
for url in "url1" "url2" "url3"; do
  python3 fetch.py "$url" >> articles.jsonl
done
```

### 3. 失败重试策略

```bash
# web_fetch 失败 → 自动切换 Scrapling
if ! web_fetch "$url"; then
  python3 fetch.py "$url"
fi
```

---

## 技术原理

**Scrapling 核心特性：**
1. **StealthyFetcher** - 模拟真实浏览器，绕过反爬
2. **自适应选择器** - 网站改版也能定位元素
3. **Playwright 引擎** - 无头浏览器渲染

**Jina Reader：**
- API: `https://r.jina.ai/{url}`
- 自动提取正文、去广告
- 速度约 1.4 秒
- 免费限额 200 次/天

---

## 注意事项

1. **微信文章** - Scrapling 成功率 >95%
2. **推特/微博** - 需要登录，此工具无法抓取
3. **付费内容** - 仅能抓取公开部分
4. **频率限制** - 建议 2-3 秒间隔，避免被封

---

## 💰 付费版本（SkillPay 计费）

### 快速开始

```bash
# 付费模式（需要 user_id）
python3 fetch_paid.py "https://mp.weixin.qq.com/s/xxxxx" --user-id user123

# 免费模式（不计费）
python3 fetch_paid.py "https://mp.weixin.qq.com/s/xxxxx" --free
```

### 计费说明

- **单价**: $0.01 USDT / 次
- **计费模型**: 1 USDT = 1000 tokens，每次调用消耗 1 token
- **最低充值**: 8 USDT
- **支付方式**: BNB Chain USDT

### 配置步骤

1. **获取 API Key**
   - 访问 https://skillpay.me/dashboard/config
   - 复制 API Key（以 `sk_` 开头）

2. **修改配置**
   ```python
   # 编辑 fetch_paid.py
   BILLING_API_KEY = 'sk_your_api_key_here'
   ```

3. **测试扣费**
   ```bash
   python3 fetch_paid.py "https://example.com" --user-id test_user
   ```

### 返回示例（余额不足）

```json
{
  "error": "余额不足",
  "balance": 0.005,
  "payment_url": "https://skillpay.me/pay/xxx",
  "hint": "请充值后继续使用"
}
```

### API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/billing/balance` | GET | 查询余额 |
| `/api/v1/billing/charge` | POST | 扣费 |
| `/api/v1/billing/payment-link` | POST | 生成充值链接 |

---

## 📊 收益预期

| 场景 | 调用量/天 | 日收入 | 月收入 |
|------|----------|--------|--------|
| 个人使用 | 10 次 | $0.10 | $3 |
| 小团队 | 100 次 | $1.00 | $30 |
| 公开服务 | 1000 次 | $10.00 | $300 |

---

## 相关技能

- `web_fetch` - 轻量级网页抓取（无反爬绕过）
- `browser` - 浏览器自动化（需要手动操作）
- `xurl` - 推特 API（需配置）

---

## 参考

- Scrapling GitHub: https://github.com/D4Vinci/Scrapling
- Jina Reader: https://jina.ai/reader
