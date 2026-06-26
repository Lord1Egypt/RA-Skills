# 多平台订单利润计算器

上传**任意电商平台或ERP**的订单导出文件，自动计算每笔订单的净利润，支持 TikTok Shop、Allegro、Temu半托管、Amazon、SHEIN、Fruugo、Shopee、Ozon 等所有主流平台。

## 版本与定价

| 版本 | 价格 | 订单限制 | 店铺限制 | 功能 |
|------|------|:--------:|:--------:|------|
| **免费版** | ¥0 | 20单/月 | 1个 | 基础利润计算 |
| **标准版** | ¥9.9/月 | 500单/月 | 3个 | 全功能 + 报表导出 |
| **专业版** | ¥29/月 | 无限 | 无限 | SKU分析 + 趋势图 |
| **团队版** | ¥99/月 | 无限 | 无限 | 历史记录 + 多用户 |

### 升级专业版

访问 [https://yk-global.com](https://yk-global.com) 购买，获取 API Key 后配置：

```bash
export PROFIT_API_KEY=您的密钥
python3 scripts/parse_orders.py orders.xlsx --api
```

---

## 快速使用

```bash
# 本地直接运行（免费版）— 自动识别任意平台格式
python3 scripts/parse_orders.py orders.xlsx

# 输出JSON格式
python3 scripts/parse_orders.py orders.xlsx --json result.json
```

**支持从以下来源导入：**
- 妙手ERP / 千牛 / 店小秘 等ERP导出
- Allegro / Temu / Amazon / TikTok Shop 等平台后台直接导出
- 任意包含订单编号、收入、成本字段的Excel文件

---

## 支持的平台

| 平台 | 状态 | 备注 |
|------|:----:|------|
| TikTok Shop | ✅ | ERP或平台后台导出 |
| Allegro | ✅ | ERP或平台后台导出 |
| Temu 半托管 | ✅ | ERP或平台后台导出 |
| SHEIN | ✅ | ERP或平台后台导出 |
| Fruugo | ✅ | ERP或平台后台导出 |
| Amazon | ✅ | 平台后台导出 |
| Shopee / Lazada | ✅ | 平台后台导出 |
| Ozon | ✅ | 平台后台导出 |
| Walmart / eBay | ✅ | 平台后台导出 |
| 其他平台 | ✅ | 通用字段自动识别 |

> **字段映射是自动的**，不限制平台。导出文件包含标准订单字段即可。

---

## 计算逻辑

**净利润 = 平台收入 - 平台支出 - 订单成本**

| 模块 | 说明 |
|------|------|
| **平台收入** | 交易收入 + 运费收入 + 退款 + 平台补贴 |
| **平台支出** | 平台佣金 + 技术服务费 + 运费 + 退款 + 违规扣款 + 税费 |
| **订单成本** | 采购成本 + 头程运费 + 尾程运费 + 包材费 + 仓库操作费 + 广告成本 |

---

## 依赖

- Python 3.8+
- openpyxl (`pip install openpyxl`)

---

## 官网与支持

- 官网：[https://yk-global.com](https://yk-global.com)
- 问题反馈：联系客服

---

> 本工具免费版完全免费，无使用期限。付费版提供API托管和增值分析功能。
