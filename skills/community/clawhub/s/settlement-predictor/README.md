# Settlement Predictor | 链上结算预测器

Real-time on-chain settlement prediction, mempool analysis, and transaction tracking for EVM chains + Bitcoin.

## 支持链

| 链 | Chain ID | 费用单位 | API | Key |
|---|---|---|---|---|
| Ethereum | 1 | Gwei | Etherscan V2 | 可选 |
| Arbitrum | 42161 | Gwei | Arbiscan | 可选 |
| Optimism | 10 | Gwei | Optimism Etherscan | 可选 |
| Base | 8453 | Gwei | Basescan | 可选 |
| Polygon | 137 | Gwei | Polygonscan | 可选 |
| **Bitcoin** | 0 | **sat/vB** | mempool.space | **免费无需Key** |

## 功能特性

| 工具 | 功能 |
|------|------|
| `get-gas-prediction` | 实时获取各档位 Gas（instant/fast/standard/slow）及网络拥堵度 |
| `predict-settlement` | 根据给定 Gas 价格预测交易结算时间与包含概率 |
| `get-optimal-window` | 分析 24 小时 Gas 规律，找到最优交易窗口 |
| `analyze-pending-pool` | 扫描 Mempool 中的待处理交易，检测三明治攻击与 DEX 冲突风险 |
| `track-tx` | 追踪已提交的交易，等待上链确认或失败回执 |
| `verify-contract` | Etherscan API 验证合约源码 + 安全风险扫描（需 Key）|
| `get-token-info` | 获取代币元数据（名称、符号、总供应量、精度）（需 Key）|
| `get-internal-txs` | 获取交易内部调用追踪（Etherscan API）（需 Key）|
| `btc-fee-estimate` | BTC 实时费率（sat/vB）+ Mempool 拥堵度，无需 API Key |
| `btc-predict-settlement` | 预测给定 sat/vB 费率下的 BTC 交易确认时间和概率 |
| `btc-optimal-window` | 分析 UTC 小时规律，找到最便宜的 BTC 交易时段 |
| `track-btc-tx` | 追踪 BTC 交易状态（mempool.space）|
| `analyze-gas-trend` | EVM 链 Gas 趋势分析（滚动历史 + 线性回归），判断涨跌通道 |
| `analyze-btc-trend` | BTC 手续费趋势分析，判断上涨/回落通道 |

## 安装

```bash
pip install -r requirements.txt
python settlement_predictor.py --help
```

## API Key 配置（可选）

基础功能（Gas 预测、结算时间、Mempool 分析）**无需 Key**，开箱即用。

可选 Key（通过环境变量设置）：

| Key | 功能 | 免费申请 |
|-----|------|---------|
| `ETHERSCAN_API_KEY` | 合约验证、代币详情、失败原因解码、内部交易追踪 | https://etherscan.io/myapikey |
| `TENDERLY_API_KEY` | 交易模拟（精准 Gas + 回滚预测） | https://dashboard.tenderly.co/ |

```bash
export ETHERSCAN_API_KEY=你的API密钥
export TENDERLY_API_KEY=你的API密钥
```

## 使用示例

```bash
# 1. 查询当前 Gas 行情
python settlement_predictor.py get-gas-prediction -c ethereum

# 2. 预测结算时间
python settlement_predictor.py predict-settlement -c ethereum -g 30

# 3. 寻找最优交易窗口
python settlement_predictor.py get-optimal-window -c ethereum -u high

# 4. 分析 Mempool 风险（防范三明治攻击）
python settlement_predictor.py analyze-pending-pool \
  -c ethereum -p 0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852 -d buy -a 10000

# 5. 追踪交易状态（含 Etherscan 失败原因解码）
python settlement_predictor.py track-tx -c ethereum -t 0xabc123...

# 6. 合约安全验证（源码 + 风险扫描）🔥
python settlement_predictor.py verify-contract -c ethereum -a 0xdAC17F958D2ee523a2206206994597C13D831ec7

# 7. 代币信息查询（名称、符号、总供应量）🔥
python settlement_predictor.py get-token-info -c ethereum -a 0xdAC17F958D2ee523a2206206994597C13D831ec7

# 8. 交易内部调用追踪（需 Etherscan API Key）🔥
python settlement_predictor.py get-internal-txs -c ethereum -t 0xabc123...

# 9. BTC 费率查询
python settlement_predictor.py btc-fee-estimate --urgency medium

# 10. 预测 BTC 结算时间
python settlement_predictor.py btc-predict-settlement --sat 3 --urgency high

# 11. 最优 BTC 交易窗口
python settlement_predictor.py btc-optimal-window --urgency low

# 12. 追踪 BTC 交易
python settlement_predictor.py track-btc-tx \
  --tx 4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b

# 13. Gas 趋势分析（EVM 链）🔥
# 持续调用多次（每隔1-2分钟）以积累数据点
python settlement_predictor.py analyze-gas-trend -c ethereum

# 14. BTC 手续费趋势分析 🔥
python settlement_predictor.py analyze-btc-trend
```

## API 参考

| 参数 | 说明 |
|------|------|
| `--chain, -c` | 链名：`ethereum`/`arbitrum`/`optimism`/`base`/`polygon` |
| `--gas-price, -g` | Gas 价格（Gwei，仅 predict-settlement）|
| `--urgency, -u` | 紧急度：`low`/`medium`/`high`（仅 optimal-window）|
| `--pool-address, -p` | Uniswap 池子地址（仅 analyze-pending-pool）|
| `--direction, -d` | 交易方向：`buy`/`sell`（仅 analyze-pending-pool）|
| `--amount-usd, -a` | 预估 USD 金额（仅 analyze-pending-pool）|
| `--tx-hash, -t` | 交易哈希（仅 track-tx / get-internal-txs）|
| `--address, -a` | 合约/代币地址（仅 verify-contract / get-token-info）|
| `--format, -f` | 输出格式：`json`（默认）/ `table` |

## 扩展方向（v2 建议）

- [ ] 接入 Tenderly API（免费层）提升交易模拟准确性
- [ ] 存储历史 Gas 数据（SQLite）用于真实模式分析
- [ ] Telegram / Email 最优窗口告警推送
- [ ] 支持更多 DEX（Curve、Balancer、PancakeSwap）
- [ ] 接入 Flashbots RPC 实现 MEV 保护交易提交
- [ ] 添加 Solana Compute Unit (Cu) 预测模型
