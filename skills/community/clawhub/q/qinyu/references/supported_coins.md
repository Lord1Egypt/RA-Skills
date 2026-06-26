# QinYu 支持的币种列表

## 主流币种 (Top 20)

| 币种 | Symbol | CoinGecko ID | 类别 |
|------|--------|--------------|------|
| Bitcoin | BTCUSDT | bitcoin | Layer 1 |
| Ethereum | ETHUSDT | ethereum | Smart Contract |
| BNB | BNBUSDT | binancecoin | Exchange Token |
| Solana | SOLUSDT | solana | Layer 1 |
| XRP | XRPUSDT | ripple | Payment |
| USDC | USDCUSDT | usd-coin | Stablecoin |
| Cardano | ADAUSDT | cardano | Layer 1 |
| Dogecoin | DOGEUSDT | dogecoin | Meme |
| TRON | TRXUSDT | tron | Layer 1 |
| Chainlink | LINKUSDT | chainlink | Oracle |
| Avalanche | AVAXUSDT | avalanche-2 | Layer 1 |
| Sui | SUIUSDT | sui | Layer 1 |
| Toncoin | TONUSDT | toncoin | Layer 1 |
| Shiba Inu | SHIBUSDT | shiba-inu | Meme |
| Polkadot | DOTUSDT | polkadot | Layer 0 |
| Bitcoin Cash | BCHUSDT | bitcoin-cash | Payment |
| UNUS SED LEO | LEOUSDT | leo-token | Exchange Token |
| Litecoin | LTCUSDT | litecoin | Payment |
| Uniswap | UNIUSDT | uniswap | DEX |
| Pepe | PEPEUSDT | pepe | Meme |

## Layer 1 公链

| 币种 | Symbol | CoinGecko ID |
|------|--------|--------------|
| NEAR Protocol | NEARUSDT | near |
| Aptos | APTUSDT | aptos |
| Cosmos | ATOMUSDT | cosmos |
| Fantom | FTMUSDT | fantom |
| Algorand | ALGOUSDT | algorand |
| Tezos | XTZUSDT | tezos |
| EOS | EOSUSDT | eos |
| Harmony | ONEUSDT | harmony |
| Klaytn | KLAYUSDT | klaytn |
| VeChain | VETUSDT | vechain |

## DeFi 代币

| 币种 | Symbol | CoinGecko ID | 类别 |
|------|--------|--------------|------|
| Aave | AAVEUSDT | aave | Lending |
| Maker | MKRUSDT | maker | Stablecoin |
| Lido DAO | LDOUSDT | lido-dao | Liquid Staking |
| Curve | CRVUSDT | curve-dao-token | DEX |
| Compound | COMPUSDT | compound-governance-token | Lending |
| SushiSwap | SUSHIUSDT | sushi | DEX |
| PancakeSwap | CAKEUSDT | pancake-swap | DEX |
| 1inch | 1INCHUSDT | 1inch |
| dYdX | DYDXUSDT | dydx | Derivatives |
| GMX | GMXUSDT | gmx | Derivatives |

## Layer 2

| 币种 | Symbol | CoinGecko ID |
|------|--------|--------------|
| Polygon | MATICUSDT | matic-network |
| Arbitrum | ARBUSDT | arbitrum |
| Optimism | OPUSDT | optimism |
| Immutable X | IMXUSDT | immutable-x |
| Mantle | MNTUSDT | mantle |
| Starknet | STRKUSDT | starknet |

## Meme 币

| 币种 | Symbol | CoinGecko ID |
|------|--------|--------------|
| Dogecoin | DOGEUSDT | dogecoin |
| Shiba Inu | SHIBUSDT | shiba-inu |
| PEPE | PEPEUSDT | pepe |
| FLOKI | FLOKIUSDT | floki |
| Dogwifhat | WIFUSDT | dogwifhat |
| BONK | BONKUSDT | bonk |
| BOME | BOMEUSDT | book-of-meme |
| POPCAT | POPCATUSDT | popcat |

## 其他热门币种

| 币种 | Symbol | CoinGecko ID | 类别 |
|------|--------|--------------|------|
| Stellar | XLMUSDT | stellar | Payment |
| Filecoin | FILUSDT | filecoin | Storage |
| Internet Computer | ICPUSDT | internet-computer | Computing |
| Render | RNDRUSDT | render-token | GPU |
| The Graph | GRTUSDT | the-graph | Indexing |
| Fetch.ai | FETUSDT | fetch-ai | AI |
| SingularityNET | AGIXUSDT | singularitynet | AI |
| Ocean Protocol | OCEANUSDT | ocean-protocol | AI |
| Worldcoin | WLDUSDT | worldcoin | Identity |
| Celestia | TIAUSDT | celestia | Modular |

## 使用示例

```bash
# 主流币种
python3 scripts/qinyu.py analyze BTCUSDT --coin-id bitcoin
python3 scripts/qinyu.py analyze ETHUSDT --coin-id ethereum
python3 scripts/qinyu.py analyze BNBUSDT --coin-id binancecoin
python3 scripts/qinyu.py analyze SOLUSDT --coin-id solana

# DeFi 代币
python3 scripts/qinyu.py analyze AAVEUSDT --coin-id aave
python3 scripts/qinyu.py analyze MKRUSDT --coin-id maker

# Layer 2
python3 scripts/qinyu.py analyze ARBUSDT --coin-id arbitrum
python3 scripts/qinyu.py analyze OPUSDT --coin-id optimism

# Meme 币
python3 scripts/qinyu.py analyze DOGEUSDT --coin-id dogecoin
python3 scripts/qinyu.py analyze PEPEUSDT --coin-id pepe
```

## 查询 CoinGecko ID

如果不确定某个币种的 CoinGecko ID：

1. 访问 https://www.coingecko.com/
2. 搜索币种名称
3. 查看 URL 中的 slug，例如：
   - https://www.coingecko.com/en/coins/bitcoin → ID: `bitcoin`
   - https://www.coingecko.com/en/coins/ethereum → ID: `ethereum`

## 添加新币种

如需添加新币种，只需在调用时指定正确的 symbol 和 coin_id：

```python
analysis = qinyu.analyze("NEWUSDT", "new-coin-gecko-id")
```
