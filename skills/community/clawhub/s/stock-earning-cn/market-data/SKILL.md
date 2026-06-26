---
name: market-data
description: 专门用于查询全球股票实时价格、基本信息和搜索股票代码的助手。
metadata: {"openclaw": {"requires": {"env": ["STOCK_API_KEY"]}}}
user-invocable: true
---

# 市场数据助手 (Market Data)

专门用于查询全球股票实时价格、基本信息和搜索股票代码的助手。

## 认证与基础配置
- 环境变量: `STOCK_API_KEY`
- Base URL: 从 `config.sh` 中读取 `$STOCK_BASE_URL`（默认 `https://www.mystockearning.cn`，切换域名只需改 `config.sh`）

## 市场代码 (Market Codes)
- 美股: `us`
- 港股: `hk`
- A股: `cn_a`
- B股: `cn_b`

## API 指令清单

### 搜索股票
当用户说 "查询腾讯的代码" 或 "寻找苹果股票" 时：
- 执行 `./scripts/search_stocks.sh`（需要设置 `QUERY`，可选 `MARKET`）

### 获取实时价格
当用户说 "查看 AAPL 的现价" 时：
- 执行 `./scripts/get_price.sh`（需要设置 `SYMBOL`，可选 `MARKET`）

### 获取股票详情
当用户需要股票的基本面信息时：
- 执行 `./scripts/get_info.sh`（需要设置 `SYMBOL`，可选 `MARKET`）

## 执行规则
1. 解析用户指令。
2. **货币显示规则**：在回复实时价格或任何金额时，必须根据该股票所在的市场显示正确的货币符号或单位：
   - `cn_a` (A股): `¥` 或 `元` (人民币 CNY)
   - `hk` (港股): `HK$` 或 `港元` (港币 HKD)
   - `us` (美股): `$` 或 `美元` (美元 USD)
3. 构造对应的 `curl` 命令并执行。
4. 如果返回 404，告知用户未找到该股票，请检查名称或市场代码。
5. 将 JSON 格式的价格和货币单位转换为易读的自然语言，金额必须带上正确的货币单位。
