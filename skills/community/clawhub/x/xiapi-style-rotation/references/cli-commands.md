# CLI 命令参考

本文档提供大小盘风格轮动分析相关的 CLI 命令详细说明。

## 主要命令

### 获取大小盘风格数据

```bash
npx daxiapi-cli@latest market style
```

**功能**：获取中证2000（小盘）与沪深300（大盘）的波动差值数据

**参数**：无

**输出格式**：

```json
{
  "date": "2025-01-15",
  "spread": 2.5,
  "csi2000": {
    "code": "1.932000",
    "name": "中证2000",
    "change": 1.2
  },
  "csi300": {
    "code": "1.000300",
    "name": "沪深300",
    "change": -1.3
  },
  "trend": "上升",
  "data": [
    // 最近20日差值数据
    { "date": "2025-01-15", "spread": 2.5 },
    { "date": "2025-01-14", "spread": 2.1 }
    // ...
  ]
}
```

**字段说明**：

| 字段      | 类型   | 说明                           |
| --------- | ------ | ------------------------------ |
| date      | string | 数据日期（YYYY-MM-DD）         |
| spread    | number | 波动差值（中证2000-沪深300）   |
| csi2000   | object | 中证2000指数数据               |
| csi300    | object | 沪深300指数数据                |
| trend     | string | 趋势方向（上升/下降/震荡）     |
| data      | array  | 最近20日差值历史数据           |

**使用示例**：

```bash
# 获取最新风格数据
npx daxiapi-cli@latest market style

# 指定输出格式
npx daxiapi-cli@latest market style --output json

# 保存到文件
npx daxiapi-cli@latest market style > style_report.json
```

## 配置命令

### 检查 Token 配置

```bash
npx daxiapi-cli@latest config get token
```

### 设置 Token

```bash
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI
```

## 常见问题

### Q: 返回空数据怎么办？

A: 可能原因：
1. 非交易日：市场休市，无新数据
2. 数据更新延迟：收盘后稍等片刻再查询
3. Token 无效：检查 Token 配置

### Q: 如何判断风格切换信号？

A: 关注以下情况：
1. 差值接近 ±10% 极端值
2. 趋势出现明显反转
3. 连续多日差值变化方向一致

### Q: 数据更新频率？

A: 数据每个交易日收盘后更新一次，盘中无实时数据。

## 相关命令

```bash
# 查看帮助
npx daxiapi-cli@latest market style --help

# 查看版本
npx daxiapi-cli@latest --version

# 查看所有市场命令
npx daxiapi-cli@latest market --help
```
