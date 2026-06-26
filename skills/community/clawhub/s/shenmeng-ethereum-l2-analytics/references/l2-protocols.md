# Ethereum L2 协议数据库

## 主要 L2 对比 (2026年初)

| L2 | 类型 | 代币 | TVL | TPS | 费用 | 最终性 |
|----|------|------|-----|-----|------|--------|
| **Arbitrum One** | Optimistic | ARB | ~$15B | 40k | $0.10-0.50 | 7天 |
| **Optimism** | Optimistic | OP | ~$8B | 4k | $0.10-0.30 | 7天 |
| **Base** | Optimistic (OP Stack) | - | ~$3B | 4k | $0.10-0.30 | 7天 |
| **Blast** | Optimistic | BLAST | ~$2B | 4k | $0.10-0.30 | 7天 |
| **zkSync Era** | ZK (zkEVM) | ZK | ~$1.5B | 2k | $0.05-0.20 | 即时 |
| **Starknet** | ZK (Cairo VM) | STRK | ~$1B | 1k+ | $0.01-0.10 | 即时 |
| **Polygon PoS** | 侧链 | MATIC | ~$4B | 7k | $0.01-0.10 | ~3分钟 |
| **Polygon zkEVM** | ZK (zkEVM) | MATIC | ~$500M | 2k | $0.05-0.20 | 即时 |
| **Scroll** | ZK (zkEVM) | SCR | ~$300M | 2k | $0.05-0.20 | 即时 |
| **Linea** | ZK (zkEVM) | - | ~$200M | 2k | $0.05-0.20 | 即时 |
| **Mantle** | Optimistic + EigenDA | MNT | ~$500M | 4k | $0.05-0.20 | 7天 |
| **Taiko** | ZK (Based Rollup) | TKO | ~$100M | 2k | $0.05-0.20 | 即时 |

---

## Optimistic Rollups

### Arbitrum One

#### 技术参数
```
启动时间: 2021年8月
技术栈: Arbitrum Nitro
虚拟机: WASM (Geth 核心)
数据可用性: Ethereum L1
排序器: 中心化 (Offchain Labs)
验证者: 无需许可
挑战期: 7天
Gas 优化: Arbitrum Stylus (支持 Rust/C 合约)
```

#### 生态数据 (2026年初)
```
TVL: ~$15B
日交易量: ~$500M
日活跃地址: ~200k
总合约数: ~50k+
主要 DEX: Camelot, Uniswap V3, Balancer
```

#### Arbitrum Nova
```
类型: AnyTrust (低费用变体)
特点: 数据可用性委员会，费用更低
适用: 游戏、社交应用
TVL: ~$100M
```

#### Arbitrum Orbit
```
类型: L3 框架
用途: 构建自定义 L3 链
特点: 使用 Arbitrum 技术栈
代表项目: XAI Games, ApeChain
```

### Optimism (OP Mainnet)

#### 技术参数
```
启动时间: 2021年12月
技术栈: OP Stack
虚拟机: EVM (等效)
数据可用性: Ethereum L1
排序器: 中心化 (Optimism Foundation)
验证者: 无需许可
挑战期: 7天
```

#### Superchain 愿景
```
概念: 基于 OP Stack 的互联 L2 网络
成员: OP Mainnet, Base, Zora, Worldcoin, Mode
共享: 桥、排序器、治理
优势: 跨 L2 无缝迁移
```

#### 生态数据 (2026年初)
```
TVL: ~$8B
日交易量: ~$300M
日活跃地址: ~100k
总合约数: ~30k+
主要 DEX: Velodrome, Uniswap V3, Curve
```

### Base

#### 技术参数
```
启动时间: 2023年8月
技术栈: OP Stack (由 Coinbase 构建)
特色: 与 Coinbase 生态整合
排序器: 中心化 (Coinbase)
特点: 无需代币，使用 ETH
```

#### 生态特点
```
优势:
- Coinbase 用户导流
- 社交应用友好 (Friend.tech)
- 开发者友好

数据 (2026年初):
TVL: ~$3B
日活跃地址: ~500k (含社交应用)
特色应用: Friend.tech, Farcaster
```

### Blast

#### 技术参数
```
启动时间: 2024年2月
技术栈: Optimistic Rollup
特色: 原生收益
排序器: 中心化 (Blur 团队)
```

#### 原生收益机制
```
ETH 质押: Lido 流动性质押收益
稳定币: MakerDAO DSR 收益
自动复投: 收益自动计入余额
```

#### 争议点
```
批评:
- 多签控制，中心化程度高
- 提现需 14 天延迟
- 团队背景 (Blur 的争议历史)

数据 (2026年初):
TVL: ~$2B
特点: 积分系统激励存款
```

---

## ZK Rollups

### zkSync Era

#### 技术参数
```
启动时间: 2023年3月
技术: zk-SNARKs
虚拟机: zkEVM (EVM 兼容)
证明系统: Boojum (PLONK 变体)
排序器: 中心化 (Matter Labs)
验证: 以太坊 L1
```

#### 技术特点
```
zkEVM 兼容:
- 大部分 Solidity 合约可直接部署
- 部分高级特性不支持
- 需要专门测试

账户抽象:
- 原生支持智能合约钱包
- 社交恢复
- 批量交易
```

#### 生态数据 (2026年初)
```
TVL: ~$1.5B
日交易量: ~$50M
日活跃地址: ~50k
主要 DEX: SyncSwap, Mute.io, Maverick
```

### Starknet

#### 技术参数
```
启动时间: 2021年11月 (主网)
技术: zk-STARKs
虚拟机: Cairo VM (非 EVM)
证明系统: STARK
排序器: 中心化 (StarkWare)
数据可用ity: Ethereum L1
```

#### Cairo 语言
```
特点:
- 专门设计用于 ZK 证明
- 高性能
- 学习曲线陡峭

适配方案:
- Warp: Solidity 到 Cairo 转译器
- Kakarot: Cairo 实现的 zkEVM
```

#### 生态数据 (2026年初)
```
TVL: ~$1B
日交易量: ~$30M
日活跃地址: ~30k
主要 DEX: JediSwap, MySwap, 10KSwap
特色: Dojo 游戏引擎
```

### Polygon zkEVM

#### 技术参数
```
启动时间: 2023年3月
技术: zk-SNARKs
虚拟机: zkEVM (等效 EVM)
开发: Polygon 团队
特点: 与 Polygon PoS 互补
```

#### 与 Polygon PoS 关系
```
Polygon PoS: 侧链，高吞吐量
Polygon zkEVM: ZK L2，高安全性
未来: PoS 升级为 zkEVM Validium
```

### Scroll

#### 技术参数
```
启动时间: 2023年10月
技术: zk-SNARKs
虚拟机: zkEVM (等效 EVM)
特点: 开源优先，社区驱动
排序器: 去中心化路线图
```

#### 技术理念
```
完全开源:
- 证明系统开源
- 排序器代码开源
- 强调透明度

社区参与:
- 开放排序器网络路线图
- 社区治理
```

### Linea

#### 技术参数
```
启动时间: 2023年8月
开发: Consensys (MetaMask 母公司)
技术: zk-SNARKs
虚拟机: zkEVM
特点: MetaMask 集成
```

#### 优势
```
用户获取:
- MetaMask 默认集成
- 庞大用户基础
- 低 onboarding 门槛
```

---

## 侧链 / Validium

### Polygon PoS

#### 技术参数
```
启动时间: 2020年6月
类型: 侧链 (将向 L2 转型)
共识: PoS (Bor + Heimdall)
TPS: ~7,000
验证者: 100+
桥: 多签桥 (向 ZK 桥转型)
```

#### 转型路线图
```
阶段 0: 当前状态 (侧链)
阶段 1: ZK 有效性证明 (2024)
阶段 2: 完整 ZK L2 (2025)
```

#### 生态数据 (2026年初)
```
TVL: ~$4B
日交易量: ~$100M
优势: 最早 L2 方案，生态最丰富
主要 DEX: QuickSwap, Uniswap V3
```

### Mantle

#### 技术参数
```
启动时间: 2023年7月
类型: Optimistic L2 + 模块化 DA
DA 层: EigenDA (EigenLayer)
特点: 降低数据可用性成本
代币: MNT
```

#### 创新点
```
EigenDA 整合:
- 数据可用性成本降低 10x
- 继承以太坊安全性
- 支持 DA 层选择
```

---

## 新兴 L2

### Taiko

#### 技术参数
```
类型: Based Rollup + ZK
特色: 去中心化排序器
技术: zk-SNARKs
代币: TKO
状态: 主网上线
```

#### Based Rollup 概念
```
特点:
- 排序由以太坊 L1 验证者完成
- 完全去中心化
- 继承 L1 活性保证
挑战: 费用高，确认慢
```

### Manta Pacific

#### 技术参数
```
类型: Optimistic L2
特色: 隐私保护 (zk 电路)
技术: OP Stack + 隐私模块
代币: MANTA
```

#### 隐私特性
```
合规隐私:
- 可选隐私交易
- 符合监管要求
- 适用于机构
```

---

## L2 技术趋势

### EIP-4844 (Proto-Danksharding) 影响
```
效果:
- L2 费用降低 10-100x
- 数据 blob 存储
- 临时数据可用性

影响:
- 小交易几乎免费
- 促进 L2 采用
- 改变 L2 经济模型
```

### 共享排序器
```
概念: 多个 L2 共享排序器网络
优势:
- 跨 L2 原子交易
- 降低 MEV 提取
- 提升互操作性

项目:
- Espresso Systems
- Astria
- Flashbots SUAVE
```

### 去中心化排序器路线图
```
当前: 大多数 L2 使用中心化排序器
未来:
- Arbitrum: 向无需许可排序器过渡
- Optimism: Fault Proof 系统
- Starknet: 去中心化排序器网络
```
