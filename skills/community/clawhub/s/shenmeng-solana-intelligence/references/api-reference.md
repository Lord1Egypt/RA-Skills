# Solana 链上分析脚本参考

## 常用 API 端点

### 市场数据 (CoinGecko)
```bash
# 获取 Solana 生态代币列表
curl "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=solana-ecosystem&order=market_cap_desc&per_page=100&page=1"

# 获取特定代币数据
curl "https://api.coingecko.com/api/v3/coins/bonk"
```

### DefiLlama API
```bash
# Solana TVL
curl "https://api.llama.fi/chain/Solana"

# 协议 TVL
curl "https://api.llama.fi/protocols"
```

### Helius RPC (链上数据)
```bash
# 获取账户信息
curl -X POST https://mainnet.helius-rpc.com/?api-key=YOUR_KEY \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getAccountInfo",
    "params": ["ACCOUNT_ADDRESS", {"encoding": "jsonParsed"}]
  }'

# 获取交易历史
curl -X POST https://mainnet.helius-rpc.com/?api-key=YOUR_KEY \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getSignaturesForAddress",
    "params": ["ADDRESS", {"limit": 10}]
  }'
```

### Pump.fun 数据
```bash
# 获取最新发射 (非官方 API，可能变动)
# 注意：Pump.fun 没有官方公开 API，数据主要通过前端抓取
```

## 分析指标计算

### 代币健康度评分 (0-100)
```python
def calculate_token_health(metrics):
    """
    计算代币综合健康度
    
    指标权重:
    - 流动性深度: 25%
    - 持有者分布: 20%
    - 交易量趋势: 20%
    - 合约安全性: 20%
    - 社交热度: 15%
    """
    liquidity_score = min(metrics['liquidity_usd'] / 100000, 25)  # 最高25分
    holder_score = (100 - metrics['top10_holder_percent']) * 0.2  # 最高20分
    volume_score = min(metrics['volume_24h_usd'] / 1000000, 20)  # 最高20分
    security_score = 20 if metrics['contract_verified'] else 10  # 最高20分
    social_score = min(metrics['twitter_mentions'] / 1000, 15)  # 最高15分
    
    return liquidity_score + holder_score + volume_score + security_score + social_score
```

### 风险等级评估
```python
def assess_risk_level(token_data):
    """
    评估代币风险等级
    
    高风险信号:
    - 团队控盘 > 50%
    - 流动性 < $50k
    - 合约未验证
    - 年龄 < 7天
    - 无社交媒体
    
    返回: 'LOW' | 'MEDIUM' | 'HIGH' | 'EXTREME'
    """
    risk_score = 0
    
    if token_data.get('team_allocation', 0) > 50:
        risk_score += 3
    if token_data.get('liquidity_usd', 0) < 50000:
        risk_score += 2
    if not token_data.get('contract_verified', False):
        risk_score += 2
    if token_data.get('age_days', 999) < 7:
        risk_score += 2
    if not token_data.get('has_social', False):
        risk_score += 1
        
    if risk_score >= 7:
        return 'EXTREME'
    elif risk_score >= 5:
        return 'HIGH'
    elif risk_score >= 3:
        return 'MEDIUM'
    else:
        return 'LOW'
```

### 机会检测算法
```python
def detect_opportunity_signals(market_data):
    """
    检测潜在机会信号
    
    信号类型:
    1. 突破信号 - 价格突破关键阻力位
    2. 放量信号 - 交易量异常增加
    3. 吸筹信号 - 巨鲸持续买入
    4. 新币信号 - 新发射项目有独特叙事
    """
    signals = []
    
    # 突破信号
    if market_data['price'] > market_data['resistance_7d'] * 1.05:
        signals.append({
            'type': 'BREAKOUT',
            'strength': 'STRONG' if market_data['volume_surge'] > 3 else 'MODERATE',
            'description': '价格突破7日阻力位'
        })
    
    # 放量信号
    if market_data['volume_24h'] > market_data['avg_volume_7d'] * 3:
        signals.append({
            'type': 'VOLUME_SURGE',
            'strength': 'HIGH' if market_data['volume_24h'] > 10 * market_data['avg_volume_7d'] else 'MODERATE',
            'description': f"24h交易量是7日均值的 {market_data['volume_24h'] / market_data['avg_volume_7d']:.1f} 倍"
        })
    
    # 吸筹信号
    if market_data['whale_accumulation_7d'] > 0:
        signals.append({
            'type': 'WHALE_ACCUMULATION',
            'strength': 'HIGH' if market_data['whale_accumulation_7d'] > 100000 else 'MODERATE',
            'description': f"巨鲸7日净流入 ${market_data['whale_accumulation_7d']:,.0f}"
        })
    
    return signals
```

## 常用工具

### 区块浏览器
- [Solscan](https://solscan.io) - 最常用的 Solana 浏览器
- [SolanaFM](https://solana.fm) - 高级分析功能
- [Explorer.solana.com](https://explorer.solana.com) - 官方浏览器

### 数据分析平台
- [DefiLlama](https://defillama.com/chain/Solana) - TVL 和协议数据
- [Dune Analytics](https://dune.com) - 自定义链上查询
- [DexScreener](https://dexscreener.com/solana) - DEX 实时价格图表
- [Birdeye](https://birdeye.so) - Solana 代币聚合器

### 发射平台监控
- [Pump.fun](https://pump.fun) - 最大发射平台
- [LetsBONK.fun](https://letsbonk.fun) - BONK 生态发射台
- [Boop.fun](https://boop.fun) - 游戏化发射台

### 钱包追踪
- [Step Finance](https://step.finance) - 投资组合追踪
- [Zapper](https://zapper.fi) - 多链投资组合
- [DeBank](https://debank.com) - 钱包分析
