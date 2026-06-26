# 交互教程指南

## Monad 测试网详细教程

### 准备工作

**1. 钱包配置**
```
Network Name: Monad Testnet
RPC URL: https://testnet-rpc.monad.xyz/
Chain ID: 10143
Currency Symbol: MON
Block Explorer: https://testnet.monadexplorer.com/
```

**2. 领水渠道**
- 官方水笼头：https://testnet.monad.xyz/
  - 要求：Twitter账号（注册>30天，有头像）
  - 数量：50 MON/天
  - 冷却：24小时
  
- Discord水笼头：
  - 加入 https://discord.gg/monad
  - 进入 #faucet 频道
  - 发送 `/faucet 你的地址`

- 社区水笼头（备用）：
  - 关注社区公告

### 交互步骤

**Step 1: 官方桥接（必做）**
```
网址：https://testnet.monad.xyz/bridge

操作：
1. 切换到 Sepolia 网络
2. 输入要桥接的 ETH 数量（建议 0.01-0.1）
3. 确认交易，等待确认（约5-10分钟）
4. 切换到 Monad Testnet 查看余额

注意：
- 需要有 Sepolia ETH（从Sepolia水笼头领）
- 桥接是双向的，可以桥回
```

**Step 2: 部署合约（高分项）**
```
工具：Remix（https://remix.ethereum.org/）

步骤：
1. 新建文件 SimpleStorage.sol
2. 粘贴以下代码：

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 storedData;
    
    function set(uint256 x) public {
        storedData = x;
    }
    
    function get() public view returns (uint256) {
        return storedData;
    }
}

3. 编译合约（Ctrl+S）
4. 部署到 Monad Testnet
5. 调用 set 和 get 函数
```

**Step 3: 生态项目交互**

*Kintsu（流动性质押）*
- 网址：https://app.kintsu.xyz/
- 操作：质押 MON 获得 stMON
- 频率：每周一次

*NadSwap（DEX）*
- 网址：https://app.nadswap.xyz/
- 操作：Swap、添加流动性
- 建议交易对：MON/stMON

*Curvance（借贷）*
- 网址：https://monad.curvance.com/
- 操作：存入、借款
- 策略：存入 stMON，借出 MON，循环

*Acurast（预言机）*
- 网址：https://app.acurast.com/
- 操作：质押、参与任务

**Step 4: NFT 交互**
- 关注 Monad 生态 NFT 项目
- 铸造、交易测试 NFT

### 时间安排
- **频率**：每周 1-2 次交互
- **周期**：持续 3-6 个月
- **建议**：设置日历提醒

---

## Sahara AI 白名单攻略

### 第一批（已结束）
- 时间：2024年Q4 - 2025年Q1
- 参与者：80万+
- 白名单：1万个

### 第二批（待定）

**准备工作**：
1. 准备多个邮箱
2. 准备 Twitter 账号（需有活跃度）
3. 准备 Discord 账号
4. 准备钱包地址

**Galxe 任务**：
- 网址：https://app.galxe.com/quest/saharalabs
- 任务类型：
  - 关注官方 Twitter
  - 转发推文
  - 加入 Discord
  - 完成测验

**提高成功率技巧**：
- 使用不同 IP 申请多个账号
- 完善社交账号资料（头像、简介）
- 参与社区讨论（Discord活跃度）
- 完成所有可选任务

---

## Eclipse 主网交互教程

### 跨链桥
```
网址：https://eclipse.bridge.lightlink.io/

步骤：
1. 连接钱包（Ethereum 网络）
2. 输入 ETH 数量
3. 确认跨链
4. 等待到账（约10-30分钟）

建议金额：0.05-0.1 ETH
```

### DeFi 交互

*Invariant（DEX）*
- 网址：https://app.invariant.exchange/
- 操作：
  1. Swap（建议金额：$50-100）
  2. 添加流动性
  3. 收取手续费

*Titan（永续合约）*
- 网址：https://app.titan.exchange/
- 操作：
  1. 存入 USDC
  2. 开多/开空（建议小额）
  3. 定期平仓再开仓

### 频率建议
- 每周 2-3 次交互
- 每次包含多种操作类型
- 保持连续性

---

## Polymarket 参与指南

### 注册流程
1. 访问 https://polymarket.com/
2. 邮箱注册
3. 完成 KYC（如需要）
4. 充值 USDC（Polygon 网络）

### 预测参与
```
选择事件类型：
- 政治事件（美国大选等）
- 体育比赛
- 加密货币价格
- 娱乐八卦

策略：
1. 选择自己熟悉的领域
2. 小额分散投资
3. 关注赔率变化
4. 适时退出
```

### 流动性提供
```
操作：
1. 选择事件市场
2. 点击 "Add Liquidity"
3. 输入 USDC 数量
4. 确认提供

收益来源：
- 交易手续费分成
- 潜在空投

风险：
- 无常损失
- 市场偏向单边
```

---

## 通用交互检查清单

### 每周必做
- [ ] 检查测试币余额
- [ ] 完成至少 1 次主要交互
- [ ] 检查新项目公告
- [ ] 备份钱包私钥/助记词

### 每月必做
- [ ] 统计交互成本
- [ ] 评估项目进展
- [ ] 调整策略
- [ ] 更新工具

### 安全 checklist
- [ ] 验证网站 URL（防钓鱼）
- [ ] 使用硬件钱包（大额）
- [ ] 不点击可疑链接
- [ ] 定期检查授权（Revoke）

---

## 工具推荐

### 钱包
- **MetaMask**：最通用
- **Rabby**：防钓鱼功能强
- **Phantom**：Solana生态

### 指纹浏览器
- **AdsPower**：中文友好
- **MoreLogin**：性价比高
- **Dolphin**：俄罗斯产品

### 代理/VPN
- **911s5**（已关闭，找替代）
- **Bright Data**
- **IPRoyal**

### 自动化工具
- **Python + Selenium**：自定义脚本
- **Automa**：浏览器插件
- **Zapier**：简单自动化

---

*实践出真知，多操作才能熟悉流程。*
