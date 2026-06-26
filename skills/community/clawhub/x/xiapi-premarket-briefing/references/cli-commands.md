# CLI 命令参考

本文档列出了盘前简报 Skill 使用的主要 CLI 命令。

## 市场温度

获取市场四大温度指标。

```bash
npx daxiapi-cli@latest market temp
```

**返回字段**：

| 字段       | 说明               | 取值范围  |
| ---------- | ------------------ | --------- |
| date       | 数据日期           | YYYY-MM-DD |
| pe         | 估值温度           | 0-100     |
| fear_greed | 恐贪指数           | 0-100     |
| trend      | 趋势温度           | 0-100     |
| momentum   | 动量温度           | 0-100     |

**更新时间**：交易日晚8点后更新

**使用场景**：
- 判断市场整体冷热程度
- 识别极端情绪
- 中长期趋势判断

---

## 板块热力图

获取板块强弱排名。

```bash
npx daxiapi-cli@latest sector heatmap
```

**返回字段**：

| 字段    | 说明           | 备注       |
| ------- | -------------- | ---------- |
| name    | 板块名称       | -          |
| qd      | 板块强度       | 0-100      |
| zdf     | 当日涨跌幅     | %          |
| zdf5    | 5日涨跌幅      | %          |
| zdf10   | 10日涨跌幅     | %          |
| zdf20   | 20日涨跌幅     | %          |

**更新时间**：交易日收盘后更新

**使用场景**：
- 识别强势板块
- 分析板块轮动
- 选择投资方向

---

## 涨跌停分析

获取市场涨跌停数据。

```bash
npx daxiapi-cli@latest price-limit
```

**返回字段**：

| 字段         | 说明           | 备注       |
| ------------ | -------------- | ---------- |
| up_count     | 涨停数量       | -          |
| down_count   | 跌停数量       | -          |
| up_2b_count  | 2连板数量      | -          |
| up_3b_count  | 3连板数量      | -          |
| up_ab_count  | 涨停开板数量   | -          |

**更新时间**：交易日收盘后更新

**使用场景**：
- 判断市场活跃度
- 识别题材持续性
- 市场情绪分析

---

## 市场指数

获取市场指数和北向资金数据。

```bash
npx daxiapi-cli@latest market index
```

**返回字段**：

| 字段           | 说明             | 备注       |
| -------------- | ---------------- | ---------- |
| north_net      | 北向净流入       | 亿元       |
| north_sh       | 沪股通净流入     | 亿元       |
| north_sz       | 深股通净流入     | 亿元       |
| up_count       | 上涨家数         | -          |
| down_count     | 下跌家数         | -          |
| limit_up       | 涨停数           | -          |
| limit_down     | 跌停数           | -          |

**更新时间**：交易日收盘后更新

**使用场景**：
- 北向资金流向分析
- 市场宽度判断
- 外资态度分析

---

## 常用命令组合

### 快速市场扫描

```bash
# 获取市场温度
npx daxiapi-cli@latest market temp

# 获取板块热力图
npx daxiapi-cli@latest sector heatmap

# 获取涨跌停数据
npx daxiapi-cli@latest price-limit

# 获取北向资金
npx daxiapi-cli@latest market index
```

### 板块深度分析

```bash
# 获取板块热力图
npx daxiapi-cli@latest sector heatmap

# 获取特定板块详情
npx daxiapi-cli@latest sector detail -n <板块名称>
```

---

## 错误处理

### 401 认证失败

```bash
# 检查 Token 配置
npx daxiapi-cli@latest config get token

# 重新配置 Token
npx daxiapi-cli@latest config set token YOUR_TOKEN
```

### 429 请求超限

等待 30-60 秒后重试。

### 空数据返回

可能是非交易日或数据更新延迟，建议交易日收盘后重试。

---

## 注意事项

1. **数据时效性**：部分数据在交易日晚8点后更新
2. **非交易日**：非交易日数据可能为空或过期
3. **频率限制**：避免短时间内频繁调用
4. **Token 有效期**：Token 可能过期，需要定期更新
