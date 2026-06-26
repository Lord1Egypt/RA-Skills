# 记账数据格式参考

## categories.json - 消费分类定义

```json
{
  "categories": [
    {"name": "餐饮", "icon": "🍜", "description": "三餐、外卖、零食、饮料、咖啡等"},
    {"name": "交通", "icon": "🚗", "description": "打车、公交、地铁、加油、停车、共享单车"},
    {"name": "购物", "icon": "🛒", "description": "日用品、数码产品、服饰、网购等"},
    {"name": "居住", "icon": "🏠", "description": "房租、房贷、水电燃气、物业、维修"},
    {"name": "娱乐", "icon": "🎮", "description": "电影、KTV、游戏、旅游、景点门票"},
    {"name": "医疗", "icon": "💊", "description": "挂号、药品、体检、治疗"},
    {"name": "通讯", "icon": "📱", "description": "话费、流量、宽带"},
    {"name": "服饰", "icon": "👗", "description": "衣服、鞋帽、饰品、箱包"},
    {"name": "教育", "icon": "📚", "description": "培训、书籍、文具、课程"},
    {"name": "其他", "icon": "📦", "description": "未归类的其他消费"}
  ]
}
```

## expenses/expenses-YYYYMM.json - 月度消费记录

```json
{
  "expenses": [
    {
      "id": "2026-06-01-001",
      "date": "2026-06-01",
      "time": "11:32:06",
      "amount": 25.00,
      "currency": "CNY",
      "merchant": "全国工商联机关服务中心（北京仁合兴餐饮）",
      "category": "餐饮",
      "payment_method": "中信银行信用卡(0814)",
      "notes": "午餐",
      "source": "微信支付截图"
    }
  ],
  "last_updated": "2026/6/6 21:03:52",
  "monthly_summaries": {}
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识，格式 `YYYY-MM-DD-NNN`，NNN 为当天 3 位序号 |
| date | string | 是 | 消费日期，格式 `YYYY-MM-DD` |
| time | string | 否 | 消费时间，格式 `HH:MM:SS` |
| amount | number | 是 | 消费金额 |
| currency | string | 否 | 货币，默认 `CNY` |
| merchant | string | 是 | 商家名称 |
| category | string | 是 | 消费分类，必须存在于 `categories.json` |
| payment_method | string | 否 | 支付方式，如"微信支付"、"支付宝"、"中信银行信用卡(0814)" |
| notes | string | 否 | 备注 |
| source | string | 否 | 数据来源，如"微信支付截图"、"支付宝截图"、"手动输入" |

### ID 生成规则

- 格式：`YYYY-MM-DD-NNN`
- NNN 从 001 开始，同一日期内依次递增
- 新增记录时读取当月文件，找到当天最大序号 +1

### monthly_summaries 格式

```json
{
  "monthly_summaries": {
    "202606": {
      "generated_at": "2026-06-30 20:05:00",
      "total_amount": 3520.50,
      "total_count": 45,
      "avg_daily": 117.35,
      "max_single": {"amount": 500.00, "merchant": "京东", "date": "2026-06-15"},
      "category_breakdown": {
        "餐饮": {"amount": 1200.00, "count": 25, "percentage": 34.1},
        "交通": {"amount": 300.50, "count": 8, "percentage": 8.5},
        "购物": {"amount": 1500.00, "count": 5, "percentage": 42.6},
        "居住": {"amount": 400.00, "count": 2, "percentage": 11.4},
        "娱乐": {"amount": 120.00, "count": 5, "percentage": 3.4}
      },
      "payment_breakdown": {
        "微信支付": {"amount": 2000.00, "count": 30},
        "支付宝": {"amount": 1520.50, "count": 15}
      }
    }
  }
}
```

## 自动化排程

建议在 OpenCLAW 中设置自动化任务 `expense-monthly-report`：

- **触发时间**：每月最后一天 20:00
- **执行指令**：`生成本月消费报告`
- **rrule**：`FREQ=MONTHLY;BYMONTHDAY=-1;BYHOUR=20;BYMINUTE=0`


建议在 OpenCLAW 中设置自动化任务 `expense-daily_reminder`：

- **触发时间**：每天 20:00
- **执行指令**：`记账提醒`
- **rrule**：`FREQ=DAILY;BYHOUR=20;BYMINUTE=0`