# 监控工具推荐

## 可视化监控平台

### DexScreener

**网址**: https://dexscreener.com/

**功能**：
- 实时价格图表
- 多DEX对比
- 新币发现
- 交易历史

**使用场景**：
```
1. 查看代币在所有DEX的价格
2. 发现价差机会
3. 监控交易量
4. 追踪新上线代币
```

**API访问**：
```python
import requests

def get_dexscreener_data(token_address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    response = requests.get(url)
    return response.json()

# 获取ETH数据
data = get_dexscreener_data('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
```

### TradingView

**网址**: https://www.tradingview.com/

**功能**：
- 专业K线图表
- 技术指标
- 预警功能
- 策略回测

**DEX数据**：
- 通过插件支持DEX数据
- 可导入自定义数据源

### APY.vision

**网址**: https://apy.vision/

**功能**：
- LP头寸追踪
- 无常损失计算
- 多DEX聚合
- 收益分析

**特色**：
- 连接钱包自动发现头寸
- 历史收益归因
- 再平衡建议

## 数据监控工具

### Dune Analytics

**网址**: https://dune.com/

**功能**：
- 自定义SQL查询
- 可视化仪表板
- 社区共享查询

**推荐查询**：
```
- DEX交易量对比
- 代币价格走势
- 套利交易统计
- 流动性分析
```

**示例查询**：
```sql
-- Uniswap V3价格查询
SELECT 
    date_trunc('hour', block_time) as hour,
    token0_price,
    token1_price,
    volumeUSD
FROM uniswap_v3.pools
WHERE pool = '0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8'
ORDER BY hour DESC
LIMIT 100
```

### DeFiLlama

**网址**: https://defillama.com/

**功能**：
- TVL追踪
- 收益率比较
- 协议收入
- Yields板块

**API**：
```python
def get_defillama_yields():
    url = "https://yields.llama.fi/pools"
    response = requests.get(url)
    return response.json()
```

### EigenPhi

**网址**: https://eigenphi.io/

**功能**：
- MEV交易分析
- 三明治攻击监控
- 套利机会发现
- 实时数据流

## 开发工具

### Python工具包

#### Web3.py

```python
from web3 import Web3

# 连接节点
w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))

# 读取合约
contract = w3.eth.contract(address=pool_address, abi=abi)
price = contract.functions.slot0().call()
```

#### CCXT

```python
import ccxt

# 连接多个交易所
exchanges = {
    'binance': ccxt.binance(),
    'coinbase': ccxt.coinbase(),
}

# 获取价格
for name, exchange in exchanges.items():
    ticker = exchange.fetch_ticker('ETH/USDC')
    print(f"{name}: {ticker['last']}")
```

### Node.js工具包

#### Ethers.js

```javascript
const { ethers } = require('ethers');

const provider = new ethers.providers.JsonRpcProvider('https://eth.llamarpc.com');

// 读取价格
const pool = new ethers.Contract(poolAddress, abi, provider);
const slot0 = await pool.slot0();
const price = calculatePrice(slot0.sqrtPriceX96);
```

#### Axios + WebSocket

```javascript
const axios = require('axios');
const WebSocket = require('ws');

// REST API获取价格
async function getPrice() {
    const response = await axios.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd');
    return response.data.ethereum.usd;
}

// WebSocket实时数据
const ws = new WebSocket('wss://stream.coingecko.com/');
ws.on('message', (data) => {
    console.log('Price update:', JSON.parse(data));
});
```

## 监控告警工具

### Telegram Bot

**创建Bot**：
1. 找 @BotFather
2. 创建新bot
3. 获取token

**发送消息**：
```python
import requests

def send_telegram_alert(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, json=payload)

# 使用
send_telegram_alert(
    'YOUR_BOT_TOKEN',
    'YOUR_CHAT_ID',
    '🚨 ETH价格突破$4000！'
)
```

### Discord Webhook

```python
import requests

def send_discord_alert(webhook_url, message):
    payload = {
        'content': message,
        'username': 'DEX Monitor'
    }
    requests.post(webhook_url, json=payload)

# 使用
send_discord_alert(
    'YOUR_WEBHOOK_URL',
    '发现套利机会！价差1.2%'
)
```

### PagerDuty / OpsGenie

**企业级告警**：
- 分级告警
- 值班轮换
- 电话/短信通知

### 日志工具

#### Loguru (Python)

```python
from loguru import logger

# 配置日志
logger.add("price_monitor.log", rotation="1 day", retention="7 days")

# 使用
logger.info("Price update: ETH = $3500")
logger.warning("Large spread detected: 1.5%")
```

## 基础设施

### 节点服务

| 提供商 | 免费额度 | 特点 |
|--------|----------|------|
| **Infura** | 100K requests/day | 稳定可靠 |
| **Alchemy** | 300M compute units | 功能丰富 |
| **QuickNode** | 无免费版 | 高性能 |
| **Ankr** | 无限制 | 免费好用 |
| **PublicNode** | 无限制 | 完全免费 |

### 免费RPC列表

```
以太坊:
- https://eth.llamarpc.com
- https://rpc.ankr.com/eth
- https://ethereum.publicnode.com

Arbitrum:
- https://arb1.arbitrum.io/rpc
- https://arbitrum.llamarpc.com

其他链:
参考 https://chainlist.org/
```

### 服务器部署

#### VPS推荐

| 提供商 | 价格 | 适合 |
|--------|------|------|
| **AWS Lightsail** | $5/月 | 入门 |
| **DigitalOcean** | $6/月 | 简单 |
| **Vultr** | $5/月 | 灵活 |
| **Hetzner** | €4.5/月 | 性价比 |

#### Docker部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "monitor.py"]
```

```yaml
# docker-compose.yml
version: '3'
services:
  monitor:
    build: .
    restart: always
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - WEB3_PROVIDER=${WEB3_PROVIDER}
    volumes:
      - ./logs:/app/logs
```

## 监控看板

### Grafana

**可视化监控**：
- 实时价格图表
- 价差热力图
- 告警统计

**数据源**：
- InfluxDB
- Prometheus
- PostgreSQL

### 自建看板

**Streamlit (Python)**：
```python
import streamlit as st

st.title("DEX价格监控看板")

# 实时价格
prices = get_prices()
st.line_chart(prices)

# 价差表
spreads = calculate_spreads(prices)
st.table(spreads)

# 告警状态
if max(spreads) > THRESHOLD:
    st.error("🚨 发现套利机会！")
```

---

*工欲善其事，必先利其器。选对工具，监控效率翻倍。*
