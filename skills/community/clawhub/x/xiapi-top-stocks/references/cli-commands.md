# CLI 命令参考

本文档详细介绍热门股票分析相关的 CLI 命令。

## 核心命令

### sector top - 获取热门股票数据

获取A股热门股票数据，筛选当日涨幅>7%且IBS>50的强势股，按板块分组展示每个板块内强度排名前10的股票。

#### 基本用法

```bash
npx daxiapi-cli@latest sector top
```

#### 命令说明

- **功能**：获取当日热门强势股数据
- **筛选条件**：
    - 当日涨幅 > 7%
    - IBS（Internal Bar Strength，内部K线强度）> 50
- **输出**：按板块分组，每个板块展示强度排名前 10 的股票
- **数据更新**：每日收盘后更新

#### 返回字段

| 字段名  | 类型   | 说明                                          |
| ------- | ------ | --------------------------------------------- |
| name    | string | 股票名称                                      |
| code    | string | 股票代码                                      |
| zdf     | number | 当日涨跌幅（%）                               |
| zdf5    | number | 5日涨跌幅（%）                                |
| zdf10   | number | 10日涨跌幅（%）                               |
| zdf20   | number | 20日涨跌幅（%）                               |
| sector  | string | 所属行业板块，BK开头是东方财富，8开头是同花顺 |
| concept | string | 所属概念（可能有多个）                        |
| cs      | number | CS强度指标                                    |
| ibs     | number | IBS（Internal Bar Strength，内部K线强度）     |

#### 示例输出

```json
{
    "板块A": [
        {
            "name": "某某科技",
            "code": "000001",
            "zdf": 9.85,
            "zdf5": 15.2,
            "zdf10": 22.3,
            "zdf20": 35.6,
            "sector": "电子",
            "concept": "芯片,国产替代",
            "cs": 85.5,
            "ibs": 72.3
        }
    ],
    "板块B": [
        // ...
    ]
}
```

## 辅助命令

### sector gn - 获取热门概念板块

获取A股热门概念板块列表，可配合热门股票分析使用。

```bash
# 使用同花顺数据源（默认）
npx daxiapi-cli@latest sector gn

# 使用东方财富数据源
npx daxiapi-cli@latest sector gn --type dfcf
```

#### 返回字段

| 字段名  | 类型   | 说明                   |
| ------- | ------ | ---------------------- |
| name    | string | 概念板块名称           |
| zdf     | number | 今日涨跌幅（%）        |
| count7p | number | 板块内涨幅7%以上股票数 |
| zdf5    | number | 5日涨跌幅（%）         |
| zdf10   | number | 10日涨跌幅（%）        |
| zdf20   | number | 20日涨跌幅（%）        |
| qd      | number | 强度指标               |
| cs      | number | CS强度                 |

### sector bk - 获取行业板块数据

获取A股行业板块数据，用于分析行业整体热度。

```bash
npx daxiapi-cli@latest sector bk
```

#### 返回字段

| 字段名 | 类型   | 说明            |
| ------ | ------ | --------------- |
| name   | string | 行业板块名称    |
| zdf    | number | 今日涨跌幅（%） |
| zdf5   | number | 5日涨跌幅（%）  |
| zdf20  | number | 20日涨跌幅（%） |
| cs     | number | CS强度指标      |
| csMa   | string | CS均线状态      |
| qd     | number | 强度指标（QD）  |

## 配置命令

### config set - 设置 Token

```bash
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI
```

### config get - 查看当前 Token

```bash
npx daxiapi-cli@latest config get token
```

## 使用场景示例

### 场景1：查看当日热门股票

```bash
npx daxiapi-cli@latest sector top
```

### 场景2：结合热门概念分析

```bash
# 先获取热门股票
npx daxiapi-cli@latest sector top

# 再获取热门概念板块
npx daxiapi-cli@latest sector gn
```

### 场景3：验证数据更新时间

```bash
# 检查行业板块数据（包含更新时间）
npx daxiapi-cli@latest sector bk
```

## 注意事项

1. **数据更新时间**：热门股票数据每日收盘后更新，盘中数据可能不完整
2. **筛选条件**：默认筛选涨幅>7%且IBS>50的股票，这是短线强势股的典型特征
3. **板块分组**：数据按板块分组，便于识别热点板块
4. **概念字段**：一只股票可能属于多个概念，用逗号分隔

## 错误处理

### 401 Unauthorized

```
错误：未配置 API Token
```

**解决方案**：先配置 Token

```bash
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI
```

### 429 Too Many Requests

```
错误：请求频率超限
```

**解决方案**：等待 30-60 秒后重试

### 空数据返回

```
返回：[] 或 {}
```

**可能原因**：

- 非交易日
- 当日无符合条件的股票（市场冷清）
- 数据尚未更新

**解决方案**：向用户说明情况，建议稍后重试或结合其他数据分析
