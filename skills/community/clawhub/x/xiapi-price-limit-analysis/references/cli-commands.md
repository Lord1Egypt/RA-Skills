# CLI 命令参考

本文档详细介绍涨跌停分析相关的 CLI 命令。

## 基础命令

### 获取涨停股票

```bash
npx daxiapi-cli@latest zdt --type zt
```

**参数说明**：
- `--type zt`：涨停类型（ZhangTing）

**返回字段**：
- `code`：股票代码
- `name`：股票名称
- `zt_days`：涨停天数（连板数）
- `industry`：所属行业
- `concept`：所属概念（数组）
- `cs`：CS强度（Close-to-EMA Strength）
- `sctr`：SCTR排名

---

### 获取跌停股票

```bash
npx daxiapi-cli@latest zdt --type dt
```

**参数说明**：
- `--type dt`：跌停类型（DieTing）

**返回字段**：
- 与涨停股相同结构

---

### 获取炸板股票

```bash
npx daxiapi-cli@latest zdt --type zb
```

**参数说明**：
- `--type zb`：炸板类型（ZhaBan，曾涨停但收盘未封住）

**返回字段**：
- 与涨停股相同结构

---

## 高级用法

### 组合查询

```bash
# 同时获取涨停和跌停数据
npx daxiapi-cli@latest zdt --type zt
npx daxiapi-cli@latest zdt --type dt
```

### 数据筛选建议

**连板股筛选**：
- 关注 `zt_days >= 2` 的股票（连板股）
- 连板数越高，市场关注度越大

**强度筛选**：
- 关注 `cs > 0` 的股票（相对强势）
- `sctr` 排名靠前表示全市场强度较高

---

## 错误处理

| 错误码 | 说明         | 处理方式          |
| ------ | ------------ | ----------------- |
| 401    | 认证失败     | 检查 Token 配置   |
| 404    | API 不存在   | 检查命令拼写      |
| 429    | 请求频率超限 | 等待后重试        |
| 500    | 服务器错误   | 稍后重试          |

### 参数错误

```bash
# 错误示例
npx daxiapi-cli@latest zdt --type invalid
# 输出：参数 'type' 必须是 zt、dt 或 zb
```

---

## 数据时效性

- 数据每日收盘后更新
- 盘中查询可能返回上一交易日数据
- 建议收盘后 15:30 后查询当日完整数据

---

## 相关文档

- [Token 配置指南](token-setup.md)
- [字段说明](field-descriptions.md)
