# WenDao Agent Skill

🏮 问道 NFA 自主修仙 Agent — BAP-578 链上 AI Agent

## 概述

让你的 BNB Chain NFA（Non-Fungible Agent）修士自动修仙。基于 BAP-578 协议标准，通过链上授权的 Agent 子钱包，自动执行闭关修炼、升级、属性分配、论道斗法等操作。

## 能力

- **自动闭关** — 智能判断闭关时机，到时间自动出关领灵气奖励
- **自动升级** — 经验值够了自动 levelUp，获得属性点
- **自动分配属性** — 根据策略自动分配 SP 到力量/敏捷/耐力/智力/根骨
- **自动论道 PK** — 分析对手战力，选择最优场次，自动 approve→depositPK→匹配→结算
- **自动渡劫** — 条件满足自动突破境界
- **链上行为存证** — 所有操作记录为 Merkle Tree（Learning Tree），定期写入链上 NFA 合约

## 使用条件

1. 在 [wendaobsc.xyz](https://wendaobsc.xyz) 用 X 账号铸造 NFA
2. 在道途页面绑定 Agent 子钱包（一键生成）
3. 往子钱包转入约 0.05 BNB 作为 gas 费

## 安装

```bash
npm install -g clawhub
clawhub install wendao-agent
```

## 启动

```bash
wendao-agent start \
  --key 0x你的Agent子钱包私钥 \
  --token-id 1 \
  --strategy balanced
```

## 策略

| 策略 | 说明 |
|------|------|
| `aggressive` | 激进：高频 PK + 快速出关 + 主攻属性 |
| `defensive` | 防守：不打 PK + 8h 长闭关 + 主堆血防 |
| `balanced` | 均衡：适度 PK + 4h 闭关 + 均匀分配 |

## 安全

Agent 子钱包与主钱包完全隔离：
- Agent 钱包里没有 NFA 和 $JW，只有少量 BNB 付 gas
- 合约通过 `setAgentWallet()` 链上授权，只允许执行闭关/升级等零成本操作
- 即使 Agent 私钥泄露，攻击者无法转移任何资产

## 架构

```
Owner 钱包 (主钱包)
    │ setAgentWallet(tokenId, agentAddress) — 链上授权
    ▼
NFA 合约
    │ 检查: ownerOf(tokenId) == caller OR agentWallet[tokenId] == caller
    ▼
Agent 子钱包 (SDK 控制)
    │ 用自己的私钥签名交易
    │ 自动执行: startMeditation / stopMeditation / levelUp / distributeSP
    ▼
Learning Tree
    │ 每次操作 → Merkle leaf → 每10次 → updateLearningTree 上链
```

## 链接

- 官网: [wendaobsc.xyz](https://wendaobsc.xyz)
- 合约 (BSC): NFA `0x3b8d8B6A9Aa1efC474A4eb252048D628569Dd842`
- 协议: BAP-578 (BNB Agent Protocol)

## Tags

bap-578, nfa, bsc, web3, agent, defi, gaming, auto-farming
