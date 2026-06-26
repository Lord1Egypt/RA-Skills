# CLI 命令参考

## 股票形态筛选命令

### 基本语法

```bash
npx daxiapi-cli@latest stock pattern <pattern_type>
```

### 参数说明

| 参数           | 类型   | 必填 | 说明                   |
| -------------- | ------ | ---- | ---------------------- |
| pattern_type   | string | 是   | 形态类型代码           |

### 常用命令示例

#### 价值指标类

```bash
# 获取高股息股票（股息率>3%）
npx daxiapi-cli@latest stock pattern gxl
```

#### 强度指标类

```bash
# 获取 RPS 大于 70 的强势股
npx daxiapi-cli@latest stock pattern rps

# 获取 SCTR 大于 70 的股票
npx daxiapi-cli@latest stock pattern sctr

# 获取 RPS 行业前三
npx daxiapi-cli@latest stock pattern rpsTop3

# 获取 CS 行业前三
npx daxiapi-cli@latest stock pattern csTop3

# 获取 SCTR 行业前三
npx daxiapi-cli@latest stock pattern sctrTop3
```

#### 趋势形态类

```bash
# 获取趋势向上的股票
npx daxiapi-cli@latest stock pattern trendUp

# 获取创新高的股票
npx daxiapi-cli@latest stock pattern newHigh

# 获取创 60 日新高的股票
npx daxiapi-cli@latest stock pattern high_60d

# 获取上穿 MA50 的股票
npx daxiapi-cli@latest stock pattern crossMa50

# 获取上穿箱体的股票
npx daxiapi-cli@latest stock pattern crossoverBox

# 获取 CS 穿过 MA20 的股票
npx daxiapi-cli@latest stock pattern cs_crossover_20
```

#### 成交量形态类

```bash
# 获取放量上涨的股票
npx daxiapi-cli@latest stock pattern fangliang

# 获取放量突破箱体的股票
npx daxiapi-cli@latest stock pattern fangliangtupo
```

#### 涨幅排名类

```bash
# 获取 1 日涨幅行业前三
npx daxiapi-cli@latest stock pattern zdf1dTop3

# 获取 5 日涨幅行业前三
npx daxiapi-cli@latest stock pattern zdf5dTop3

# 获取 10 日涨幅行业前三
npx daxiapi-cli@latest stock pattern zdf10dTop3

# 获取 20 日涨幅行业前三
npx daxiapi-cli@latest stock pattern zdf20dTop3

# 获取行业市值前三
npx daxiapi-cli@latest stock pattern shizhiTop3
```

#### 经典技术形态类

```bash
# 获取 VCP 形态股票（波动收缩形态）
npx daxiapi-cli@latest stock pattern vcp

# 获取跨越小溪形态股票
npx daxiapi-cli@latest stock pattern joc

# 获取强势上涨 SOS 形态股票
npx daxiapi-cli@latest stock pattern sos

# 获取 SOS 后出现高 1 入场点的股票
npx daxiapi-cli@latest stock pattern sos_h1

# 获取 Spring 弹簧形态股票
npx daxiapi-cli@latest stock pattern spring

# 获取 W 底吸收形态股票
npx daxiapi-cli@latest stock pattern w

# 获取 LPS 最后供应点形态股票
npx daxiapi-cli@latest stock pattern lps

# 获取 K 线实体较大的股票
npx daxiapi-cli@latest stock pattern ibs
```

## 配置命令

### 查看当前 Token 配置

```bash
npx daxiapi-cli@latest config get token
```

### 设置 Token

```bash
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI
```

## 输出格式

命令返回 Toon 格式的表格数据，包含以下字段：

| 字段     | 说明                                   |
| -------- | -------------------------------------- |
| 代码     | 股票代码                               |
| 名称     | 股票名称                               |
| 涨幅     | 当日涨跌幅(%)                          |
| 5日涨幅  | 近 5 个交易日涨跌幅(%)                 |
| 10日涨幅 | 近 10 个交易日涨跌幅(%)                |
| 20日涨幅 | 近 20 个交易日涨跌幅(%)                |
| RPS      | 相对价格强度，全市场排名百分比         |
| SCTR     | 个股技术综合排名，值越高技术面越强     |
| CS       | 短期动量，收盘价相对 EMA20 的偏离强度  |
| RSI      | 相对强弱指数                           |
| 概念     | 所属概念标签（逗号分隔）               |
| 板块     | 所属行业板块                           |
| 趋势向上 | 是否处于趋势向上状态（true/false）     |
| 收盘价   | 当日收盘价                             |

## 错误处理

### 不支持的形态类型

```bash
# 错误示例
$ npx daxiapi-cli@latest stock pattern unknown
❌ 参数无效: 不支持的形态类型: unknown
支持的形态: gxl, rps, sctr, trendUp, high_60d, ...

# 正确做法：使用支持的形态代码
$ npx daxiapi-cli@latest stock pattern vcp
```

### Token 未配置

```bash
# 错误示例
$ npx daxiapi-cli@latest stock pattern vcp
❌ 未配置 API Token
请先配置 Token: npx daxiapi-cli@latest config set token YOUR_TOKEN

# 正确做法：先配置 Token
$ npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI
```

## 使用建议

1. **收盘后查询**：数据每日收盘后更新，建议收盘后查询获取最新数据
2. **组合筛选**：可同时查询多个形态，进行交叉验证
3. **结合大盘**：形态有效性受大盘环境影响，建议结合市场温度判断
4. **设置止损**：技术形态存在失效风险，建议设置止损位
