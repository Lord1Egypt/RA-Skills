# 字段列表

本文档列出大虾皮 SQL 股票筛选器支持的所有查询字段。

## 日期字段

| 字段名 | 类型 | 说明 | 示例 |
| ------ | ---- | ---- | ---- |
| `date` | String | 查询日期（必填） | `date='2026-06-17'` |

**注意**：

- `date` 字段为必填条件
- 只支持查询最近 10 天内的数据
- 格式：YYYY-MM-DD

## 基本信息

| 字段名 | 类型 | 说明 | 示例 |
| ------ | ---- | ---- | ---- |
| `stockId` | String | 股票代码 | `stockId='000001'` |
| `name` | String | 股票名称 | `name='平安银行'` |

## 涨跌幅指标

| 字段名 | 类型 | 说明 | 示例 |
| ------ | ---- | ---- | ---- |
| `zdf` | Number | 当日涨跌幅（%） | `zdf>3` |
| `zdf_5d` | Number | 5日涨跌幅（%） | `zdf_5d>10` |
| `zdf_10d` | Number | 10日涨跌幅（%） | `zdf_10d>15` |
| `zdf_20d` | Number | 20日涨跌幅（%） | `zdf_20d>20` |

## 强度指标

| 字段名 | 类型 | 说明 | 示例 |
| ------ | ---- | ---- | ---- |
| `cs` | Number | CS强度值 | `cs>0` |
| `rps_score` | Number | RPS相对强度（0-100） | `rps_score>70` |
| `sctr` | Number | SCTR技术排名（0-100） | `sctr>60` |
| `sm` | Number | SM强度 | `sm>5` |
| `ml` | Number | ML强度 | `ml>3` |

**强度指标说明**：

- **CS（强度值）**：股票相对强度的核心指标，正值表示强势，负值表示弱势
- **RPS（相对强度）**：欧奈尔 RPS 指标，0-100 分，70 以上为强势股
- **SCTR（技术排名）**：技术综合排名，0-100 分，60 以上为技术强势股
- **SM（强度）**：短期强度指标
- **ML（强度）**：中期强度指标

## 技术形态

| 字段名 | 类型 | 说明 | 示例 |
| ------ | ---- | ---- | ---- |
| `isVCP` | Number | 是否VCP形态（0/1） | `isVCP=1` |
| `isSOS` | Number | 是否SOS形态（0/1） | `isSOS=1` |
| `isSpring` | Number | 是否Spring形态（0/1） | `isSpring=1` |
| `isNewHigh` | Number | 是否新高（0/1） | `isNewHigh=1` |
| `isHigh_60d` | Number | 是否60日新高（0/1） | `isHigh_60d=1` |

**技术形态说明**：

- **VCP（波动收缩形态）**：股魔 Mark Minervini 的经典形态
- **SOS（强势上涨）**：威科夫强势上涨信号
- **Spring（弹簧形态）**：威科夫弹簧形态
- **isNewHigh**：是否创近期新高
- **isHigh_60d**：是否创60日新高

## 价格指标

| 字段名 | 类型 | 说明 | 示例 |
| ------ | ---- | ---- | ---- |
| `close` | Number | 收盘价 | `close>10` |
| `open` | Number | 开盘价 | `open>9` |
| `high` | Number | 最高价 | `high>11` |
| `low` | Number | 最低价 | `low<9` |

## 成交量指标

| 字段名 | 类型 | 说明 | 示例 |
| ------ | ---- | ---- | ---- |
| `vol` | Number | 成交量（手） | `vol>100000` |
| `amount` | Number | 成交额（万元） | `amount>1000` |

## 市值指标

| 字段名 | 类型 | 说明 | 示例 |
| ------ | ---- | ---- | ---- |
| `shizhi` | Number | 总市值（亿元） | `shizhi>100` |

## 其他指标

| 字段名 | 类型 | 说明 | 示例 |
| ------ | ---- | ---- | ---- |
| `rsi` | Number | RSI指标 | `rsi>70` |
| `ibs` | Number | IBS强度（K线实体占比） | `ibs>69` |

## 字段类型说明

### String 类型字段

- 需要用单引号或双引号包围
- 示例：`date='2026-06-17'`、`stockId='000001'`

### Number 类型字段

- 不需要引号
- 支持比较运算符（>、<、>=、<=、=、!=）
- 支持区间运算符（`in [...]`）
- 示例：`rps_score>70`、`cs in [0, 15]`

## 常用字段组合

### 强势股筛选

```sql
date='2026-06-17' AND rps_score>70 AND sctr>60 AND cs>0
```

### 技术形态筛选

```sql
date='2026-06-17' AND isVCP=1 AND rps_score>70
```

### 涨幅筛选

```sql
date='2026-06-17' AND zdf>3 AND zdf_5d>10
```

### 市值筛选

```sql
date='2026-06-17' AND shizhi>100 AND rps_score>70
```

### 板块筛选

```sql
date='2026-06-17' AND bkName='银行' AND rps_score>70
```

## 字段优先级建议

在构建查询条件时，建议按以下优先级选择字段：

1. **必填字段**：`date`
2. **核心强度指标**：`rps_score`、`sctr`、`cs`
3. **技术形态**：`isVCP`、`isSOS`、`isSpring`
4. **涨跌幅**：`zdf`、`zdf_5d`、`zdf_10d`
5. **市值**：`shizhi`
6. **板块**：`bkName`

## 参考文档

- [SQL 语法说明](sql-syntax.md)：查看 SQL 语法详细说明
- [常用查询示例](query-examples.md)：查看更多查询示例
