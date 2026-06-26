# 鲸鱼钱包标签库

## 交易所钱包

### Binance
```
0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE  # 热钱包1
0xdB3c617cDd2fBf0c8611C04A49d34C7B332e2BB6  # 热钱包2
0x5a52E96BAcdaBb82fd05763E25335261B270Efcb  # 冷钱包
```

### Coinbase
```
0x71660c4005BA85c37ccec55d0C4493E66Fe775d3
0x503828976D22510aad0201ac7EC88293211D23Da
```

### OKX
```
0x6b75d8AF000000e20B7a7DD000000090D0000000
```

### Bybit
```
0xf89d7b9c864f589bbF53f821d7EfC68c91d70958
```

### KuCoin
```
0x2B6eD29a95753C3Ad948348e3e7b1A251039FBB9
```

## 知名机构/鲸鱼

### 机构钱包
```yaml
# Jump Trading
- address: 0x9507cE...  # 示例地址
  label: "Jump Trading"
  type: "institution"
  
# Wintermute
- address: 0xdbf5e9c5...
  label: "Wintermute"
  type: "market_maker"
  
# Alameda (已破产，但历史数据有价值)
- address: 0xf02e86d5...
  label: "Alameda Research"
  type: "institution"
  status: "defunct"
```

### 知名鲸鱼
```yaml
# 早期ETH持有者
- address: 0x8ba1f109...
  label: "ETH OG Whale"
  type: "individual"
  
# DeFi大玩家
- address: 0x742d35Cc...
  label: "DeFi Whale"
  type: "individual"
```

## 标签类型定义

```python
WALLET_TYPES = {
    'exchange': '交易所钱包',
    'institution': '机构钱包',
    'market_maker': '做市商',
    'individual': '个人鲸鱼',
    'contract': '智能合约',
    'bridge': '跨链桥',
    'mixer': '混币器'
}
```

## 数据来源

- Arkham Intelligence
- Nansen
- Etherscan Labels
- DefiLlama

---

*保持标签库的更新对于准确分析至关重要。*
