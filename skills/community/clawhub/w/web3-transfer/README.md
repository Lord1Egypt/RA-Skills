[🇺🇸 English](#english) · [🇨🇳 中文](#chinese)

---

<a name="english"></a>

# Antalpha Web3 Transfer

> One natural-language transfer skill for BTC, EVM, and Solana with preview, safety checks, and wallet signing.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/AntalphaAI/web3-transfer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Chains: BTC/EVM/Solana](https://img.shields.io/badge/chains-BTC%20%7C%20EVM%20%7C%20Solana-purple.svg)](https://antalpha.com)
[![Mode: Non-custodial](https://img.shields.io/badge/mode-Non--custodial-green.svg)](https://antalpha.com)

---

## What Is This?

**Antalpha Web3 Transfer** is an instruction-only skill for AI agents that orchestrates multi-chain transfers across:

- Bitcoin
- EVM networks such as Ethereum, Base, Arbitrum, Optimism, Polygon, and BSC
- Solana

It is designed for a zero-custody workflow:

- the AI agent prepares and coordinates the transfer
- the user reviews the preview
- the user signs with their own wallet
- the agent follows up on status and reports the result

This skill is especially useful when the environment already exposes the Antalpha transfer MCP tools and you want the agent to use them correctly and safely.

## Features

- Unified natural-language transfer flow for BTC, EVM, and Solana
- Preview-first execution with clear fee and recipient review
- Address risk scanning for supported chains before transfer
- Medium-risk acknowledgement handling
- Price-unavailable acknowledgement handling
- Batch payout support for up to 10 recipients
- Non-custodial signing model
- Status follow-up through MCP tools

## Supported Scope

| Category | Support |
|---|---|
| Single transfer | Supported |
| Batch transfer | Supported, up to 10 recipients |
| Atomic batch | Not supported |
| EVM native + ERC20 | Supported |
| SOL + SPL token | Supported |
| BTC PSBT handoff | Supported |
| BTC service-side broadcast | Not supported in v1.0 |

## Required MCP Tools

This skill assumes the runtime exposes:

- `transfer-request`
- `transfer-status`
- `transfer-cancel`

If those tools are unavailable, the agent should not pretend it can execute the transfer.

## Installation

This is an **instruction-only** skill.

```bash
clawhub install web3-transfer
```

Or clone manually:

```bash
git clone https://github.com/AntalphaAI/web3-transfer.git
```

## Typical Usage

Examples:

```text
Send 0.1 ETH to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

```text
On Arbitrum, transfer 50 USDT to 0x1234...
```

```text
给这 5 个地址各转 10 USDC（Solana）
```

```text
转 0.01 BTC 到 bc1q...
```

The agent should:

1. call `transfer-request` with `action="prepare"`
2. present the preview and safety result
3. collect explicit confirmation when needed
4. call `transfer-request` with `action="confirm"`
5. provide the signing link or BTC handoff info
6. call `transfer-status` when the user asks for progress

## Safety Principles

- Never ask the user for a private key or seed phrase
- Never hide transfer risk warnings
- Never claim success before status confirms broadcast / completion
- Never invent USD value when price data is unavailable
- Never describe batch transfer as atomic

## Chain Notes

### EVM

- best for ETH and ERC20 transfers
- uses wallet signing flow and signing page
- risk scan is required before transfer preview

### Solana

- supports SOL and SPL token transfers
- uses browser-wallet signing flow
- v1.0 explicitly skips address security scan and must disclose that limitation

### Bitcoin

- uses PSBT handoff flow
- supports BTC transfer preview and signing handoff
- v1.0 does not provide service-side broadcast completion

## Maintainer

**Antalpha** — [https://antalpha.com](https://antalpha.com)

---

<a name="chinese"></a>

# Antalpha Web3 Transfer（统一转账 Skill）

> 一套自然语言转账 Skill，覆盖 BTC、EVM 与 Solana，带预览、风控和钱包签名流程。

[![版本](https://img.shields.io/badge/版本-1.0.0-blue.svg)](https://github.com/AntalphaAI/web3-transfer)
[![协议](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![链](https://img.shields.io/badge/链-BTC%20%7C%20EVM%20%7C%20Solana-purple.svg)](https://antalpha.com)
[![模式](https://img.shields.io/badge/模式-零托管-green.svg)](https://antalpha.com)

---

## 这是什么？

**Antalpha Web3 Transfer** 是一个面向 AI Agent 的 instruction-only Skill，用来协调多链转账流程，支持：

- Bitcoin
- EVM 网络（如 Ethereum、Base、Arbitrum、Optimism、Polygon、BSC）
- Solana

它遵循零托管原则：

- Agent 负责解析、预览、协调流程
- 用户先看预览
- 用户用自己的钱包签名
- Agent 再跟进状态并回报结果

如果你的运行环境已经接好了 Antalpha 的转账 MCP 工具，这个 Skill 的作用就是让 Agent 用正确、安全、稳定的方式使用它们。

## 核心能力

- 统一的 BTC / EVM / Solana 自然语言转账流程
- 先预览后执行
- 转账前风险扫描
- 中风险显式确认
- 价格不可得时显式确认
- 最多 10 个地址的批量转账
- 零托管签名模型
- 基于 MCP 工具的状态跟进

## 支持范围

| 类别 | 支持情况 |
|---|---|
| 单笔转账 | 支持 |
| 批量转账 | 支持，最多 10 个地址 |
| 原子批量 | 不支持 |
| EVM 原生币 + ERC20 | 支持 |
| SOL + SPL Token | 支持 |
| BTC PSBT 交接 | 支持 |
| BTC 服务端广播闭环 | v1.0 不支持 |

## 依赖的 MCP 工具

该 Skill 默认运行环境已暴露以下工具：

- `transfer-request`
- `transfer-status`
- `transfer-cancel`

如果这些工具不可用，Agent 不应假装自己可以执行转账。

## 安装方式

这是一个 **instruction-only** Skill。

```bash
clawhub install web3-transfer
```

或手动克隆：

```bash
git clone https://github.com/AntalphaAI/web3-transfer.git
```

## 使用示例

```text
帮我转 0.1 ETH 到 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

```text
在 Arbitrum 上转 50 USDT 到 0x1234...
```

```text
给这 5 个地址各转 10 USDC（Solana）
```

```text
转 0.01 BTC 到 bc1q...
```

Agent 的标准动作应该是：

1. 用 `transfer-request` 的 `action="prepare"` 建立预览
2. 展示转账预览和风险结果
3. 如有需要，收集显式确认
4. 用 `transfer-request` 的 `action="confirm"` 进入签名阶段
5. 提供签名链接或 BTC handoff 信息
6. 用户追问进度时，用 `transfer-status` 查询

## 安全原则

- 永远不要向用户索要私钥或助记词
- 永远不要隐藏风险提示
- 在状态未明确成功前，不要宣称已经转账成功
- 当价格不可得时，不要编造 USD 估值
- 批量转账不能描述成原子执行

## 各链说明

### EVM

- 适用于 ETH 和 ERC20
- 通过钱包签名页完成签名
- 转账前必须做风险扫描

### Solana

- 支持 SOL 和 SPL Token
- 通过浏览器钱包签名
- v1.0 明确跳过地址安全扫描，必须告知用户

### Bitcoin

- 使用 PSBT handoff 流程
- 支持 BTC 预览和签名交接
- v1.0 不提供服务端广播闭环

## 维护者

**Antalpha** — [https://antalpha.com](https://antalpha.com)
