# Monad 测试网交互完整教程

> 融资 $244M，预期空投价值 $5K-20K，当前必做项目 #1

---

## 🔗 官方资源

- 官网：https://www.monad.xyz/
- 测试网：https://testnet.monad.xyz/
- Discord：https://discord.gg/monad
- Twitter：https://twitter.com/monad_xyz
- 文档：https://docs.monad.xyz/

---

## 📝 准备工作

### 1. 添加 Monad 测试网到钱包

**网络配置：**
```
Network Name: Monad Testnet
RPC URL: https://testnet-rpc.monad.xyz/
Chain ID: 10143
Currency Symbol: MON
Block Explorer: https://testnet.monadexplorer.com/
```

**添加步骤：**
1. 打开钱包插件
2. 点击网络切换按钮
3. 选择 "Add Network"
4. 填入上述配置
5. 保存

### 2. 领取测试币（Faucet）

**官方领水：** https://testnet.monad.xyz/

**步骤：**
1. 连接钱包
2. 输入钱包地址
3. 完成验证码
4. 点击 "Request MON"
5. 等待到账（通常几分钟）

**备用领水（Discord）：**
1. 加入 Monad Discord
2. 进入 #faucet 频道
3. 输入：`/faucet 你的钱包地址`
4. 等待机器人发放

**领水限制：**
- 每个地址每24小时可领一次
- 每次约 0.5-1 MON
- 建议多备几个地址（但不要关联）

---

## 🎯 核心交互任务

### 任务1：官方桥接（必做，每周1次）

**目的：** 与官方核心产品交互，权重最高

**步骤：**
1. 访问：https://testnet.monad.xyz/bridge
2. 连接钱包
3. 确保在 Sepolia 网络（需要 Sepolia ETH）
4. 输入桥接金额（建议小额）
5. 确认交易
6. 等待跨链完成（约5-10分钟）
7. **截图保存交易哈希**

**注意事项：**
- 需要 Sepolia 测试网 ETH（从 Sepolia faucet 领取）
- 桥接是双向的，可以 Monad → Sepolia
- 保持规律性，每周1次

---

### 任务2：Acurast - 计算平台

**官网：** https://testnet.acurast.com/

**交互步骤：**
1. 连接钱包（切换到 Monad 测试网）
2. 领取平台代币（如有 faucet）
3. 进入 Staking/质押页面
4. 选择验证器，进行质押
5. 记录质押金额和时间
6. 隔一段时间后解除质押

**频率：** 每周1次

---

### 任务3：Kintsu - 流动性质押

**官网：** https://testnet.kintsu.xyz/

**交互步骤：**
1. 连接钱包
2. 进入 "Stake" 页面
3. 输入质押金额（建议小额）
4. 确认交易
5. 获得流动性质押代币
6. 等待一段时间后，进入 "Unstake" 解除质押

**频率：** 每2周1次

---

### 任务4：NadSwap - DEX交易所

**官网：** https://testnet.nadswap.com/

**交互类型 A：Swap 交易**
1. 连接钱包
2. 选择交易对（如 MON → 其他代币）
3. 输入金额
4. 确认 Swap
5. 反向 Swap 回来

**交互类型 B：添加流动性**
1. 进入 "Pool" 页面
2. 选择 "Add Liquidity"
3. 选择代币对
4. 输入金额
5. 确认添加
6. （可选）后续移除流动性

**频率：** 每周1-2次

---

### 任务5：部署合约（进阶加分项）

**使用 Remix IDE：** https://remix.ethereum.org/

**步骤：**
1. 打开 Remix
2. 创建新文件，粘贴简单合约代码（如 ERC20）
3. 编译合约
4. 切换到 "Deploy & Run" 标签
5. 环境选择 "Injected Provider - MetaMask"
6. 确保钱包在 Monad 测试网
7. 点击 Deploy
8. **保存合约地址**

**示例 ERC20 合约代码：**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TestToken is ERC20 {
    constructor() ERC20("TestToken", "TT") {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }
}
```

---

## 📅 推荐交互计划

### 新手计划（每周5-8小时）

**周三（1-2小时）：**
- 官方桥接
- 1个生态项目交互
- 检查 Discord 公告

**周日（1-2小时）：**
- 1-2个生态项目交互
- 记录本周交互
- 规划下周任务

### 进阶计划（每周10-15小时）

在以上基础上增加：
- 更多生态项目探索
- 合约部署练习
- 多项目并行参与

---

## ⚠️ 常见问题和解决

### 1. 领水失败
- 检查地址是否正确
- 等待24小时后再试
- 尝试 Discord faucet
- 在社区求助

### 2. 交易卡住
- 检查 Gas 费是否足够
- 尝试提高 Gas 价格
- 等待网络拥堵缓解

### 3. 无法连接网站
- 检查网络配置是否正确
- 刷新页面重试
- 清除浏览器缓存

### 4. 交易失败
- 检查余额是否足够
- 确认网络是否正确
- 查看错误信息，在 Discord 求助

---

## 🔔 重要提醒

1. **保持规律**：每周至少交互1-2次
2. **保存记录**：截图交易哈希，记录交互时间
3. **关注公告**：快照时间、规则变化
4. **分散时间**：不要集中在同一时间段操作
5. **安全第一**：只在官方渠道操作

---

## 📊 交互质量评估

**高分行为：**
- 使用官方桥接
- 部署合约
- 多种类型交互（Swap、质押、桥接）
- 持续时间长（3个月以上）
- 交互金额合理（不要太小）

**低分行为：**
- 只有转账
- 单次交互后不再操作
- 金额极小（0.0001级别）
- 短时间内集中操作

---

*祝你撸毛顺利，期待空投到账的那一天！*
