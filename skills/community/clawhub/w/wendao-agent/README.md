# wendao-agent (ClawHub)

🏮 **问道 NFA Agent SDK** — BAP-578 自主修仙 AI Agent

让你的链上修士 NFA 自动闭关修炼、自动升级、自动分配属性、自动论道斗法。基于 BNB Smart Chain BAP-578 协议标准。

---

## 它能做什么

你铸造了一个 NFA（修士 NFT），但你不想每天手动上去闭关、升级。安装这个 SDK，你的 NFA 会自己修仙：

- 🧘 **自动闭关** — 智能判断闭关时机，到时间自动出关结算经验（灵气奖励需 owner 手动领取）
- 📈 **自动升级** — 经验够了自动 levelUp
- 🎯 **自动分配属性** — 根据策略自动分配 SP 到五维
- ⚔️ **自动论道** — 分析对手，选最优场次，自动 PK（可选）
- 🔮 **自动渡劫** — 条件满足自动突破境界（可选）
- 📜 **链上存证** — 所有行为记录为 Merkle Tree，定期写入链上

---

## 前置条件

你需要先在 [wendaobsc.xyz](https://wendaobsc.xyz) 完成：

1. ✅ 用 X 账号铸造了 NFA
2. ✅ 在「道途」页面绑定了 Agent 子钱包
3. ✅ 往子钱包转了少量 BNB（约 0.05 BNB 作为 gas 费）

---

## 安装

```bash
clawhub install wendao-agent
```

---

## 使用方法

### 方式一：命令行（推荐）

```bash
# 启动 Agent
wendao-agent start \
  --key 0x你的Agent子钱包私钥 \
  --token-id 1 \
  --strategy balanced

# 查看 NFA 状态
wendao-agent status \
  --key 0x你的Agent子钱包私钥 \
  --token-id 1
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|:----:|------|
| `--key` | ✅ | Agent 子钱包私钥（不是你的主钱包！） |
| `--token-id` | ✅ | 你的 NFA tokenId（铸造时获得） |
| `--strategy` | 否 | `aggressive` / `defensive` / `balanced`（默认 balanced） |
| `--interval` | 否 | 决策间隔秒数（默认 300 = 5分钟） |
| `--rpc` | 否 | BSC RPC URL（默认公共节点） |
| `--api` | 否 | 后端 API（默认 https://wendaobsc.xyz） |

### 方式二：代码集成

```typescript
import { WenDaoAgent } from "wendao-agent";

const agent = new WenDaoAgent({
  agentPrivateKey: "0x...",
  rpcUrl: "https://bsc-dataseed1.bnbchain.org",
  tokenId: 1,
  contracts: {
    nfa: "0x3b8d8B6A9Aa1efC474A4eb252048D628569Dd842",
    vault: "0x5FF4F77213AF077fF82270B32916F62900a1DA61",
    token: "0x869f5d274122a91D98f4fbE4f576C351808dDa29",
  },
  apiUrl: "https://wendaobsc.xyz",
  strategy: "balanced",
  interval: 300,
});

agent.on("action", (log) => {
  console.log(`${log.action}: ${log.details}`);
});

await agent.start();
```

---

## 三种策略

| 策略 | 风格 | 闭关 | PK | 属性分配 |
|------|------|------|-----|---------|
| `aggressive` | ⚔️ 激进 | 1h 出关 | 主动打凡境/灵境 | 主攻 STR+AGI |
| `defensive` | 🛡 防守 | 8h 长闭关 | 不打 PK | 主堆 END+CON |
| `balanced` | ⚖ 均衡 | 4h 出关 | 适度打凡境 | 均匀分配 |

### 自定义策略

```typescript
import { WenDaoAgent, type CustomStrategy } from "wendao-agent";

const myStrategy: CustomStrategy = {
  name: "my-strategy",
  shouldMeditate: (state) => !state.isMeditating && !state.isInPK,
  shouldStopMeditation: (state) => state.pendingXP > 500,
  shouldLevelUp: (state) => state.warrior.xp >= state.xpToNextLevel,
  shouldBreakthrough: () => false, // 不自动渡劫
  shouldPK: () => ({ should: false, tier: 0 }), // 不自动 PK
  distributeSP: (_state, points) => {
    // 全部加力量
    return [points, 0, 0, 0, 0];
  },
};

const agent = new WenDaoAgent({ ...config, strategy: myStrategy });
```

---

## 架构原理

### 为什么需要 Agent 子钱包？

```
你的主钱包 (MetaMask)              Agent 子钱包
┌────────────────────┐            ┌──────────────────┐
│ 持有 NFA #1        │            │ 只有 0.05 BNB    │
│ 持有 50000 $JW     │            │ 没有 NFA         │
│ 质押 10000 $JW     │            │ 没有 $JW         │
│                    │            │                  │
│ 大额资金全在这      │            │ 只付 gas 费      │
└────────────────────┘            └──────────────────┘
         │                                │
    手动操作：                         自动操作：
    - 质押/取消质押                     - 闭关/出关
    - 领取质押奖励                     - 升级
    - 渡劫                            - 分配属性
```

### 安全隔离

1. **Agent 子钱包里没有你的 NFA 和 $JW** — 即使私钥泄露，攻击者偷不走任何资产
2. Agent 只能执行零成本操作（闭关/升级/分配属性），这些操作**不花 $JW，只花 gas**
3. 合约通过 `setAgentWallet()` 链上绑定，只有你主钱包授权过的子钱包才能操作你的 NFA

### 链上授权机制

```
第1步：你用主钱包调用 setAgentWallet(tokenId, agentAddress) — 链上记录绑定关系

第2步：Agent 用子钱包调用 startMeditation(tokenId) — 合约检查：
       msg.sender == ownerOf(tokenId)?     → 不是
       msg.sender == agentWallet[tokenId]?  → 是 ✅ 放行
```

### Learning Tree（BAP-578 道果）

Agent 的每次操作都会被记录为 Merkle Tree 的叶子节点：

```
操作1: startMeditation → hash(timestamp, action, details)
操作2: stopMeditation  → hash(timestamp, action, details)
操作3: levelUp         → hash(timestamp, action, details)
...

每积累 10 次操作 → 计算 Merkle Root → 调用 updateLearningTree(tokenId, root) 上链
```

链上存储的 merkle root 就是你的 NFA 的「道果」——可验证的链上行为存证。

---

## Agent 每次决策做什么

```
tick() 每隔 N 秒执行一次：
  │
  ├── 读取链上状态（境界/等级/XP/质押/闭关/PK）
  │
  ├── 有未分配的 SP？ → 按策略分配到五维属性
  ├── XP 够升级？    → 自动 levelUp
  ├── 在闭关中？      → 到时间了就 stopMeditation
  ├── 没在闭关？      → 满足条件就 startMeditation
  ├── 策略允许 PK？   → approve → depositPK → 调后端匹配 → settlePK
  │
  └── 记录行为到 Learning Tree → 每 10 次自动上链
```

---

## 合约地址 (BSC Mainnet)

| 合约 | 代理地址（永不变） |
|------|---------|
| JingwuNFA (修士) | `0x3b8d8B6A9Aa1efC474A4eb252048D628569Dd842` |
| GameVault (金库) | `0x5FF4F77213AF077fF82270B32916F62900a1DA61` |
| $JW Token (灵石) | `0x869f5d274122a91D98f4fbE4f576C351808dDa29` |

---

## API 导出

```typescript
// 核心
export { WenDaoAgent } from "./agent";
export { LearningTree } from "./learning-tree";

// 策略
export { getStrategy, aggressiveStrategy, defensiveStrategy, balancedStrategy } from "./strategies";

// 类型
export type {
  AgentConfig,
  AgentState,
  ActionLog,
  CustomStrategy,
  StrategyType,
  Warrior,
} from "./types";
```

---

## 常见问题

**Q: Agent 能偷走我的 NFA 或 $JW 吗？**
A: 不能。Agent 子钱包里没有你的任何资产。合约只允许 agent 执行闭关、升级等操作，无法 transfer NFA 或 $JW。

**Q: Agent 子钱包需要多少 BNB？**
A: 约 0.05 BNB（每次链上操作约 $0.01，够几百次）。

**Q: 可以同时给多个 NFA 跑 Agent 吗？**
A: 可以，每个 NFA 绑定不同的 agent 子钱包，分别启动。

**Q: 服务器挂了怎么办？**
A: Agent 不影响你的 NFA 状态。如果闭关中 Agent 断了，你可以手动去官网出关，或重启 Agent。

**Q: PK 会亏钱吗？**
A: PK 需要 $JW（从 agent 子钱包扣）。如果你不想 PK，用 `defensive` 策略，Agent 只闭关升级不打架。

---

## License

MIT
