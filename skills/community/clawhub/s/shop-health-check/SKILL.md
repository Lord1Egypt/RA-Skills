---
name: shop-health-check
description: 跨境电商店铺健康度自动巡检 Skill。支持多店铺配置，定时检查站点可用性、响应时间、SSL证书健康度、关键页面404/内容缺失，异常时自动推送到飞书。
tags:
  - monitoring
  - uptime
  - ssl
  - shop-health
  - e-commerce
  - feishu
  - cron
---

# 店铺健康巡检 Skill

## 何时使用

- 用户说："检查店铺健康度"、"巡检店铺"、"帮我监控店铺是否宕机"、"店铺健康报告"
- 作为定时任务（Cron / Heartbeat）定期执行，异常时推送到飞书

## 前置条件

- Python 3.8+，需要 `requests`、`beautifulsoup4`、`urllib3`、`python-dateutil` 库
- 配置好多店铺信息（`config/shops.conf`）
- 飞书 Webhook 已配置（环境变量 `FEISHU_WEBHOOK`，或脚本内配置）

## 配置文件 `config/shops.conf`

```ini
[DEFAULT]
# 默认阈值（可被店铺级别覆盖）
response_timeout = 3      # 响应时间阈值（秒）
ssl_warning_days = 14     # SSL 剩余天数警告阈值
check_sample_size = 5     # 分类页抽检商品数量

[shop1]
name = 店铺1
domain = www.example.com
base_url = https://www.example.com
# 站点可用性检查的页面路径（逗号分隔，留空则用默认）
check_paths = /, /c/best-sellers, /cart, /checkout
# 要检查的分类页路径（用于抽检商品页）
category_paths = /c/best-sellers, /c/new-arrivals, /c/sale
# 可选：覆盖全局阈值
response_timeout = 5
ssl_warning_days = 30

[shop2]
name = 店铺2
domain = shop2.example.com
base_url = https://shop2.example.com
check_paths = /, /products, /collections/all
category_paths = /collections/all
```

> **使用提醒**：首次使用前，请先配置 `config/shops.conf`，填入真实的店铺域名和路径。

## 工作流程

脚本按以下顺序执行：

1. **`check_sites.py`** — 检查站点可用性和响应时间
2. **`check_ssl.py`** — 检查 SSL 证书过期和状态
3. **`check_404.py`** — 爬取分类页 → 抽检商品页 → 检测404和错误内容
4. **`report.py`** — 汇总所有结果，判定告警，推送到飞书

## 命令示例

### 完整巡检

```bash
cd ~/.openclaw/skills/shop-health-check
python3 scripts/report.py
```

### 指定店铺巡检

```bash
python3 scripts/report.py --shop shop1
```

### 查看帮助

```bash
python3 scripts/report.py --help
```

## 输出示例（正常）

```
✅ 店铺健康巡检报告 | 2026-03-30 11:00

📦 shop1 (www.example.com)
✅ 站点可用性：全部正常（2/2 检查点）
   - / : 200 (1.2s)
   - /c/best-sellers : 200 (0.9s)
✅ SSL证书：正常（剩余 89 天）
🔍 商品页抽检：全部正常（5 个商品）

📦 shop2 (shop2.example.com)
✅ 站点可用性：全部正常（3/3 检查点）
✅ SSL证书：正常（剩余 45 天）
🔍 商品页抽检：全部正常（5 个商品）

🎉 所有店铺健康，无异常。
```

## 告警示例（有问题时）

```
🚨 店铺健康巡检告警 | 2026-03-30 11:00

📦 shop1 (www.example.com)
❌ 站点可用性：
   - /checkout : 超时（>3s）
⚠️  SSL证书：剩余 12 天，请尽快续期
❌ 商品页抽检：
   - /products/12345 : 404

📦 shop2 (shop2.example.com)
✅ 无异常

⚡ 共 3 个问题需要处理
```

## 告警规则

| 检查项 | 告警条件 |
|--------|---------|
| 站点可用性 | HTTP状态码非200，或响应时间超过阈值 |
| SSL证书 | 剩余有效期 < 警告天数（默认14天），或证书无效/自签名 |
| 商品页404 | 被抽检的商品页返回404 |
| 商品页内容 | 页面包含"此商品已下架"、"Page Not Found"、"404"等错误文本 |

## 定时任务配置

```bash
openclaw cron add \
  --name "shop-health-check-hourly" \
  --cron "0 * * * *" \
  --session isolated \
  --message "运行店铺健康巡检：cd ~/.openclaw/skills/shop-health-check && python3 scripts/report.py" \
  --announce \
  --channel feishu
```

## 依赖安装

```bash
pip3 install requests beautifulsoup4 urllib3 python-dateutil
```