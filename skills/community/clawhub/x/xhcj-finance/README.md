# Xinhua Finance Skill

## 技能描述

Xinhua Finance Skill 是一个用于查询新华财经行情及资讯的工具，通过简单的命令行操作获取实时市场数据、K线数据、股票代码查询以及财经资讯。

## 功能特性

1. **市场数据查询**：获取指定股票的实时行情数据
2. **K线数据查询**：获取指定股票的K线数据
3. **股票代码查询**：通过股票名称或代码模糊查询股票信息
4. **财经资讯查询**：获取不同分类的财经新闻，支持关键词搜索

## 安装与配置

### 安装依赖
```bash
npm install
```

### 链接CLI工具
```bash
npm link
```

## 使用方法

### 查询市场数据
```bash
xhcj-finance --api-key <api-key> market --symbol <symbol>
```

**参数说明**：
- `--api-key`：API密钥，格式为 `xhcj_` 开头的32位十六进制字符串
- `--symbol`：A股股票代码，如000001.SZ

### 查询K线数据
```bash
xhcj-finance --api-key <api-key> kline --symbol <symbol>
```

**参数说明**：
- `--api-key`：API密钥，格式为 `xhcj_` 开头的32位十六进制字符串
- `--symbol`：A股股票代码，如000001.SZ

### 查询股票代码
```bash
xhcj-finance --api-key <api-key> symbol --name <name>
```

**参数说明**：
- `--api-key`：API密钥，格式为 `xhcj_` 开头的32位十六进制字符串
- `--name`：股票名称模糊查询，如"中国平安"，也可以是股票代码如"601318"

### 查询财经资讯
```bash
xhcj-finance --api-key <api-key> news [--category <category>] [--limit <number>]
```

**参数说明**：
- `--api-key`：API密钥，格式为 `xhcj_` 开头的32位十六进制字符串
- `--category`：新闻资讯分类：1-股票 2-商品期货 3-外汇 4-债券 5-宏观 9-全部, default 9
- `--limit`：限制结果数量，默认10, max 20

## 示例

1. **查询股票实时行情**：
   ```bash
   xhcj-finance --api-key "xhcj_1234567890abcdef1234567890abcdef" market --symbol 600000.SS
   ```

2. **查询股票K线数据**：
   ```bash
   xhcj-finance --api-key "xhcj_1234567890abcdef1234567890abcdef" kline --symbol 600000.SS
   ```

3. **查询股票代码**：
   ```bash
   xhcj-finance --api-key "xhcj_1234567890abcdef1234567890abcdef" symbol --name "中国平安"
   ```

4. **获取财经新闻**：
   ```bash
   xhcj-finance --api-key "xhcj_1234567890abcdef1234567890abcdef" news --category 1 --limit 5
   ```

## 注意事项

- 请确保在每次执行命令时正确提供 `--api-key` 参数
- API密钥格式应为 `xhcj_` 开头的32位十六进制字符串
- 所有API请求都会进行安全处理，避免API密钥泄露
- 如遇到网络问题，请检查网络连接和API密钥是否正确