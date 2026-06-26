# API 参考文档

## 类: SinopecOilPriceSkill

中石化油价查询技能的主类。

### 构造函数

```javascript
const skill = new SinopecOilPriceSkill();
```

### 方法

#### getOilPrice(params)

获取指定省份的油价信息。

**参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| province_id | string | 否 | 省份ID，与 province_name 二选一 |
| province_name | string | 否 | 省份名称（如"北京"、"广西"） |

**返回:**

```javascript
{
  success: true,
  date: '2026-03-26',
  province: '广西',
  areaDesc: '广西',
  prices: [
    {
      area: '广西',
      gas_92: { price: 8.62, change: 0 },
      gas_95: { price: 9.31, change: 0 },
      gas_98: { price: 10.59, change: 0 },
      diesel_0: { price: 8.31, change: 0 },
      // ...
    }
  ]
}
```

**示例:**

```javascript
// 按省份名称查询
const result = await skill.getOilPrice({ province_name: '广西' });

// 按省份ID查询
const result = await skill.getOilPrice({ province_id: '17' });
```

#### monitorOilPrice(params)

监控油价变化，对比历史数据。

**参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| province_name | string | 是 | 省份名称 |
| recipient_id | string | 否 | 接收通知的用户open_id |

**返回:**

```javascript
{
  success: true,
  message: '⛽ 广西油价日报（2026-03-26）\n\n92号汽油: 8.62元/升 (+0)\n...',
  hasChanges: false,
  changes: [],
  province: '广西',
  date: '2026-03-26'
}
```

---

## 支持的省份

| 省份 | 省份ID |
|------|--------|
| 北京 | 1 |
| 上海 | 2 |
| 天津 | 3 |
| 重庆 | 4 |
| 广东 | 5 |
| 四川 | 6 |
| 贵州 | 7 |
| 云南 | 8 |
| 陕西 | 9 |
| 甘肃 | 10 |
| 青海 | 11 |
| 内蒙古 | 12 |
| 广西 | 17 |
| 西藏 | 19 |
| 宁夏 | 20 |
| 新疆 | 21 |
| 河北 | 22 |
| 山西 | 23 |
| 吉林 | 24 |
| 辽宁 | 25 |
| 黑龙江 | 26 |
| 江苏 | 27 |
| 浙江 | 28 |
| 安徽 | 29 |
| 福建 | 30 |
| 江西 | 31 |
| 山东 | 32 |
| 河南 | 33 |
| 湖北 | 34 |
| 湖南 | 35 |
| 海南 | 36 |

---

## 油价数据类型

| 字段 | 类型 | 说明 |
|------|------|------|
| gas_92 | object | 92号汽油 { price, change } |
| gas_95 | object | 95号汽油 |
| gas_98 | object | 98号汽油 |
| gas_89 | object | 89号汽油 |
| e92 | object | E92乙醇汽油 |
| e95 | object | E95乙醇汽油 |
| e98 | object | E98乙醇汽油 |
| aipao_98 | object | 爱跑98 |
| aipao_95 | object | 爱跑95 |
| diesel_0 | object | 0号柴油 |
| diesel_10 | object | -10号柴油 |
| diesel_20 | object | -20号柴油 |
| diesel_35 | object | -35号柴油 |

price: 价格（元/升）
change: 相比上次的涨跌
