# rozo-checkout

[English](../README.md) | **简体中文** | [日本語](README.ja.md) | [Español](README.es.md)

用一种 **OpenRouter Coinbase 收款链接 (Payment Link)** 本身收不了的币去付款 —— 走
闪电网络的 BTC，Solana、BNB Chain、Ethereum、Polygon、Arbitrum、Base、Stellar 上的
USDT/USDC，或者原生币：Ethereum、Base、Arbitrum 上的 ETH，以及 BNB、SOL、POL。Coinbase 收款链接只接受 Base 上的 USDC；本工具把你实际持有的币通过
一座桥路由过去，再由一个出资钱包代你结清账单。无需账号、无需 API key、无需浏览器。

```bash
npx @rozoai/checkout pay <coinbase-link>
```

它会先问你想用哪种币付款 —— 在提示处粘贴你的钱包地址，它就会标出哪些币你余额
够付 —— 然后打印一个充值地址，你用任意钱包付进去即可 —— **不需要私钥、不需要
环境变量、不需要任何配置**。之后它会一直等到账单被结清。

已经知道要用哪种币？直接跳过这一问：

```bash
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

## 可用于付款的币种

| 链 | `--with` | 链 id | 备注 |
|---|---|---|---|
| Ethereum | `usdt-ethereum` `usdc-ethereum` | `1` | 6 位小数 |
| BNB Chain | `usdt-bnb` `usdc-bnb` | `56` | 18 位小数 |
| Polygon | `usdt-polygon` `usdc-polygon` | `137` | 6 位小数 |
| Arbitrum | `usdt-arbitrum` `usdc-arbitrum` | `42161` | 6 位小数 |
| Base | `usdc-base` | `8453` | 6 位小数 |
| Solana | `usdt-solana` `usdc-solana` | `900` | SPL |
| Stellar | `usdc-stellar` | `1500` | 必须带 `MEMO_TEXT` memo —— 会在充值信息块里给出 |
| Bitcoin Lightning | `btc-lightning` | `lightning` | BOLT11；金额单位为聪 |

**原生币**，各自只在自己的链上：

| 币 | `--with` | 链 id | 备注 |
|---|---|---|---|
| Ethereum 上的 ETH | `eth-ethereum` | `1` | 18 位小数（wei）；最低 $1 |
| Base 上的 ETH | `eth-base` | `8453` | 18 位小数（wei） |
| Arbitrum 上的 ETH | `eth-arbitrum` | `42161` | 18 位小数（wei） |
| BNB | `bnb-bnb` 或 `bnb` | `56` | 18 位小数 |
| SOL | `sol-solana` 或 `sol` | `900` | 9 位小数（lamports） |
| POL | `pol-polygon` 或 `pol` | `137` | 18 位小数 |

只有当这张账单的报价列出某个原生币时才能用它（`quote` 会显示），且账单不超过 $3,500。原生币订单是**精确到账（exact-out）**，和闪电网络一样：按充值信息块里的币数一分不差地发送。币价只锁定到显示的时间（约 1 小时，OpenRouter 付款链接本身在创建后约 24 小时内都可支付）；过了这个时间就不要再发，让订单过期后重新下单。币数里在服务费之外还含汇率价差，钱包里还需要多留一点同一种币付网络费。从交易所提币时，到账金额必须是完整金额：确认提币手续费没有从中扣除。`--send` 也能付原生币，按精确金额做一笔普通转账。

链上 BTC 和 Tron 不支持。
Zcash 上的 ZEC（Beta）：请用 https://checkout.rozo.ai/zec，本 CLI 不创建 ZEC 订单。

## 我需要什么钱包？

**一个钱包、一条链就够了——不需要每条链各准备一个。**从上面挑一种你已经持有的币，然后从它现在所在的地方付款即可。

- **任何钱包都可以，从交易所提币同样可以。**默认路径只是打印一段充值信息：按其中给出的 `amount`、`tokenSymbol`、`chain`，把钱发到 `receiverAddress` 即可。全程不需要连接任何网站，也不需要在浏览器里做任何授权。实践中大家在 EVM 链上用 MetaMask 或 Rabby，在 Solana 上用 Phantom 或 Solflare，付 BTC 时用 Phoenix、Wallet of Satoshi 之类的闪电钱包。
- **Stellar 是需要特别小心的那一条。**它的充值走的是共享地址加 `receiverMemo` 的方式，所以无论你从交易所还是钱包发出，都必须能填写 memo。漏掉 memo，这笔钱就丢了。
- **闪电网络付的是一张 invoice，不是地址。**扫描或粘贴 `deposit.lnInvoice` 即可，这条路径上没有可转账的地址。
- **只有 `--send` 需要私钥**，从 `ROZO_CHECKOUT_EVM_KEY` 或 `ROZO_CHECKOUT_SOL_KEY` 读取，且仅支持 EVM 链和 Solana。其余方式都不涉及私钥。

## 在你的 agent 里使用

不管用哪个 agent，喂给它的东西都一样：上面那条命令，或者直接让它读
[llms.txt](../llms.txt)。**用你自己的钱包付款永远不需要私钥。** 只有可选的
`--send` 才会在本地签名，也只有它会读取 `ROZO_CHECKOUT_EVM_KEY` /
`ROZO_CHECKOUT_SOL_KEY`。

<details>
<summary><b>Claude Code</b> —— 安装 skill，或者直接粘贴那条命令</summary>

本仓库本身就是一个 Claude Code skill：它自带 `SKILL.md` 和 `scripts/dist/` 里的
可执行文件。把它克隆到你的 skills 目录，Claude Code 会自动识别。

```bash
git clone https://github.com/RozoAI/rozo-checkout-skill ~/.claude/skills/rozo-checkout
```

或者跳过安装，直接让它执行：

```
用 Solana 上的 USDT 支付这个 OpenRouter 链接：
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

钱包：任意钱包，**无需私钥**。只有当你想让 Claude 用热钱包签名时才加 `--send`（用你的 Solana CLI 密钥对或加密 keystore），
那一步才需要环境变量里的私钥。
</details>

<details>
<summary><b>Codex CLI</b> —— 写进 AGENTS.md，或者直接跑</summary>

Codex 会读取项目根目录的 `AGENTS.md`。加一条常驻指令，它就不用每次都被告知怎么付：

```
要支付 OpenRouter / Coinbase 收款链接，执行：
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

钱包：任意钱包，**无需私钥**。只有 `--send` 需要，它用你的 Solana CLI 密钥对或加密 keystore 在本地签名；仅支持 EVM 链和 Solana —— Stellar 与闪电网络只能用模式 A。
</details>

<details>
<summary><b>OpenCode</b> —— 写进 AGENTS.md，或者直接跑</summary>

OpenCode 同样读取项目根目录的 `AGENTS.md`，所以上面那段 Codex 的写法可以原样照搬。
最短的路径依然是直接执行命令本身：

```bash
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

钱包：任意钱包，**无需私钥**。只有 `--send` 需要，它用你的 Solana CLI 密钥对或加密 keystore 在本地签名。
</details>

<details>
<summary><b>Cline</b> —— 写进 .clinerules，或者直接跑</summary>

Cline 从项目根目录的 `.clinerules` 读取常驻指令：

```
要支付 OpenRouter / Coinbase 收款链接，执行：
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

钱包：任意钱包，**无需私钥**。只有 `--send` 需要，它用你的 Solana CLI 密钥对或加密 keystore 在本地签名。
</details>

<details>
<summary><b>Cursor</b> —— 写进 .cursor/rules，或者直接跑</summary>

在 `.cursor/rules/rozo-checkout.mdc` 加一条项目规则：

```
要支付 OpenRouter / Coinbase 收款链接，执行：
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

钱包：任意钱包，**无需私钥**。只有 `--send` 需要，它用你的 Solana CLI 密钥对或加密 keystore 在本地签名。
</details>

<details>
<summary><b>Hermes Agent</b> —— 在会话里跑那条命令</summary>

Hermes Agent（Nous Research）有 shell 权限，也有自己的 skill 体系。用 `hermes`
启动后这样说：

```
先抓取 https://checkout.rozo.ai/llms.txt，然后支付这个 OpenRouter 链接：
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

钱包：任意钱包，**无需私钥**。只有 `--send` 需要，它用你的 Solana CLI 密钥对或加密 keystore 在本地签名。
</details>

<details>
<summary><b>OpenClaw</b> —— openclaw agent exec</summary>

OpenClaw 的无头入口用来跑一次性任务，很适合从脚本或聊天渠道里触发一笔付款：

```bash
openclaw agent exec "Pay this OpenRouter link with USDT on Solana by running: npx @rozoai/checkout pay <coinbase-link> --with usdt-solana"
```

钱包：任意钱包，**无需私钥**。只有 `--send` 需要，它用你的 Solana CLI 密钥对或加密 keystore 在本地签名。
</details>

<details>
<summary><b>Pi</b> —— 在会话里跑那条命令</summary>

Pi 是一个 BYOK 终端 agent，内置工具里就有 `bash`，可以直接执行命令。用 `pi`
启动后这样说：

```
用 Solana 上的 USDT 支付这个 OpenRouter 链接，执行：
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

钱包：任意钱包，**无需私钥**。只有 `--send` 需要，它用你的 Solana CLI 密钥对或加密 keystore 在本地签名。
</details>

<details>
<summary><b>终端 —— 完全不用 agent</b> —— 一步步跑脚本</summary>

每一步都自己来。打包产物是自包含的，除了 Node 18+ 之外不需要装任何东西。

```bash
git clone https://github.com/RozoAI/rozo-checkout-skill && cd rozo-checkout-skill
LINK="https://payments.coinbase.com/payment-links/pl_01YOURLINKID"

# 只读报价，不产生任何费用
node scripts/dist/quote.js --url "$LINK"

# 创建订单。此阶段完整充值地址会被扣留：你先拿到一份打码后的摘要用于核对。
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT

# 决定付款之后，加 --confirm 重新执行同一条命令来释放它
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT --confirm

# 用任意钱包按充值信息块付款，然后观察它结清
node scripts/dist/status.js --rozo-payment-id <uuid> --watch
```

每个脚本在 stdout 上只打印一个 JSON 对象。退出码 `0` 表示成功，`1` 表示被拒绝/
失败（读 `error.code`），`2` 表示用法错误，`3` 表示已提交但未确认。完整走一遍：
[QUICKSTART](QUICKSTART.zh.md)。

钱包：任意钱包，**无需私钥**。热钱包发送见 `send-evm.js` / `send-sol.js`，它们读取
`ROZO_CHECKOUT_EVM_KEY` / `ROZO_CHECKOUT_SOL_KEY`。agent 和脚本必须显式传 `--with`：
交互式选择只在终端里出现，而且刻意没有默认币种。
</details>

<details>
<summary><b>任何其他 agent</b> —— 让它去读 llms.txt</summary>

只要一个 agent 能抓 URL、能执行命令，它就能干这件事：

```
把 https://checkout.rozo.ai/llms.txt 抓进你的上下文，然后照着它
支付这个 OpenRouter 链接：<coinbase-link>
```

如果 agent 没有 shell 但能发 HTTP 请求，它可以直接调用那四个公开端点 —— 见
[工作原理](how-it-works.md)。

钱包：任意钱包，**无需私钥**。只有 `--send` 需要，它用你的 Solana CLI 密钥对或加密 keystore 在本地签名。
</details>

<details>
<summary><b>为 <code>--send</code> 配置本地钱包</b> —— .env 模板与各钱包导出步骤</summary>

你很可能完全不需要这些：默认路径不需要任何私钥；Stellar 来源可用 `stellar-agent-wallet` skill，它有自己的密钥管理来完成发送 —— 这份 `.env` 配置只用于无人值守的 EVM/Solana 自动化，且应使用余额很低的专用热钱包。

**默认路径不需要这里的任何东西。** 用你自己的钱包付款既不需要私钥也不需要任何配置，
而且支持那些在这里根本用不了的钱包 —— 包括硬件钱包和交易所账户。

在你运行命令的目录放一个 `.env`，下面列出了本工具会读取的全部变量：

```bash
# 用你自己的钱包付款不需要下面任何一项。它们只在你使用 --send 时才被读取。

# Solana 私钥：base58 字符串，或 JSON 字节数组。只有在你没有
# ~/.config/solana/id.json（它会被自动识别）时才需要填。
ROZO_CHECKOUT_SOL_KEY=REPLACE_ME_base58_secret_key

# EVM 原始私钥：0x 加 64 位十六进制。这是最不安全的方式 —— 优先用下面的 keystore。
ROZO_CHECKOUT_EVM_KEY=0x0000000000000000000000000000000000000000000000000000000000000000

# EVM 加密 V3 keystore：文件路径。比上面的原始私钥更推荐。
ROZO_CHECKOUT_EVM_KEYSTORE=/replace/me/keystores/my-hot-wallet

# 该 keystore 的口令。只在无人值守时需要；在终端上会交互式提示，且不会被保存。
ROZO_CHECKOUT_KEYSTORE_PASSPHRASE=REPLACE_ME_not_a_real_passphrase

# 可选的 RPC 覆盖，按链 id 一条。8453 = Base，900 = Solana。
ROZO_CHECKOUT_RPC_8453=https://mainnet.base.org
ROZO_CHECKOUT_RPC_900=https://api.mainnet-beta.solana.com
```

然后锁好权限，并确保它不进 git：

```bash
chmod 600 .env
echo '.env' >> .gitignore
```

**Solana**

- `solana-keygen new` 会写出 `~/.config/solana/id.json`。什么都不用配 —— 它会被自动
  找到。这是我们推荐的方式。
- **Phantom** → Settings → Export Private Key 给出的是 **base58** 字符串，填进
  `ROZO_CHECKOUT_SOL_KEY`。
- **Solflare** 新版本导出 base58 字符串，旧版本导出 JSON 字节数组。两种都可以直接用。

**EVM**

- **MetaMask** 和 **Rabby** → 导出私钥给出的是 64 位十六进制字符串。直接原样粘贴到
  `ROZO_CHECKOUT_EVM_KEY` 即可；`0x` 前缀加不加都行。
- **加密 keystore（更安全）。** 浏览器钱包只能导出原始私钥，不能导出 keystore。
  想把私钥变成加密 keystore，可以用 Foundry：`cast wallet import my-hot-wallet
  --interactive` 会提示你输入私钥，并把加密的 V3 keystore 写到
  `~/.foundry/keystores/my-hot-wallet`（用 `--keystore-dir` 可改目录）。然后把
  `ROZO_CHECKOUT_EVM_KEYSTORE` 指向该文件。`geth account import` 同样会生成 V3 keystore。

**不能用于 `--send` 的钱包：** 硬件钱包（Ledger、Trezor）、只支持 WalletConnect 的
手机钱包，以及交易所账户。它们在设计上就不会交出签名私钥。这类用户请走默认的无私钥
路径 —— 那条路对它们全都适用。

</details>

## 三条必须知道的规则

- **充值地址是一次性的。** 绝不要复用旧订单、缓存响应或截图里的地址。
- **严格按显示的金额发送。** 它通常比账单金额大 —— 因为包含了跨桥费和网络费。
- **绝不要对已入账的订单二次付款。** 一旦检测到已有付款，就停下来找人工核对；
  再往一个一次性地址打第二笔钱，不保证能被记账。

它拒绝去做哪些事、以及为什么，完整清单见
[docs/safety.md](safety.md)。

## 相关链接

- [快速开始](QUICKSTART.zh.md) —— 五条命令，附预期输出
- [工作原理](how-it-works.md) —— 流程、端点、标识符
- [安全设计](safety.md) —— 每一道防线的细节
- [SKILL.md](../SKILL.md) —— 面向 agent 的指令 · [llms.txt](../llms.txt) —— 单文件摘要
- [checkout.rozo.ai/agent](https://checkout.rozo.ai/agent.html) —— 网页版，同样的东西
- [Issues](https://github.com/RozoAI/rozo-checkout-skill/issues) —— bug 与需求

## 更新日志

- **0.1.3** —— 第一笔真实付款暴露出来的问题修复。构建产物在 Node 22+ 上不再因
  `__filename is not defined` 崩溃（esbuild banner 现在同时注入 `__filename`/`__dirname`
  和 `require`，并且测试会真正执行每一个构建产物）。Stellar 充值现在会明确标出 memo
  类型（`MEMO_TEXT`，即使 memo 看起来是纯数字）。订单在充值信息块和 `status` 里都会以
  时长显示剩余有效期（"expires in 47m"），过期时给出重新下单的完整命令。复用已有的未付
  订单、以及所选币种与已有订单不一致这两种情况，现在都会被解释清楚，而不是看起来像报错。
- **0.1.2** —— 模式 B 不再需要把原始私钥放进环境变量。Solana 直接用 `solana-keygen`
  已经写好的 `~/.config/solana/id.json`；EVM 用加密的 V3 keystore，口令交互式提示输入。
  `--keyfile` 可以显式指定其中任一种，相关设置也可以放进已 gitignore 的 `.env`。
  环境变量里的原始私钥仍然可用于无人值守的自动化。密钥文件和 `.env` 必须
  `chmod 600` 且不被 git 跟踪。
- **0.1.1** —— 两条额度上限合并为一条：单笔付款不得超过 $1,100（按购买 $1,000
  额度加 5% 手续费来设定），单会话累计上限与 `--yes-large` 绕过开关均已移除。文档
  明确说明：用你自己的钱包付款不需要私钥，也不需要任何配置。
- **0.1.0** —— 首个版本：`npx @rozoai/checkout`。

## 许可证

MIT。
