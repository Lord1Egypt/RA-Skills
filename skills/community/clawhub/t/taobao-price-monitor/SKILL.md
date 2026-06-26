---
name: taobao-price-monitor
version: 1.0.0
description: 监控淘宝/天猫商品价格，支持历史价格查询、降价提醒、比价功能。适合电商卖家、代购、精明消费者。
homepage: https://github.com/openclaw/skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🛒",
        "requires": { "bins": ["python3", "curl"], "env": ["TAOBAO_COOKIE"] },
        "install":
          [
            {
              "id": "requests",
              "kind": "pip",
              "package": "requests",
              "label": "安装依赖：pip3 install requests",
            },
          ],
      },
  }
---

# 淘宝价格监控技能

监控淘宝/天猫商品价格，支持历史价格查询、降价提醒、跨平台比价。

## 功能

1. **价格查询**: 实时获取商品当前价格
2. **历史价格**: 查看商品历史价格走势
3. **降价提醒**: 设置目标价，降价时通知
4. **比价功能**: 同款商品跨店铺比价
5. **批量监控**: 同时监控多个商品

## 快速开始

### 1. 安装依赖

```bash
pip3 install requests playwright
playwright install
```

### 2. 配置 Cookie（可选，用于突破反爬）

在 `~/.openclaw/openclaw.json` 中添加：

```json5
{
  skills: {
    entries: {
      "taobao-price-monitor": {
        enabled: true,
        env: {
          TAOBAO_COOKIE: "your_cookie_here",
        },
      },
    },
  },
}
```

### 3. 使用方式

**查询单个商品价格**:
```
监控淘宝价格 https://item.taobao.com/item.htm?id=123456789
```

**设置降价提醒**:
```
当这个商品降到 100 元以下时提醒我 https://item.taobao.com/item.htm?id=123456789
```

**批量监控**:
```
监控以下商品的价格：
- https://item.taobao.com/item.htm?id=123
- https://item.taobao.com/item.htm?id=456
- https://item.taobao.com/item.htm?id=789
```

**查看历史价格**:
```
查看这个商品的历史价格走势 https://item.taobao.com/item.htm?id=123456789
```

**比价**:
```
帮我找同款商品的最低价 https://item.taobao.com/item.htm?id=123456789
```

## 工具说明

### 核心工具

| 工具 | 功能 | 调用方式 |
|------|------|---------|
| `query_price.py` | 查询商品价格 | 自动调用 |
| `history_price.py` | 历史价格查询 | 自动调用 |
| `price_alert.py` | 降价提醒设置 | 自动调用 |
| `compare_price.py` | 比价功能 | 自动调用 |

### 输出格式

```json
{
  "item_id": "123456789",
  "title": "商品标题",
  "current_price": 199.00,
  "original_price": 299.00,
  "discount": "6.7 折",
  "sales": "月销 1000+",
  "shop_name": "店铺名称",
  "shop_rating": 4.8,
  "delivery": "包邮",
  "timestamp": "2026-03-24 00:00:00"
}
```

## 注意事项

1. **反爬限制**: 高频访问可能需要 Cookie 或代理
2. **价格准确性**: 促销价格可能实时变化
3. **地区差异**: 部分商品有地区限价
4. **使用频率**: 建议单 IP 每分钟不超过 10 次请求

## 进阶用法

### 定时监控

配置 cron 任务，每小时自动检查：

```json5
{
  cron: {
    jobs: [
      {
        id: "taobao-price-check",
        schedule: { kind: "every", everyMs: 3600000 },
        payload: { 
          kind: "agentTurn", 
          message: "检查监控的淘宝商品价格，有变化时通知我" 
        },
        sessionTarget: "isolated",
      }
    ]
  }
}
```

### 导出数据

```
导出我监控的所有商品价格数据为 Excel
```

### API 调用（高级）

技能支持 HTTP API 调用，适合集成到其他系统：

```bash
curl http://localhost:18789/skills/taobao-price-monitor/query \
  -d '{"item_id": "123456789"}'
```

## 变现模式

### 免费功能
- 每日 10 次价格查询
- 基础历史价格
- 手动比价

### 付费功能（¥99/月）
- 无限次查询
- 实时降价提醒
- 批量监控（100+ 商品）
- 数据导出
- API 访问

### 企业版（¥5000/年）
- 私有部署
- 自定义监控规则
- 数据 API
- 专属支持

## 常见问题

**Q: 为什么有些商品价格获取失败？**
A: 可能是反爬限制，尝试配置 Cookie 或使用代理。

**Q: 历史价格数据准确吗？**
A: 基于公开数据抓取，仅供参考，以实际下单为准。

**Q: 可以监控拼多多/京东吗？**
A: 请安装对应的 `pinduoduo-price-monitor` 和 `jd-price-monitor` 技能。

## 更新日志

- v0.1.0 (2026-03-24): 初始版本，基础价格查询

## 支持

- GitHub: https://github.com/openclaw/skills
- 问题反馈：提交 Issue

---

**声明**: 本技能仅供学习研究使用，请遵守淘宝/天猫平台规则。
