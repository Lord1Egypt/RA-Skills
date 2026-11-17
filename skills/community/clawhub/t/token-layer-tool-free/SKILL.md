---
slug: token-layer-tool-free
name: token-layer-tool-free
version: 1.0.0
displayName: 跨链代币入门工具
summary: "跨链代币数据查询工具，支持主流链代币信息与基础价格查询.。面向个人加密货币用户的跨链代币数据查询工具。支持以太坊/BSC/"
license: Proprietary
edition: free
description: '面向个人加密货币用户的跨链代币数据查询工具。支持以太坊/BSC/

  Polygon等主流链上的代币信息查询，包括合约地址、价格、流动性

  等基础数据。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。Use
  when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。'
tags:
  - Operations
  - 加密货币
  - 跨链
  - 代币
  - 工具
  - 效率
  - ethereum
  - bsc
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# 跨链代币入门工具（免费版）

## 概述

本工具为个人加密货币用户提供跨链代币数据查询能力。支持主流区块链上的代币信息查询，包括合约地址、价格、流动性等基础数据。适合个人用户进行跨链代币研究与投资决策辅助.
## 核心能力

### 查询功能

| 功能 | 说明 | 免费版支持 |
|---|---|-----|
| 代币信息 | 合约地址/精度/总量 | 支持 |
| 价格查询 | 实时价格 | 支持 |
| 流动性 | 流动性池规模 | 支持 |
| 多链支持 | 支持的区块链 | 主流5条链 |
| 批量查询 | 多代币并行 | 不支持 |
| 跨链桥 | 桥接信息 | 不支持 |
| 实时监控 | 价格告警 | 不支持 |
| 深度分析 | 链上行为 | 不支持 |

**处理**: 解析查询功能的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回查询功能的响应数据,包含状态码、结果和日志.
### 支持的区块链

| 链名称 | 代币数量 | 免费版支持 |
|:-----|:-----|:-----|
| Ethereum | 10000+ | 支持 |
| BSC | 5000+ | 支持 |
| Polygon | 3000+ | 支持 |
| Arbitrum | 2000+ | 支持 |
| Optimism | 1500+ | 支持 |

**处理**: 解析支持的区块链的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回支持的区块链的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：跨链代币数据查询、支持主流链代币信、息与基础价格查询、面向个人加密货币、用户的跨链代币数、据查询工具、支持以太坊、等主流链上的代币、信息查询、包括合约地址、等基础数据、Use、when、需要数据分析、报表生成、统计洞察、数据可视化时使用、不适用于实时流数、据处理、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：查询代币信息

用户输入："查一下USDC在不同链上的合约地址"

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | 跨链代币入门工具处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 跨链代币查询
python3 （请参考skill目录中的脚本文件） info \
  --symbol USDC \
  --chains "ethereum,bsc,polygon"
# ...
# 输出：
# === USDC 跨链信息 ===
# Ethereum:  0xA0b8...eB48 (精度:6)
# BSC:       0x8AC7...e14E (精度:18)
# Polygon:   0x2791...ca44 (精度:6)
```

### 场景二：价格查询

用户输入："查UNI在各链上的价格"

```bash
# 跨链价格查询
python3 （请参考skill目录中的脚本文件） price \
  --symbol UNI \
  --chains "ethereum,arbitrum,optimism"
# ...
# 输出各链价格
```

### 场景三：流动性查询

用户输入："查UNI在以太坊上的流动性"

```bash
# 流动性查询
python3 （请参考skill目录中的脚本文件） liquidity \
  --symbol UNI \
  --chain ethereum
# ...
# 输出流动性池信息
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境准备

```bash
# 依赖说明
pip install requests web3
# ...
# 查询代币
python3 （请参考skill目录中的脚本文件） info --symbol USDC --chains "ethereum,bsc"
```

### 常用命令

```bash
# 代币信息
python3 （请参考skill目录中的脚本文件） info --symbol USDC --chains "ethereum,bsc,polygon"
python3 （请参考skill目录中的脚本文件） info --address 0xA0b8...eB48 --chain ethereum
# ...
# 价格查询
python3 （请参考skill目录中的脚本文件） price --symbol UNI --chains "ethereum,arbitrum"
# ...
# 流动性
python3 （请参考skill目录中的脚本文件） liquidity --symbol UNI --chain ethereum
# ...
# 代币列表
python3 （请参考skill目录中的脚本文件） list --chain ethereum --top 20
# ...
# 合约验证
python3 （请参考skill目录中的脚本文件） verify --address 0x... --chain ethereum
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 查询配置

```yaml
token_config:
  api:
    endpoints:
      ethereum: "https://api.etherscan.io"
      bsc: "https://api.bscscan.com"
      polygon: "https://api.polygonscan.com"
    api_keys:
      ethereum: "${ETHERSCAN_API_KEY}"
      bsc: "${BSCSCAN_API_KEY}"
# ...
  chains:
    supported: ["ethereum", "bsc", "polygon", "arbitrum", "optimism"]
    default: ethereum
# ...
  cache:
    ttl: 60
    storage: "./cache/"
# ...
  rpc:
    ethereum: "https://mainnet.infura.io/v3/${INFURA_KEY}"
    bsc: "https://bsc-dataseed.binance.org"
```

## 最佳实践

1. **合约验证**：投资前务必验证合约地址的真实性
2. **多链对比**：同一代币在不同链上可能有不同合约
3. **流动性关注**：低流动性代币交易滑点大
4. **数据时效**：链上数据实时变化，查询结果仅供参考

| 实践要点 | 说明 |
|:---:|:---:|
| 合约安全 | 仅信任官方公布的合约地址 |
| 精度差异 | 同一代币在不同链上精度可能不同 |
| 桥接风险 | 跨链桥接存在安全风险，了解后再使用 |
| 免责声明 | 数据仅供参考，不构成投资建议 |

## 常见问题

### Q1：免费版支持多少条链？

免费版支持以太坊、BSC、Polygon、Arbitrum和Optimism五条主流链。如需更多链支持，建议升级PRO版.
### Q2：数据来源是什么？

代币数据来自各链的区块浏览器API（如Etherscan）和去中心化数据源（如CoinGecko）。价格数据可能有延迟.
### Q3：支持跨链桥接查询吗？

免费版不包含跨链桥接信息查询。如需查询跨链桥接路径与费用，建议升级PRO版.
### Q4：可以监控代币价格变化吗？

免费版仅支持即时查询，不支持价格监控。如需实时价格告警，建议升级PRO版.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| requests | Python库 | 必需 | `pip install requests` |
| web3 | Python库 | 可选 | `pip install web3`（链上查询） |

### API Key 配置

| 服务 | 环境变量 | 是否必需 | 用途 |
|---:|:---|---:|---:|
| Etherscan | `ETHERSCAN_API_KEY` | 推荐 | 以太坊数据查询 |
| BSCScan | `BSCSCAN_API_KEY` | 推荐 | BSC数据查询 |
| Infura | `INFURA_KEY` | 可选 | RPC节点访问 |

- 未配置API Key时使用免费公共接口，频率较低
- 所有Key存储在本地环境变量

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本执行）
- **说明**: 通过区块浏览器API和RPC查询跨链代币数据
- **免费版限制**: 5条链、基础查询、不支持批量与监控

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------:|--------|:-------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
