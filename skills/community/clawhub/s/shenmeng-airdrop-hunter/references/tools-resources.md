# 工具与资源汇总

## 钱包工具

### 软件钱包

| 钱包 | 特点 | 适用场景 |
|------|------|----------|
| **MetaMask** | 最通用，生态最全 | 日常使用，测试网 |
| **Rabby** | 防钓鱼，安全提示 | 主网交互，防骗 |
| **Phantom** | Solana生态首选 | Solana项目 |
| **Keplr** | Cosmos生态 | Cosmos空投 |
| **Martian** | Aptos/Sui | Move语言项目 |
| **Petra** | Aptos官方 | Aptos生态 |

### 硬件钱包

| 产品 | 价格 | 特点 |
|------|------|------|
| **Ledger Nano S Plus** | $79 | 性价比高 |
| **Ledger Nano X** | $149 | 蓝牙连接 |
| **Trezor Model T** | $219 | 开源 |
| **Keystone** | $129 | 纯气隙，中文 |

**建议**：
- 大额资金用硬件钱包
- 交互用小狐狸/Rabby热钱包

---

## 指纹浏览器

### 产品对比

| 产品 | 价格 | 特点 | 推荐度 |
|------|------|------|--------|
| **AdsPower** | $10/月起 | 中文友好，功能全 | ⭐⭐⭐⭐⭐ |
| **MoreLogin** | $8/月起 | 性价比高，新起之秀 | ⭐⭐⭐⭐ |
| **Dolphin** | €$8/月 | 俄罗斯产品，稳定 | ⭐⭐⭐⭐ |
| **Incogniton** | 免费5个 | 有免费版 | ⭐⭐⭐ |
| **Gologin** | $24/月 | 老牌，稳定 | ⭐⭐⭐ |

### 选择建议

**新手入门**：Incogniton（免费版先试用）
**长期使用**：AdsPower（中文客服好）
**预算有限**：MoreLogin（价格便宜）

### 配置要点

```
每个环境配置：
- 独立 IP（代理）
- 独立浏览器指纹
- 独立 Cookies/缓存
- 独立时区/语言
- 独立屏幕分辨率
```

---

## 代理/IP服务

### 住宅代理

| 服务商 | 价格 | 特点 |
|--------|------|------|
| **Bright Data** | $15/GB | 企业级，贵但稳定 |
| **Oxylabs** | $15/GB | 质量高 |
| **Smartproxy** | $80/月5GB | 性价比 |
| **IPRoyal** | $7/GB | 便宜，够用 |
| **922S5**（原911）| 已关闭 | 找替代 |

### 静态IP/VPS

| 服务商 | 价格 | 适用 |
|--------|------|------|
| **AWS Lightsail** | $5/月 | 长期稳定 |
| **DigitalOcean** | $6/月 | 简单好用 |
| **Vultr** | $5/月 | 多地区 |
| **阿里云海外** | $8/月 | 中文支持 |

### 选择建议

- **精品号**：住宅代理（质量优先）
- **批量号**：VPS自建（成本优先）
- **测试网**：普通VPN即可

---

## 信息追踪工具

### 空投追踪网站

| 网站 | 特点 |
|------|------|
| **DappRadar** | 全面，有空投追踪板块 |
| **DeFiLlama** | 数据权威，有airdrops页面 |
| **Airdrops.io** | 专门空投信息 |
| **Earnifi** | 检查是否有空投可领 |
| **Dropsearn** | 任务型空投汇总 |

### Twitter账号（推荐关注）

**英文**:
- @OlimpioCrypto - 空投快讯
- @MingoAirdrop - 教程详细
- @0xKillTheWolf - 项目分析
- @DropsEarn - 空投汇总
- @DefiLlama - 数据分析

**中文**:
- 各种空投KOL（注意甄别质量）

### Discord社区

**通用**:
- OpenDAO
- Various Airdrop Hunters

**项目官方**:
- 每个项目都有Discord，必加

### 信息聚合工具

**RSS阅读器**：
- Feedly - 订阅项目博客
- Inoreader - 跟踪更新

**通知工具**：
- Discord webhook - 自动推送
- IFTTT - 跨平台自动化
- Telegram bot - 自定义提醒

---

## 自动化工具

### 浏览器自动化

**Python + Selenium/Playwright**:
```python
# 示例：自动领水
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://faucet.example.com")
driver.find_element("id", "address").send_keys(wallet_address)
driver.find_element("id", "submit").click()
```

**Automa** (浏览器插件):
- 可视化工作流
- 无需编程
- 适合简单重复任务

### 脚本模板

**批量转账**:
```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://rpc.example.com'))

for wallet in wallets:
    tx = {
        'to': wallet['address'],
        'value': w3.to_wei(0.01, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': w3.eth.get_transaction_count(sender_address),
    }
    signed = w3.eth.account.sign_transaction(tx, private_key)
    w3.eth.send_raw_transaction(signed.rawTransaction)
```

**批量检查余额**:
```python
for wallet in wallets:
    balance = w3.eth.get_balance(wallet['address'])
    print(f"{wallet['address']}: {w3.from_wei(balance, 'ether')} ETH")
```

### 钱包管理工具

**Excel/Google Sheets**:
- 简单记录
- 自定义字段
- 适合少量账号

**Notion/Airtable**:
- 更强大数据库功能
- 模板丰富
- 适合多项目管理

**专业工具**:
- 自建数据库
- 自动化脚本集成

---

## 安全工具

### 授权管理

**Revoke.cash**:
- https://revoke.cash/
- 查看和撤销合约授权
- 定期检查必做

**DeBank**:
- https://debank.com/
- 查看授权列表
- 资产总览

### 防钓鱼工具

**Rabby钱包**:
- 自动识别钓鱼网站
- 交易前安全提示

**Fire扩展**:
- 模拟交易结果
- 显示实际支出

**Pocket Universe**:
- 交易预览
- 风险提示

### 资产追踪

**Zapper**:
- DeFi仓位追踪
- 多链资产总览

**Zerion**:
- 投资组合管理
- NFT展示

**Koinly**:
- 税务计算
- 空投成本追踪

---

## 实用资源

### 测试网水笼头

| 网络 | 网址 | 备注 |
|------|------|------|
| Sepolia | https://sepoliafaucet.com/ | 需要Alchemy账号 |
| Goerli | 已废弃 | 迁移到Sepolia |
| Mumbai | https://faucet.polygon.technology/ | Polygon测试网 |
| BSC Testnet | https://testnet.bnbchain.org/faucet-smart | BNB测试网 |

### Gas追踪

| 工具 | 网址 |
|------|------|
| Etherscan Gas Tracker | https://etherscan.io/gastracker |
| Ultrasound Money | https://ultrasound.money/ |
| Blocknative | https://www.blocknative.com/gas-estimator |

### 学习资源

**文档**:
- Ethereum.org - 以太坊官方文档
- OpenZeppelin - 合约开发
- Solidity官方文档

**教程**:
- CryptoZombies - Solidity教程
- OpenZeppelin教程
- YouTube各种空投教程

**社区**:
- Reddit r/ethfinance
- Discord各种项目社区

---

## 成本预算参考

### 基础配置成本

| 项目 | 月度成本 | 年度成本 |
|------|----------|----------|
| 指纹浏览器（5环境） | $10-20 | $120-240 |
| 代理IP（5个） | $20-50 | $240-600 |
| VPS（1个） | $5-10 | $60-120 |
| **总计** | **$35-80** | **$420-960** |

### 主网交互成本（按项目）

| 项目类型 | Gas成本 | 建议资金 |
|----------|---------|----------|
| L2项目 | $10-50 | $100-500 |
| L1 DeFi | $100-500 | $1000+ |
| 测试网 | 免费 | 仅需领水时间 |

---

*工欲善其事，必先利其器。选对工具，事半功倍。*
