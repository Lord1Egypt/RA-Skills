# API文档速查

## The Graph API

### 基础查询

#### 获取池子价格

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
    tick
    observationIndex
  }
}
```

**变量**：
```json
{
  "poolAddress": "0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8"
}
```

#### 获取多个池子

```graphql
query GetMultiplePools($first: Int!) {
  pools(first: $first, orderBy: volumeUSD, orderDirection: desc) {
    id
    token0 {
      symbol
    }
    token1 {
      symbol
    }
    token0Price
    feeTier
    volumeUSD
    liquidity
  }
}
```

#### 按代币搜索池子

```graphql
query GetPoolsByToken($tokenAddress: String!) {
  pools(where: { 
    or: [
      {token0: $tokenAddress},
      {token1: $tokenAddress}
    ]
  }) {
    id
    token0 {
      symbol
    }
    token1 {
      symbol
    }
    token0Price
    volumeUSD
  }
}
```

### 历史数据查询

#### 最近24小时数据

```graphql
query GetRecentData($poolAddress: String!) {
  poolDayDatas(
    where: { pool: $poolAddress }
    first: 1
    orderBy: date
    orderDirection: desc
  ) {
    date
    open
    high
    low
    close
    volumeUSD
    feesUSD
  }
}
```

####  Swap事件

```graphql
query GetRecentSwaps($poolAddress: String!, $first: Int!) {
  swaps(
    where: { pool: $poolAddress }
    first: $first
    orderBy: timestamp
    orderDirection: desc
  ) {
    id
    timestamp
    amount0
    amount1
    amountUSD
    sqrtPriceX96
    tick
  }
}
```

### 价格计算

```python
def calculate_price_from_sqrt(sqrt_price_x96, token0_decimals, token1_decimals):
    """从sqrtPriceX96计算价格"""
    price = (sqrt_price_x96 ** 2) / (2 ** 192)
    
    # 调整精度
    decimals_diff = token1_decimals - token0_decimals
    price = price * (10 ** decimals_diff)
    
    return price
```

## Web3 合约调用

### Uniswap V3 Pool

#### ABI片段

```json
[
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
  },
  {
    "inputs": [],
    "name": "liquidity",
    "outputs": [{"internalType": "uint128", "name": "", "type": "uint128"}],
    "stateMutability": "view",
    "type": "function"
  }
]
```

#### Python调用

```python
from web3 import Web3

class UniswapV3Pool:
    def __init__(self, provider_url, pool_address):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        
        self.abi = [...]  # 上面的ABI
        self.contract = self.w3.eth.contract(
            address=pool_address,
            abi=self.abi
        )
    
    def get_price(self):
        """获取当前价格"""
        slot0 = self.contract.functions.slot0().call()
        sqrt_price_x96 = slot0[0]
        
        price = (sqrt_price_x96 ** 2) / (2 ** 192)
        return price
    
    def get_liquidity(self):
        """获取流动性"""
        return self.contract.functions.liquidity().call()
    
    def get_tick(self):
        """获取当前tick"""
        slot0 = self.contract.functions.slot0().call()
        return slot0[1]
```

### Uniswap V2 Pair

#### ABI片段

```json
[
  {
    "constant": true,
    "inputs": [],
    "name": "getReserves",
    "outputs": [
      {"internalType": "uint112", "name": "_reserve0", "type": "uint112"},
      {"internalType": "uint112", "name": "_reserve1", "type": "uint112"},
      {"internalType": "uint32", "name": "_blockTimestampLast", "type": "uint32"}
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]
```

#### 价格计算

```python
def get_v2_price(pool_contract):
    """获取Uniswap V2价格"""
    reserves = pool_contract.functions.getReserves().call()
    reserve0 = reserves[0]
    reserve1 = reserves[1]
    
    # 价格 = reserve1 / reserve0
    price = reserve1 / reserve0
    return price
```

## CoinGecko API

### 简单价格

```python
import requests

def get_simple_price(ids, vs_currencies='usd'):
    """获取简单价格"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(ids),
        'vs_currencies': vs_currencies,
        'include_market_cap': 'true',
        'include_24hr_vol': 'true',
        'include_24hr_change': 'true',
        'include_last_updated_at': 'true'
    }
    
    response = requests.get(url, params=params)
    return response.json()

# 使用
prices = get_simple_price(['ethereum', 'bitcoin', 'chainlink'])
```

### 历史数据

```python
def get_market_chart(id, days=30):
    """获取历史价格数据"""
    url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    
    response = requests.get(url, params=params)
    return response.json()

# 使用
data = get_market_chart('ethereum', days=7)
prices = data['prices']  # [[timestamp, price], ...]
```

### 交易所数据

```python
def get_exchanges_with_tickers(id):
    """获取代币在各交易所的价格"""
    url = f"https://api.coingecko.com/api/v3/coins/{id}/tickers"
    params = {
        'include_exchange_logo': 'false',
        'order': 'volume_desc'
    }
    
    response = requests.get(url, params=params)
    return response.json()

# 使用
tickers = get_exchanges_with_tickers('ethereum')
for ticker in tickers['tickers'][:5]:
    print(f"{ticker['market']['name']}: ${ticker['last']}")
```

## 1inch API

### 报价

```python
import requests

def get_1inch_quote(chain_id, from_token, to_token, amount):
    """获取1inch报价"""
    url = f"https://api.1inch.dev/swap/v5.2/{chain_id}/quote"
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY'
    }
    params = {
        'src': from_token,
        'dst': to_token,
        'amount': amount
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 使用
quote = get_1inch_quote(
    1,  # 以太坊
    '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',  # ETH
    '0xA0b86a33E6441E6C7D3D4B4f6B7A2c8D5e9F0123',  # USDC
    '1000000000000000000'  # 1 ETH
)

price = int(quote['toAmount']) / 1e6  # USDC价格
```

### 流动性来源

```python
def get_liquidity_sources(chain_id):
    """获取1inch流动性来源"""
    url = f"https://api.1inch.dev/swap/v5.2/{chain_id}/liquidity-sources"
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY'
    }
    
    response = requests.get(url, headers=headers)
    return response.json()
```

## 0x API

### 价格

```python
def get_0x_price(sell_token, buy_token, sell_amount):
    """获取0x价格"""
    url = "https://api.0x.org/swap/v1/price"
    params = {
        'sellToken': sell_token,
        'buyToken': buy_token,
        'sellAmount': sell_amount
    }
    
    response = requests.get(url, params=params)
    return response.json()

# 使用
price_data = get_0x_price('ETH', 'USDC', '1000000000000000000')
price = 1 / float(price_data['price'])
```

### 来源细分

```python
def get_0x_sources():
    """获取0x来源"""
    url = "https://api.0x.org/swap/v1/sources"
    response = requests.get(url)
    return response.json()
```

## DexScreener API

### 代币数据

```python
def get_dexscreener_token(token_address):
    """获取代币在所有DEX的数据"""
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    response = requests.get(url)
    return response.json()

# 使用
eth_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
data = get_dexscreener_token(eth_address)

for pair in data['pairs']:
    print(f"{pair['dexId']}: ${pair['priceUsd']}")
```

### 配对搜索

```python
def search_dexscreener(query):
    """搜索配对"""
    url = f"https://api.dexscreener.com/latest/dex/search"
    params = {'q': query}
    response = requests.get(url, params=params)
    return response.json()

# 使用
results = search_dexscreener('ETH USDC')
```

---

*熟练掌握API是高效监控的基础。*
