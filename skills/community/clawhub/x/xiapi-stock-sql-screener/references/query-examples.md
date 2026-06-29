# 常用查询示例

本文档提供大虾皮 SQL 股票筛选器的常用查询示例，帮助用户快速构建筛选条件。

## 基础查询

### 查询指定日期的股票

```bash
daxiapi sql "date='2026-06-17' LIMIT 10"
```

查询 2026-06-17 日期的股票，最多返回 10 条。

### 查询指定股票

```bash
daxiapi sql "date='2026-06-17' AND stockId='000001'"
```

查询平安银行（000001）在 2026-06-17 的数据。

## 强势股筛选

### RPS 强势股

```bash
daxiapi sql "date='2026-06-17' AND rps_score>70 ORDER BY rps_score DESC LIMIT 20"
```

查询 RPS>70 的强势股，按 RPS 降序排序，最多返回 20 条。

### SCTR 技术强势股

```bash
daxiapi sql "date='2026-06-17' AND sctr>60 ORDER BY sctr DESC LIMIT 20"
```

查询 SCTR>60 的技术强势股，按 SCTR 降序排序。

### CS 强度股

```bash
daxiapi sql "date='2026-06-17' AND cs>0 ORDER BY cs DESC LIMIT 20"
```

查询 CS>0 的强度股，按 CS 降序排序。

## 趋势+距离52周高点回调20天以上
```bash
daxiapi sql "date='2026-06-17' AND close > ma150
            AND ma150 > ma200
            AND ma50 > ma150
            AND ma50 > ma200
            AND isMA200Up1M = 1
            AND close > ma50
            AND high_52w_days>20 ORDER BY sctr DESC LIMIT 20"
```

### 多强度指标组合

```bash
daxiapi sql "date='2026-06-17' AND rps_score>70 AND sctr>60 AND cs>0 ORDER BY rps_score DESC LIMIT 15"
```

查询 RPS>70、SCTR>60、CS>0 的强势股，按 RPS 降序排序。

## 技术形态筛选

### VCP 形态股

```bash
daxiapi sql "date='2026-06-17' AND isVCP=1 ORDER BY rps_score DESC LIMIT 20"
```

查询 VCP 形态股，按 RPS 降序排序。

### SOS 形态股

```bash
daxiapi sql "date='2026-06-17' AND isSOS=1 ORDER BY sctr DESC LIMIT 20"
```

查询 SOS 形态股，按 SCTR 降序排序。

### Spring 形态股

```bash
daxiapi sql "date='2026-06-17' AND isSpring=1 ORDER BY cs DESC LIMIT 20"
```

查询 Spring 形态股，按 CS 降序排序。

### 多形态组合

```bash
daxiapi sql "date='2026-06-17' AND (isVCP=1 OR isSOS=1) AND rps_score>70 ORDER BY rps_score DESC LIMIT 20"
```

查询 VCP 或 SOS 形态，且 RPS>70 的股票。

### 形态+强度组合

```bash
daxiapi sql "date='2026-06-17' AND isVCP=1 AND rps_score>70 AND sctr>60 ORDER BY rps_score DESC LIMIT 10"
```

查询 VCP 形态，且 RPS>70、SCTR>60 的强势股。

## 涨跌幅筛选

### 当日涨幅股

```bash
daxiapi sql "date='2026-06-17' AND zdf>3 ORDER BY zdf DESC LIMIT 20"
```

查询当日涨幅>3%的股票，按涨幅降序排序。

### 5日涨幅股

```bash
daxiapi sql "date='2026-06-17' AND zdf_5d>10 ORDER BY zdf_5d DESC LIMIT 20"
```

查询5日涨幅>10%的股票，按5日涨幅降序排序。

### 10日涨幅股

```bash
daxiapi sql "date='2026-06-17' AND zdf_10d>15 ORDER BY zdf_10d DESC LIMIT 20"
```

查询10日涨幅>15%的股票，按10日涨幅降序排序。

### 多涨幅组合

```bash
daxiapi sql "date='2026-06-17' AND zdf>3 AND zdf_5d>10 AND zdf_10d>15 ORDER BY zdf DESC LIMIT 15"
```

查询当日涨幅>3%、5日涨幅>10%、10日涨幅>15%的股票。

## 区间范围查询

### CS 区间筛选

```bash
daxiapi sql "date='2026-06-17' AND cs in [0, 15] ORDER BY cs DESC LIMIT 20"
```

查询 CS 在 0-15 之间的股票，按 CS 降序排序。

### RPS 区间筛选

```bash
daxiapi sql "date='2026-06-17' AND rps_score in [70, 90] ORDER BY rps_score DESC LIMIT 20"
```

查询 RPS 在 70-90 之间的股票，按 RPS 降序排序。

### 涨跌幅区间

```bash
daxiapi sql "date='2026-06-17' AND zdf in [3, 10] ORDER BY zdf DESC LIMIT 20"
```

查询涨幅在 3%-10% 之间的股票。

## 市值筛选

### 大市值股

```bash
daxiapi sql "date='2026-06-17' AND shizhi>100 AND rps_score>70 ORDER BY shizhi DESC LIMIT 20"
```

查询市值>100亿且 RPS>70 的股票，按市值降序排序。

### 中市值股

```bash
daxiapi sql "date='2026-06-17' AND shizhi in [50, 100] AND rps_score>70 ORDER BY rps_score DESC LIMIT 20"
```

查询市值在 50-100亿之间且 RPS>70 的股票。

## 板块筛选

### 指定板块

```bash
daxiapi sql "date='2026-06-17' AND bkName='银行' AND rps_score>70 ORDER BY rps_score DESC LIMIT 20"
```

查询银行板块且 RPS>70 的股票。

### 板块+形态组合

```bash
daxiapi sql "date='2026-06-17' AND bkName='银行' AND isVCP=1 ORDER BY rps_score DESC LIMIT 10"
```

查询银行板块的 VCP 形态股。

## 复杂组合查询

### 强势股综合筛选

```bash
daxiapi sql "date='2026-06-17' AND rps_score>70 AND sctr>60 AND cs>0 AND zdf>3 AND shizhi>50 ORDER BY rps_score DESC LIMIT 20"
```

查询 RPS>70、SCTR>60、CS>0、涨幅>3%、市值>50亿的强势股。

### 形态+涨幅+市值组合

```bash
daxiapi sql "date='2026-06-17' AND isVCP=1 AND zdf_5d>10 AND shizhi>100 ORDER BY rps_score DESC LIMIT 15"
```

查询 VCP 形态、5日涨幅>10%、市值>100亿的股票。

### 多条件逻辑组合

```bash
daxiapi sql "date='2026-06-17' AND (isVCP=1 OR isSOS=1) AND (rps_score>70 OR sctr>60) AND cs>0 ORDER BY rps_score DESC LIMIT 20"
```

查询 VCP 或 SOS 形态，且 RPS>70 或 SCTR>60，且 CS>0 的股票。

## 字段间比较

### RPS 大于 SCTR

```bash
daxiapi sql "date='2026-06-17' AND rps_score>sctr AND cs>0 ORDER BY rps_score DESC LIMIT 20"
```

查询 RPS 大于 SCTR 且 CS>0 的股票。

### CS 大于 RPS

```bash
daxiapi sql "date='2026-06-17' AND cs>rps_score AND sctr>60 ORDER BY cs DESC LIMIT 20"
```

查询 CS 大于 RPS 且 SCTR>60 的股票。

## 排序示例

### 单字段排序

```bash
daxiapi sql "date='2026-06-17' AND rps_score>70 ORDER BY rps_score DESC LIMIT 20"
```

按 RPS 降序排序。

### 多字段排序

```bash
daxiapi sql "date='2026-06-17' AND rps_score>70 ORDER BY rps_score DESC, sctr DESC LIMIT 20"
```

先按 RPS 降序，RPS 相同的按 SCTR 降序。

### 涨幅+强度排序

```bash
daxiapi sql "date='2026-06-17' AND rps_score>70 ORDER BY zdf DESC, rps_score DESC LIMIT 20"
```

先按涨幅降序，涨幅相同的按 RPS 降序。

## 实战场景示例

### 寻找突破形态

```bash
daxiapi sql "date='2026-06-17' AND isVCP=1 AND zdf>3 AND vol>100000 ORDER BY rps_score DESC LIMIT 10"
```

查询 VCP 形态、涨幅>3%、成交量>10万手的突破股。

### 寻找强势板块龙头

```bash
daxiapi sql "date='2026-06-17' AND bkName='银行' AND rps_score>80 AND shizhi>100 ORDER BY rps_score DESC LIMIT 5"
```

查询银行板块的市值>100亿、RPS>80 的龙头股。

### 寻找动量股

```bash
daxiapi sql "date='2026-06-17' AND zdf_5d>10 AND zdf_10d>15 AND rps_score>70 ORDER BY zdf_10d DESC LIMIT 20"
```

查询5日涨幅>10%、10日涨幅>15%、RPS>70 的动量股。

### 寻找价值股

```bash
daxiapi sql "date='2026-06-17' AND shizhi>100 AND rps_score>60 AND zdf<5 ORDER BY shizhi DESC LIMIT 20"
```

查询市值>100亿、RPS>60、涨幅<5%的价值股。

## CLI 命令格式

所有示例都可以通过 CLI 命令执行：

```bash
daxiapi sql "<SQL 条件>"
```

**示例**：

```bash
daxiapi sql "date='2026-06-17' AND rps_score>70 ORDER BY rps_score DESC LIMIT 20"
```

## 参考文档

- [SQL 语法说明](sql-syntax.md)：查看 SQL 语法详细说明
- [字段列表](field-list.md)：查看所有支持的查询字段
