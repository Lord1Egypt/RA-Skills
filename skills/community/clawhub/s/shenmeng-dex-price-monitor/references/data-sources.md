# 价格数据源指南

## 数据源分类

### 1. 链上数据源（最准确）

#### The Graph

**优势**：
- 直接从链上索引数据
- 实时性高
- 免费使用

**Uniswap V3子图**：
```graphql
query GetPoolPrice($poolAddress: ID!) {
  pool(id: $poolAddress) {
    id
    token0 {
      symbol
      decimals
    }
    token1 {
      symbol
      decimals
    }
    token0Price
    token1Price
    sqrtPriceX96
    liquidity
    volumeUSD
    feesUSD
  }
}
```

**常用子图地址**：
```
Uniswap V3: https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3
SushiSwap: https://api.thegraph.com/subgraphs/name/sushiswap/exchange
Curve: https://api.thegraph.com/subgraphs/name/curvefi/curve
Balancer: https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2
```

**Python调用**：
```python
import requests

def query_thegraph(subgraph_url, query, variables=None):
    response = requests.post(
        subgraph_url,
        json={'query': query, 'variables': variables or {}},
        headers={'Content-Type': 'application/json'}
    )
    return response.json()

# 示例：获取ETH/USDC价格
query = """
{
  pools(where: {token0_: {symbol: "ETH"}, token1_: {symbol: "USDC"}}, first: 5) {
    id
    token0Price
    feeTier
  }
}
"""

result = query_thegraph(
    'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
    query
)
```

#### 直接合约调用

**优势**：
- 最实时
- 无需第三方
- 100%准确

**Uniswap V3 slot0**：
```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))

# Uniswap V3 Pool ABI (简化)
pool_abi = [
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
            {"internalType": "int24", "name": "tick", "type": "int24"},
            {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
            {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
            {"internalType": "bool", "name": "unlocked", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# ETH/USDC 0.3%池子
pool_address = '0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8'
pool = w3.eth.contract(address=pool_address, abi=pool_abi)

sqrtPriceX96, *_ = pool.functions.slot0().call()

# 计算价格
price = (sqrtPriceX96 ** 2) / (2 ** 192)
print(f"ETH/USDC价格: {price}")
```

### 2. DEX聚合器API

#### 1inch API

**特点**：
- 多DEX聚合价格
- 最优路径计算
- 免费额度充足

**基础用法**：
```python
import requests

def get_1inch_price(chain_id, from_token, to_token, amount):
    url = f"https://api.1inch.dev/swap/v5.2/{chain_id}/quote"
    params = {
        'src': from_token,
        'dst': to_token,
        'amount': amount
    }
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY'
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

# 获取ETH价格
result = get_1inch_price(
    1,  # 以太坊
    '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',  # ETH
    '0xA0b86a33E6441E6C7D3D4B4f6B7A2c8D5e9F0123',  # USDC
    '1000000000000000000'  # 1 ETH
)
```

#### 0x API

**特点**：
- 专业做市商报价
- 深度好
- 免费使用

```python
def get_0x_price(buy_token, sell_token, sell_amount):
    url = "https://api.0x.org/swap/v1/price"
    params = {
        'buyToken': buy_token,
        'sellToken': sell_token,
        'sellAmount': sell_amount
    }
    response = requests.get(url, params=params)
    return response.json()

result = get_0x_price('ETH', 'USDC', '1000000000000000000')
price = 1 / float(result['price'])
```

### 3. 价格聚合器

#### CoinGecko

**特点**：
- 免费版足够用
- 历史数据丰富
- 多链支持

**API端点**：
```
简单价格: /simple/price
代币列表: /coins/list
历史数据: /coins/{id}/market_chart
```

```python
def get_coingecko_price(token_ids):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(token_ids),
        'vs_currencies': 'usd',
        'include_24hr_vol': 'true',
        'include_24hr_change': 'true'
    }
    response = requests.get(url, params=params)
    return response.json()

prices = get_coingecko_price(['ethereum', 'bitcoin', 'chainlink'])
```

**限制**：
- 免费版 10-30 calls/minute
- 需要 attribution

#### CoinMarketCap

**特点**：
- 专业数据
- 实时性高
- 需要API key

```python
def get_cmc_price(symbol):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        'X-CMC_PRO_API_KEY': 'YOUR_API_KEY'
    }
    params = {'symbol': symbol}
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

### 4. WebSocket实时数据

#### The Graph WebSocket

```javascript
const ws = new WebSocket('wss://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3');

ws.onopen = () => {
    ws.send(JSON.stringify({
        type: 'start',
        id: '1',
        payload: {
            query: `
                subscription {
                    pools(first: 5) {
                        token0Price
                        token1Price
                    }
                }
            `
        }
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Price update:', data);
};
```

#### Web3 WebSocket

```python
from web3 import Web3

# WebSocket连接
w3 = Web3(Web3.WebsocketProvider('wss://eth-mainnet.g.alchemy.com/v2/YOUR_KEY'))

# 监听Swap事件
pool_address = '0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8'

swap_event_signature = w3.keccak(text='Swap(address,address,int256,int256,uint160,uint128,int24)').hex()

filter_params = {
    'address': pool_address,
    'topics': [swap_event_signature]
}

def handle_event(event):
    print(f"New swap: {event}")

# 创建过滤器
filter = w3.eth.filter(filter_params)

# 轮询
while True:
    for event in filter.get_new_entries():
        handle_event(event)
```

## 数据源选择建议

### 高频监控（实时套利）

```
推荐: Web3直接合约调用
原因: 
- 无延迟
- 100%准确
- 无API限制

成本: 
- 需要节点（Infura/Alchemy免费版足够）
- 读取不消耗Gas
```

### 中频监控（5-30秒）

```
推荐: The Graph
原因:
- 免费
- 结构化数据
- 可靠

限制:
- 可能有1-2区块延迟
- 查询限制
```

### 低频监控（5分钟+）

```
推荐: CoinGecko / CoinMarketCap
原因:
- 简单易用
- 历史数据
- 多链聚合

限制:
- 实时性差
- API限制
```

### 多DEX聚合

```
推荐: 1inch API / 0x API
原因:
- 自动聚合多个DEX
- 最优价格
- 路径计算

限制:
- 需要API key
- 有调用限制
```

## 数据质量检查

### 异常检测

```python
def detect_price_anomaly(current_price, historical_prices, threshold=0.05):
    """检测价格异常"""
    mean_price = sum(historical_prices) / len(historical_prices)
    deviation = abs(current_price - mean_price) / mean_price
    
    if deviation > threshold:
        return True, deviation
    return False, deviation
```

### 数据源交叉验证

```python
def verify_price(token, sources):
    """多数据源验证"""
    prices = []
    
    for source_name, fetch_func in sources.items():
        try:
            price = fetch_func(token)
            prices.append((source_name, price))
        except Exception as e:
            print(f"{source_name} failed: {e}")
    
    # 检查一致性
    price_values = [p[1] for p in prices]
    avg_price = sum(price_values) / len(price_values)
    
    for source_name, price in prices:
        deviation = abs(price - avg_price) / avg_price
        status = "✓" if deviation < 0.01 else "⚠️"
        print(f"{status} {source_name}: ${price:.2f} (dev: {deviation:.2%})")
```

---

*选择合适的数据源是成功监控的第一步。*
