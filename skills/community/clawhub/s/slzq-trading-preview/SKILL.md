---
name: slzq-trading
version: 1.2.8
description: 三立期货「三立智期」官方技能：对话领取模拟盘密钥，查行情与持仓，模拟盘可下单；问是否正规、开户也可答。实盘请去 App 复制密钥。
author: sanli
triggers:
  - 期货
  - 下单
  - 持仓
  - 委托
  - 撤单
  - 行情
  - K线
  - 黄金
  - 铜
  - 合约
  - 三立智期
  - 三立期货
  - 模拟盘
  - 实盘
  - 开户
  - 正规
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "primaryEnv": "SLZQ_OPENCLAW_API_KEY",
        "envVars":
          [
            {
              "name": "SLZQ_OPENCLAW_API_KEY",
              "required": false,
              "description": "三立智期 OpenClaw API Key。可在 App「我的 → 期货辅助交易」生成；留空时可在会话中用手机号领取模拟盘密钥。"
            },
            {
              "name": "SLZQ_OPENCLAW_DOMAIN",
              "required": false,
              "description": "API 域名，仅 https:// + 主机名，不要带 /mobile-api。默认 https://slzqapi.sxslqhsh.com"
            },
            {
              "name": "SLZQ_OPENCLAW_ENV",
              "required": false,
              "description": "交易环境。sim=模拟盘（默认），live=实盘。"
            }
          ]
      }
  }
config:
  - key: SLZQ_OPENCLAW_API_KEY
    description: 三立智期 OpenClaw API Key。可在 App「我的 → 期货辅助交易」生成；留空时可在会话中用手机号领取模拟盘密钥。
    required: false
  - key: SLZQ_OPENCLAW_DOMAIN
    description: API 域名，仅 https:// + 主机名，不要带 /mobile-api。默认生产环境 https://slzqapi.sxslqhsh.com
    required: false
    default: https://slzqapi.sxslqhsh.com
  - key: SLZQ_OPENCLAW_ENV
    description: 交易环境。sim=模拟盘（默认），live=实盘（需已在 App 绑定 CTP 凭据）。
    required: false
    default: sim
references:
  - references/usage-notes.md
  - references/company-faq.md
  - references/openapi.yaml
  - references/api.md
---

# 三立智期

山西三立期货有限公司官方「三立智期」量化技能。在 OpenClaw 里查询期货行情与账户，并支持模拟盘交易。

> **智能体：先完整阅读 [references/usage-notes.md](./references/usage-notes.md)。** 领钥、下单等操作规则都在使用须知里。

## 能做什么

- 用手机号在对话里领取 **模拟盘** 密钥（先展示风险告知，同意后再发验证码）
- 查询行情、K 线、持仓、委托、成交
- 模拟盘下单与撤单
- **推荐注册 MCP** 后使用（工具更稳，密钥自动保存）
- 说明三立期货是否正规、如何开户（依据包内资料，不上网搜索）
- 实盘：请先在 **三立智期 App → 我的 → 期货辅助交易** 生成带实盘权限的密钥再使用

模拟盘不进交易所；实盘走期货柜台，与 App 同一资金账号。期货交易有风险，本技能不提供投资建议。

## 怎么用（ClawHub）

两种安装方式都可以。

**方式 A（推荐）**：一次装完，不会卡在黄框上。

```text
openclaw skills install @sqringwang/slzq-trading-preview --acknowledge-clawhub-risk
```

**方式 B**：短命令，效果相同，但安装过程中可能要你再确认一次。

```text
openclaw skills install slzq-trading-preview
```

若方式 B 弹出黄色警告（`suspicious` / Security scan is not clean），并提示 `Install cancelled` 或要你输入技能名：

- **不是木马**，ClawHub 也没有把它标成 malicious（恶意）。
- **原因**：本技能会读取 API 密钥、访问三立接口，模拟盘和实盘都可以下单/撤单。商店扫描把这类「能碰资金」的能力标成可疑，OpenClaw 默认拦住，让你先看一眼再继续。
- **怎么继续**：按提示输入 `@sqringwang/slzq-trading-preview`，或改用上面的方式 A。细节可到技能页 **Security details** 查看。

`--acknowledge-clawhub-risk` 只表示你已知悉上述扫描结果并愿意安装，不是跳过杀毒或关闭安全检查。

装完技能后，请继续 **注册 MCP**（见下一节），然后 **新开一个对话**，直接说「查热门行情」或「我要用三立智期模拟盘」。

没有密钥时，智能体会同时给出：

1. **会话内领取**（手机号 + 短信，仅模拟盘）
2. **去 App 复制**（已有密钥或要用实盘时）

## 注册 MCP（强烈推荐）

MCP 是本技能的主路径：行情、持仓、下单更稳，会话里领到的密钥会自动保存，不必每次手填。装完技能后请马上注册。

在技能安装目录执行：

```text
node install/setup-clawhub.mjs
```

MCP 入口是本包里的 `runtime/mcp/dist/index.js`。脚本会尝试写入 OpenClaw；成功后请 **完全退出并重启客户端**，再新开对话。也可以在对话里直接说「帮我注册三立智期 MCP」，智能体会协助。

暂时没装 MCP 也能用对话 + HTTP 领钥和查询；但查账户、下单请尽快补上 MCP。

## 关于我们

本技能对接 **山西三立期货有限公司**（1993 年成立，经中国证监会批准，山西省唯一一家期货公司）。官网 https://www.sxslqh.com/ ，客服 400-098-6699。资质请到官网「走进三立 → 信息公示」及中国期货业协会公示自行核验。
