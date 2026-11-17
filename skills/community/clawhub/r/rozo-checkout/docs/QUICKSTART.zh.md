# 快速开始

[English](QUICKSTART.md) | **简体中文** | [日本語](QUICKSTART.ja.md) | [Español](QUICKSTART.es.md)

用 Solana、BNB Chain、Ethereum、Polygon、Arbitrum、Base 或 Stellar 上的 USDT/USDC，用走
Lightning 的 BTC，或者用原生币（Ethereum、Base、Arbitrum 上的 ETH，BNB、SOL、POL），去支付一个 OpenRouter Coinbase 收款链接 (Payment Link)。五分钟搞定。
工作原理与设计理由见 [README.md](../README.md)。

## 一行命令搞定

```bash
npx @rozoai/checkout pay https://payments.coinbase.com/payment-links/pl_01YOURLINKID
```

这一条命令会替你跑完下面的每一步：选币、报价、创建订单、核对、确认、充值指令，然后一直轮询到结清。在选币那一步，你可以粘贴自己的钱包地址，它会去查余额并标出哪些币你付得起 —— 这是可选的，而且不会改变任何实际签名的内容。

如果你已经知道要用哪种币，直接指定就能跳过这一问：

```bash
npx @rozoai/checkout pay https://payments.coinbase.com/payment-links/pl_01YOURLINKID --with usdt-solana
```

`--with` 可选的币种有：`usdt-solana`、`usdc-solana`、`usdt-bnb`、`usdc-bnb`、`usdt-ethereum`、`usdc-ethereum`、`usdt-polygon`、`usdc-polygon`、`usdt-arbitrum`、`usdc-arbitrum`、`usdc-base`、`usdc-stellar`、`btc-lightning`，以及原生币 `eth-ethereum`、`eth-base`、`eth-arbitrum`、`bnb-bnb`、`sol-solana`、`pol-polygon`。脚本和 agent 必须显式传 `--with`：交互式选择只在终端里出现，而且没有默认币种。

原生币只有在这张账单的报价列出时才能用，账单上限 $3,500（Ethereum 上的 ETH 最低 $1）。原生币是精确到账（exact-out）：在币价锁定结束前（约 1 小时；OpenRouter 付款链接本身在创建后约 24 小时内都可支付）按显示的币数精确发送，并留一点同一种币付 gas。链上 BTC 和 Tron 不支持。Zcash 上的 ZEC（Beta）：请用 https://checkout.rozo.ai/zec，本 CLI 不创建 ZEC 订单。

默认情况下它只是打印一个地址，让你用任意钱包去付 —— 不需要私钥，也不需要任何配置。只有当你想让 CLI 改从热钱包签名时才加 `--send`；加 `--json` 输出机器可读格式。

本页剩下的内容就是同一套流程，只不过一步一步来 —— 如果出了问题，或者你想自己写脚本，那才需要看它们。

## 开始之前

- **Node 18 或更高版本**（`node -v`）。别的什么都不用装 —— `npx` 会去拉取 CLI，而克隆下来的
  `scripts/dist/*.js` 都是自包含的打包产物。
- **一个钱包**，在你选的链上持有你想用来付款的币种。
- **那个 Coinbase 链接**，例如
  `https://payments.coinbase.com/payment-links/pl_01YOURLINKID`。
- 不需要账号，也不需要 API key。这里用到的每个端点都是公开的。

先设一次：

```bash
LINK="https://payments.coinbase.com/payment-links/pl_01YOURLINKID"
```

链 id：`1` Ethereum · `56` BNB Chain · `137` Polygon · `8453` Base ·
`42161` Arbitrum · `900` Solana · `1500` Stellar · `lightning` Bitcoin Lightning。

## 我需要什么钱包？

**一个钱包、一条链就够了——不需要每条链各准备一个。**挑一种你已经持有的币，然后从它现在所在的地方付款即可。

任何钱包都可以，从交易所提币同样可以：下面的 Mode A 只是打印一段充值信息，你按其中给出的 `amount`、`tokenSymbol`、`chain`，把钱发到 `receiverAddress` 即可。全程不需要连接任何网站，也不需要在浏览器里做任何授权。实践中大家在 EVM 链上用 MetaMask 或 Rabby，在 Solana 上用 Phantom 或 Solflare，付 BTC 时用 Phoenix、Wallet of Satoshi 之类的闪电钱包。

有两种情况不一样。**Stellar** 走的是共享地址加 `receiverMemo` 的方式，所以你的付款来源必须能填写 memo——漏掉 memo，这笔钱就丢了。**闪电网络**付的是 `deposit.lnInvoice` 里的 BOLT11 invoice，没有可转账的地址。

只有 `--send`（Mode B）需要私钥，且仅支持 EVM 链和 Solana：Solana 直接用 `solana-keygen` 已经生成的 `~/.config/solana/id.json`，EVM 用加密的 keystore（口令交互式输入）。环境变量里的原始私钥保留给无人值守的自动化。

## 1. 报价（只读，免费）

```bash
node scripts/dist/quote.js --url "$LINK"
```

```json
{
  "success": true,
  "merchant": "OpenRouter, Inc.",
  "invoice": { "amount": "1050.00", "fiat": { "amount": "1050.00", "currency": "USD" } },
  "serviceFee": "10.5",
  "feeBps": 100,
  "callerPays": "1060.5",
  "coinbaseExpiryIso": "2026-08-09T10:00:00.000Z"
}
```

`"success": false` 且带 `LINK_NO_LONGER_PAYABLE`，说明这个链接已被付过或已过期 ——
去要一个新的，然后停止。

## 2. 创建订单

```bash
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT
```

这一步不动任何资金，未付款的订单会自然过期。订单约 1 小时到期，而 OpenRouter 付款链接在创建后约 24 小时内都可支付（`coinbaseExpiryIso`），所以订单过期后可以用同一条链接重新下单。完整充值地址 (deposit address) 在此阶段
会被**扣留** —— 你只拿到打码后的摘要，先用它核对。

```json
{
  "success": true,
  "rozoPaymentId": "11111111-2222-4333-8444-555555555555",
  "invoice": { "amount": "1050.000000", "currency": "USD" },
  "serviceFee": "10.5",
  "feeBps": 100,
  "callerPays": "1060.5",
  "deposit": null,
  "depositWithheld": true,
  "display": {
    "chain": "Solana",
    "amount": "1064.910000 USDT",
    "payToMasked": "9WzDXw...AWWM"
  },
  "expiry": { "effectiveDeadlineIso": "2026-08-08T11:00:00.000Z", "minutesOfSlack": 55 }
}
```

本例即旗舰场景：一张 **$1,050.00** 的账单，用于购买 $1,000 的 OpenRouter 额度。
任何不超过 **$1,100** 的账单都可以这样支付。

**继续之前务必核对 `display.amount`。** 它通常大于账单金额 —— 因为它包含了跨桥费用和
网络费用。记下 `rozoPaymentId`；后面每一条命令都要用它。

## 3. 确认

只有在你已经决定付款之后，才带上 `--confirm` 重新执行同一条命令：

```bash
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT --confirm
```

这会释放完整的充值详情，并记录下发送脚本所需的那条确认。

```json
{
  "success": true,
  "confirmed": true,
  "deposit": {
    "chain": "Solana",
    "tokenSymbol": "USDT",
    "receiverAddress": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
    "receiverMemo": "rozo-901",
    "amount": "1054.410000",
    "payTo": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
  }
}
```

严格按这个信息块给出的字段来发送。Stellar 上的 memo 即使看起来是纯数字，也**始终是 `MEMO_TEXT`** —— 按 `MEMO_ID` 发送不会被匹配上。`deposit.expiresIn` 会告诉你订单还有多久过期。对于 Lightning，`deposit.lnInvoice` 里是供扫码的
BOLT11 字符串，`deposit.amount` 的单位是聪 (satoshis)。

## 4. 付款

### 最简单的方式：用你自己的钱包

**无需私钥、无需环境变量、无需任何配置。** 打开任意一个钱包，严格按上面那个
`deposit` 信息块所写的去发送：

- `amount` 数量的 `tokenSymbol`，
- 在 `chain` 这条链上，
- 发往 `receiverAddress` —— 从 JSON 里复制，绝不要手打重输。

如果这个信息块里还有别的字段，比如 `receiverMemo`，就原样一并带上；在那条链上它属于
地址的一部分。对于 Lightning，改为扫码或粘贴 `deposit.lnInvoice`。

模式 A 到这里就全部结束了。直接跳到第 5 步。

### 可选的方式：让脚本替你付（模式 B）

只有当你想让这台机器替你签名时才需要，而且**只支持 EVM 链和 Solana** —— Stellar 和
闪电网络没有 `--send`，只能用你自己的钱包付。这是整个流程里唯一需要私钥的部分。

**Solana —— 直接用你已有的密钥对。** 只要你跑过 `solana-keygen`，
`~/.config/solana/id.json` 就已经存在，脚本会自动使用它：

```bash
node scripts/dist/send-sol.js --rozo-payment-id <rozoPaymentId> --send
```

**EVM —— 用加密的 keystore。** 从你的钱包导出一个 V3 JSON keystore 并指向它。
口令 (passphrase) 会交互式提示输入，永远不会作为命令行参数传递：

```bash
ROZO_CHECKOUT_EVM_KEYSTORE=~/wallets/hot.json \
  node scripts/dist/send-evm.js --rozo-payment-id <rozoPaymentId> --send
```

两种文件也都可以用 `--keyfile <path>` 显式指定；`--dry-run` 对所有来源都有效：
它会推导出地址并跑完所有检查，但不签任何名。

**用于无人值守的自动化**（没有人能输入口令的场景），环境变量里的原始私钥依然照旧
可用 —— `ROZO_CHECKOUT_SOL_KEY` 或 `ROZO_CHECKOUT_EVM_KEY`，或者配合 keystore 使用
`ROZO_CHECKOUT_KEYSTORE_PASSPHRASE`。在有人使用的机器上，优先用密钥文件。

这些设置也可以放在你运行命令所在目录的 `.env` 里（或者用 `--env-file <path>` 指定）。
其中只有 `ROZO_CHECKOUT_*` 开头的键会被读取，文件按纯文本解析、绝不交给 shell 执行，
而且真实环境变量优先级更高。**记得把 `.env` 加进 `.gitignore`。**

密钥文件和 `.env` 都不能被其他用户读取（`chmod 600`），也不能被 git 跟踪。这两种情况都会被
直接拒绝，而不是只给个警告。

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

单笔付款不得超过 **$1,100**；超过就按上面的方式用你自己的钱包付。

```json
{
  "success": true,
  "submitted": true,
  "confirmed": true,
  "txHash": "3Bxs4h24hBjHziQ8UJqSjqjbjWQq2sQ3yV9Fq4HrVh5c"
}
```

## 5. 观察结清

```bash
node scripts/dist/status.js --rozo-payment-id <rozoPaymentId> --watch --timeout 600
```

```json
{
  "success": true,
  "state": "settled",
  "terminal": true,
  "payin": { "txHash": "3Bxs4h24...", "confirmedAt": "2026-08-08T10:05:00.000Z" }
}
```

状态流转依次为 `awaiting_deposit` → `payin_detected` → `payin_confirmed` →
`bridging` → `paying_coinbase` → `settled`。你的链上交易被确认**并不**代表结束：
要一直轮询到 `settled` 为止。

## 出问题时

读 `error.code`。最可能遇到的三个：

| `error.code` | 发生了什么 | 该怎么办 |
|---|---|---|
| `LINK_NO_LONGER_PAYABLE` | 这个链接已经被别人付过，或者已过期 | 找商家要一个新链接；不要付任何钱 |
| `EXPIRY_MARGIN` | 剩余时间太短，不足以安全完成充值、跨桥和结清 | 不要给这个订单充值；等它过期后，用同一个链接从第 1 步重新开始（确认旧订单未收到付款后会生成新订单）。如果返回 `LINK_USED_OR_EXPIRED`，或 `PAYMENT_EXPIRED` 且 `confirmed: true`，就找商家要一个新链接 |
| `ALREADY_SENT` | 这个订单已经记录过一次发送 | **不要**再发一次；先跑 `status.js` 并去链上核对 |

**只要已经有钱离开了你的钱包，就绝不要再付一次。** 保留好 `linkId`、
`rozoPaymentId` 和每一个交易 hash，找人来做对账。向一个一次性充值地址付第二笔款，
并不保证会被入账。

完整的错误码表在 [README.md](../README.md)，面向 agent 的指令在 [SKILL.md](../SKILL.md)。
