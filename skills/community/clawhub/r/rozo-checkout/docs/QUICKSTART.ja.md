# クイックスタート

[English](QUICKSTART.md) | [简体中文](QUICKSTART.zh.md) | **日本語** | [Español](QUICKSTART.es.md)

OpenRouter の Coinbase 決済リンク (Payment Link) を、Solana、BNB Chain、
Ethereum、Polygon、Arbitrum、Base、Stellar 上の USDT/USDC、Lightning 経由の BTC、またはネイティブコイン（Ethereum・Base・Arbitrum の ETH、BNB、SOL、POL）で支払います。所要 5 分。
仕組みと設計意図については [README.md](../README.md) を参照してください。

## ワンライナー

```bash
npx @rozoai/checkout pay https://payments.coinbase.com/payment-links/pl_01YOURLINKID
```

これ 1 つで、以下の全ステップを実行します。通貨の選択、見積もり、注文作成、確認、承認、
入金手順の表示、そして決済完了までのポーリングです。通貨を選ぶ場面でウォレットアドレスを
貼り付けると、残高を調べてどの通貨なら支払えるかを表示します。これは任意で、実際に署名
される内容は一切変わりません。

使う通貨が決まっている場合は、指定すればこの質問を省略できます:

```bash
npx @rozoai/checkout pay https://payments.coinbase.com/payment-links/pl_01YOURLINKID --with usdt-solana
```

`--with` に指定できる通貨: `usdt-solana`、
`usdc-solana`、`usdt-bnb`、`usdc-bnb`、`usdt-ethereum`、`usdc-ethereum`、
`usdt-polygon`、`usdc-polygon`、`usdt-arbitrum`、`usdc-arbitrum`、`usdc-base`、`usdc-stellar`、`btc-lightning`、
ネイティブコインの `eth-ethereum`、`eth-base`、`eth-arbitrum`、`bnb-bnb`、`sol-solana`、`pol-polygon`。
スクリプトやエージェントでは必ず `--with` を渡してください。対話式の選択は端末でのみ
表示され、既定の通貨はありません。

ネイティブコインは、インボイスの見積もりに含まれている場合のみ使えます（上限 $3,500、Ethereum の ETH は最低 $1）。
受取額固定（exact-out）なので、表示された数量を価格固定の期限（約 1 時間。OpenRouter の支払いリンク自体は作成から約 24 時間支払い可能です）までに正確に送り、ガス代として同じコインを少し残してください。
オンチェーンの BTC と Tron には対応していません。
Zcash の ZEC（Beta）は https://checkout.rozo.ai/zec を使ってください。この CLI では ZEC の注文は作れません。

既定では、任意のウォレットから支払うためのアドレスを表示するだけです — 鍵も設定も
不要です。CLI にホットウォレットから署名させたい場合にだけ `--send` を、機械可読な
出力が必要な場合は `--json` を追加してください。

このページの残りは、同じフローを 1 ステップずつ実行するものです。うまくいかないときや、
自分でスクリプトを書くときは、こちらが必要になります。

## 始める前に

- **Node 18 以降**（`node -v`）。ほかにインストールするものはありません — `npx` が CLI を
  取得しますし、クローンした `scripts/dist/*.js` は自己完結型のバンドルです。
- 選んだチェーン上で、支払いたい通貨を保有している**ウォレット**。
- **Coinbase のリンク**。例:
  `https://payments.coinbase.com/payment-links/pl_01YOURLINKID`。
- アカウントも API キーも不要です。ここで使うエンドポイントはすべて公開です。

最初に一度だけ設定します:

```bash
LINK="https://payments.coinbase.com/payment-links/pl_01YOURLINKID"
```

チェーン id: `1` Ethereum · `56` BNB Chain · `137` Polygon · `8453` Base ·
`42161` Arbitrum · `900` Solana · `1500` Stellar · `lightning` Bitcoin Lightning。

## どのウォレットが必要ですか？

**ウォレットは 1 つ、チェーンも 1 つで足ります — チェーンごとに用意する必要はありません。**すでに持っている通貨を選び、それが今ある場所から支払ってください。

どのウォレットでも構いませんし、取引所からの出金でも構いません。下記の Mode A は入金情報を表示するだけで、示された `amount` の `tokenSymbol` を、その `chain` 上で `receiverAddress` へ送るだけです。どのサイトに接続することも、ブラウザで承認することもありません。実際には、EVM チェーンでは MetaMask や Rabby、Solana では Phantom や Solflare、BTC では Phoenix や Wallet of Satoshi といった Lightning ウォレットがよく使われています。

異なるケースが 2 つあります。**Stellar** は共有アドレスと `receiverMemo` の組み合わせで振り分けられるため、送信元で memo を設定できる必要があります。memo を省くと、その支払いは失われます。**Lightning** は `deposit.lnInvoice` にある BOLT11 インボイスに支払います。送金先アドレスというものはありません。

鍵が必要なのは `--send`（Mode B）だけで、対象は EVM チェーンと Solana のみです。Solana では `solana-keygen` が既に作成した `~/.config/solana/id.json` を、EVM では暗号化された keystore（パスフレーズは対話的に入力）を使います。環境変数の生の鍵は無人自動化向けに残されています。

## 1. 見積もりを取得する（読み取り専用、無料）

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

`"success": false` かつ `LINK_NO_LONGER_PAYABLE` の場合、そのリンクは使用済みか
期限切れです — 新しいリンクを依頼し、そこで中止してください。

## 2. 注文を作成する

```bash
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT
```

資金は動かず、入金のない注文はそのまま期限切れになります。注文の有効期限は約 1 時間ですが、OpenRouter の支払いリンクは作成から約 24 時間支払い可能です（`coinbaseExpiryIso`）。注文が期限切れになっても、同じリンクで新しい注文を作れます。この段階では完全な
入金アドレス (deposit address) は**伏せられます** — まず確認用にマスクされたサマリーが返ります。

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

この例は代表的なケースです。$1,000 分の OpenRouter クレジットに対する **$1,050.00**
のインボイスです。**$1,100** までのインボイスであれば同じ方法で支払えます。

**先へ進む前に必ず `display.amount` を確認してください。** 通常はインボイス金額より
大きくなります — ブリッジ (bridge) 手数料とネットワーク手数料が含まれるためです。`rozoPaymentId` を
控えておいてください。以降のコマンドはすべてこれを使います。

## 3. 確認する

支払うと決めたときにだけ、同じコマンドを `--confirm` 付きで実行し直してください:

```bash
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT --confirm
```

これで完全な入金詳細が開示され、送金スクリプトが要求する確認記録が残ります。

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

このブロックが示すフィールドを、そのとおりに送金してください。Lightning の場合、
Stellar の memo は数字に見えても**常に `MEMO_TEXT`** です — `MEMO_ID` として送ると一致しません。`deposit.expiresIn` に残りの有効時間が出ます。
`deposit.lnInvoice` にスキャン用の BOLT11 文字列が入り、`deposit.amount` は
satoshi 単位になります。

## 4. 支払う

### 簡単な方法: 自分のウォレットから

**秘密鍵も環境変数も設定も一切不要です。** 好きなウォレットを開き、上の `deposit`
ブロックが示すとおりに送金してください:

- `tokenSymbol` を `amount` だけ、
- `chain` の上で、
- `receiverAddress` へ — JSON からコピーし、決して手入力し直さないでください。

ブロックに `receiverMemo` などそれ以外のフィールドが含まれている場合は、示されたとおりに
そのまま付けてください。それはそのチェーンにおけるアドレスの一部です。Lightning の場合は
代わりに `deposit.lnInvoice` をスキャンするか貼り付けてください。

モード A はこれで全部です。ステップ 5 へ進んでください。

### 任意の方法: スクリプトに支払わせる（モード B）

このマシンに署名させたい場合のみで、対象は **EVM チェーンと Solana だけ**です。Stellar と
Lightning に `--send` はなく、自分のウォレットから支払います。鍵が必要なのはこの部分だけです。

**Solana — すでにある鍵ペアをそのまま使います。** `solana-keygen` を一度でも実行して
いれば `~/.config/solana/id.json` が既に存在し、自動的に使われます:

```bash
node scripts/dist/send-sol.js --rozo-payment-id <rozoPaymentId> --send
```

**EVM — 暗号化された keystore を使います。** ウォレットから V3 形式の JSON keystore を
書き出し、それを指定してください。パスフレーズは対話的に尋ねられ、フラグとして渡す
ことは決してありません:

```bash
ROZO_CHECKOUT_EVM_KEYSTORE=~/wallets/hot.json \
  node scripts/dist/send-evm.js --rozo-payment-id <rozoPaymentId> --send
```

どちらのファイルも `--keyfile <path>` で明示的に指定できます。`--dry-run` はすべての
取得元で機能し、アドレスを導出してすべてのチェックを実行しますが、署名は行いません。

**無人自動化の場合**（パスフレーズを入力できる人がいない場合）は、環境変数の生の鍵が
これまでどおり使えます — `ROZO_CHECKOUT_SOL_KEY` または `ROZO_CHECKOUT_EVM_KEY`、
あるいは keystore と併せて `ROZO_CHECKOUT_KEYSTORE_PASSPHRASE` です。人が使うマシンでは
鍵ファイルを優先してください。

これらの設定は、実行するディレクトリの `.env` に置くこともできます（`--env-file <path>`
でも指定できます）。読み込まれるのは `ROZO_CHECKOUT_*` のキーだけで、ファイルはテキスト
として解析され、シェルで評価されることは決してありません。実際の環境変数のほうが優先
されます。**`.env` は `.gitignore` に追加してください。**

鍵ファイルと `.env` は他のユーザーから読めてはならず（`chmod 600`）、git で追跡されて
いてもいけません。どちらの場合も警告ではなく拒否されます。

<details>
<summary><b><code>--send</code> 用のローカルウォレット設定</b> — .env テンプレートとウォレット別の書き出し手順</summary>

おそらくこれらは一切不要です。既定の経路に鍵は不要で、Stellar なら `stellar-agent-wallet` スキルが独自の鍵管理で送金します — この `.env` 設定は、残高を低く抑えた専用ホットウォレットによる EVM/Solana の無人自動化専用です。

**既定の経路ではここに書かれたものは一切不要です。** 自分のウォレットから支払う場合、
鍵も設定も要りません。しかもここでは決して使えないウォレット — ハードウェアウォレットや
取引所アカウントを含む — でも支払えます。

コマンドを実行するディレクトリに `.env` を置きます。本ツールが読み取る変数の全一覧です:

```bash
# 自分のウォレットから支払う場合、以下はどれも不要です。--send を使うときだけ
# 読み込まれます。

# Solana の秘密鍵: base58 文字列、または JSON のバイト配列。
# ~/.config/solana/id.json (自動的に使われます) が無い場合にのみ必要です。
ROZO_CHECKOUT_SOL_KEY=REPLACE_ME_base58_secret_key

# EVM の生の秘密鍵: 0x + 16 進 64 文字。最も安全でない選択肢です。
# 下の keystore を優先してください。
ROZO_CHECKOUT_EVM_KEY=0x0000000000000000000000000000000000000000000000000000000000000000

# EVM の暗号化 V3 keystore: そのファイルへのパス。上の生の鍵より推奨されます。
ROZO_CHECKOUT_EVM_KEYSTORE=/replace/me/keystores/my-hot-wallet

# その keystore のパスフレーズ。無人実行のときだけ必要で、端末では対話的に
# 尋ねられ、保存もされません。
ROZO_CHECKOUT_KEYSTORE_PASSPHRASE=REPLACE_ME_not_a_real_passphrase

# 任意の RPC 上書き。チェーン id ごとに 1 行。8453 = Base、900 = Solana。
ROZO_CHECKOUT_RPC_8453=https://mainnet.base.org
ROZO_CHECKOUT_RPC_900=https://api.mainnet-beta.solana.com
```

そのうえで権限を絞り、git に入らないようにします:

```bash
chmod 600 .env
echo '.env' >> .gitignore
```

**Solana**

- `solana-keygen new` は `~/.config/solana/id.json` を書き出します。設定は不要で、
  自動的に見つかります。これが推奨の経路です。
- **Phantom** → Settings → Export Private Key で得られるのは **base58** 文字列です。
  `ROZO_CHECKOUT_SOL_KEY` に設定してください。
- **Solflare** は現行バージョンでは base58 文字列、古いバージョンでは JSON のバイト配列を
  書き出します。どちらもそのまま使えます。

**EVM**

- **MetaMask** と **Rabby** の秘密鍵の書き出しは 16 進 64 文字です。そのまま
  `ROZO_CHECKOUT_EVM_KEY` に貼り付けてください。`0x` 接頭辞は付けても付けなくても
  構いません。
- **暗号化 keystore (より安全)。** ブラウザーウォレットが書き出せるのは生の鍵だけで、
  keystore ではありません。生の鍵を暗号化 keystore に変えるには Foundry を使います:
  `cast wallet import my-hot-wallet --interactive` が鍵の入力を促し、暗号化された
  V3 keystore を `~/.foundry/keystores/my-hot-wallet` に書き出します
  (`--keystore-dir` で場所を変更できます)。`ROZO_CHECKOUT_EVM_KEYSTORE` をその
  ファイルに向けてください。`geth account import` も V3 keystore を生成します。

**`--send` に使えないウォレット:** ハードウェアウォレット (Ledger、Trezor)、
WalletConnect 専用のモバイルウォレット、取引所アカウント。いずれも設計上、署名鍵を
渡しません。これらの場合は既定の鍵なしの経路を使ってください — すべてで動作します。

</details>

1 回の支払いは **$1,100** を超えられません。それ以上は上記のとおり自分のウォレットから
支払ってください。

```json
{
  "success": true,
  "submitted": true,
  "confirmed": true,
  "txHash": "3Bxs4h24hBjHziQ8UJqSjqjbjWQq2sQ3yV9Fq4HrVh5c"
}
```

## 5. 決済完了を監視する

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

状態は `awaiting_deposit` → `payin_detected` → `payin_confirmed` →
`bridging` → `paying_coinbase` → `settled` と遷移します。オンチェーンの
トランザクションが確認されても終わりではありません: `settled` になるまでポーリングを続けてください。

## うまくいかないとき

`error.code` を読んでください。遭遇しやすいのは次の 3 つです:

| `error.code` | 何が起きたか | どうするか |
|---|---|---|
| `LINK_NO_LONGER_PAYABLE` | そのリンクは既に誰かが支払ったか、期限切れです | 加盟店に新しいリンクを依頼してください。何も支払わないこと |
| `EXPIRY_MARGIN` | 入金・ブリッジ・決済完了を安全に行うには残り時間が足りません | この注文には入金しないでください。期限切れになるのを待ち、同じリンクでステップ 1 からやり直してください（旧注文が未入金と確認されると新しい注文が作られます）。`LINK_USED_OR_EXPIRED`、または `confirmed: true` の `PAYMENT_EXPIRED` が返った場合は、加盟店に新しいリンクを依頼してください |
| `ALREADY_SENT` | この注文に対する送金が既に記録されています | 再送信しては**いけません**。まず `status.js` を実行し、チェーンを確認してください |

**ウォレットから既に資金が出ている場合は、決して二重に支払わないでください。**
`linkId`、`rozoPaymentId`、すべてのトランザクションハッシュを保管し、人間に照合を
依頼してください。使い捨ての入金アドレスへの 2 回目の支払いは、入金として反映される
保証がありません。

エラーコードの完全な一覧は [README.md](../README.md) に、エージェント向けの指示は
[SKILL.md](../SKILL.md) にあります。
