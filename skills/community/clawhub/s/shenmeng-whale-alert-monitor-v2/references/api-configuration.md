# API数据源配置指南

## Etherscan API

### 基础配置
```python
ETHERSCAN_API_KEY = "YourApiKey"
BASE_URL = "https://api.etherscan.io/api"
```

### 常用端点

#### 获取账户交易
```
module=account
action=txlist
address={address}
startblock=0
endblock=99999999
sort=desc
apikey={apikey}
```

#### 获取ERC20转账
```
module=account
action=tokentx
address={address}
contractaddress={token_contract}
startblock=0
endblock=99999999
sort=desc
apikey={apikey}
```

#### 获取账户余额
```
module=account
action=balance
address={address}
tag=latest
apikey={apikey}
```

### 速率限制
- 5 calls/second
- 100,000 calls/day (免费版)

## Alchemy API

### 配置
```python
ALCHEMY_API_KEY = "your-api-key"
ETH_MAINNET_URL = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
```

### 特色功能

#### Asset Transfers API
```python
from alchemy import Alchemy

alchemy = Alchemy(ALCHEMY_API_KEY)

transfers = alchemy.core.get_asset_transfers({
    "fromBlock": "0x0",
    "toBlock": "latest",
    "fromAddress": "0x...",
    "category": ["external", "erc20", "erc721", "erc1155"]
})
```

### 免费额度
- 300M compute units/month

## Moralis API

### 配置
```python
MORALIS_API_KEY = "your-api-key"
```

### 常用端点

#### 获取钱包代币余额
```python
import requests

url = f"https://deep-index.moralis.io/api/v2/{address}/erc20"
headers = {
    "X-API-Key": MORALIS_API_KEY
}
response = requests.get(url, headers=headers)
```

#### 获取交易历史
```python
url = f"https://deep-index.moralis.io/api/v2/{address}"
params = {
    "chain": "eth",
    "order": "desc"
}
```

## Web3.py 直连

### 配置
```python
from web3 import Web3

# 使用Alchemy/Infura节点
w3 = Web3(Web3.HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/KEY"))

# 检查连接
print(w3.is_connected())
```

### 查询余额
```python
balance = w3.eth.get_balance("0x...")
balance_eth = w3.from_wei(balance, 'ether')
```

### 获取交易
```python
tx = w3.eth.get_transaction("0x...")
receipt = w3.eth.get_transaction_receipt("0x...")
```

## 跨链支持

### 支持的链
```yaml
chains:
  ethereum:
    chain_id: 1
    rpc: https://eth-mainnet.g.alchemy.com/v2/${KEY}
    explorer: https://etherscan.io
    
  bsc:
    chain_id: 56
    rpc: https://bsc-dataseed.binance.org
    explorer: https://bscscan.com
    
  arbitrum:
    chain_id: 42161
    rpc: https://arb-mainnet.g.alchemy.com/v2/${KEY}
    explorer: https://arbiscan.io
    
  optimism:
    chain_id: 10
    rpc: https://opt-mainnet.g.alchemy.com/v2/${KEY}
    explorer: https://optimistic.etherscan.io
```

## 环境变量配置

### .env 文件
```bash
# Etherscan
ETHERSCAN_API_KEY=xxx

# Alchemy
ALCHEMY_API_KEY=xxx

# Moralis
MORALIS_API_KEY=xxx

# Infura (备选)
INFURA_PROJECT_ID=xxx
INFURA_PROJECT_SECRET=xxx

# 通知
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
DISCORD_WEBHOOK_URL=xxx
```

---

*选择稳定可靠的节点服务对于实时监控至关重要。*
