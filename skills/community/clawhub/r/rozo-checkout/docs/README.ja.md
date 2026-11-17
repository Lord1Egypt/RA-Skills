# rozo-checkout

[English](../README.md) | [简体中文](README.zh.md) | **日本語** | [Español](README.es.md)

**OpenRouter の Coinbase 決済リンク (Payment Link)** を、そのリンクが直接受け取れない
通貨で支払います：Lightning 経由の BTC、Solana、BNB Chain、Ethereum、
Polygon、Arbitrum、Base、Stellar 上の USDT/USDC、またはネイティブコイン（Ethereum・Base・Arbitrum の ETH、BNB、SOL、POL）です。Coinbase の決済リンクは Base 上の USDC しか
受け付けません。本ツールは、あなたが実際に保有している通貨をブリッジ経由で中継し、
資金提供ウォレット (funder wallet) があなたに代わってインボイスを決済します。
アカウントも API キーもブラウザーも不要です。

```bash
npx @rozoai/checkout pay <coinbase-link>
```

どの通貨で支払うかを最初に尋ねます。プロンプトでウォレットアドレスを貼り付けると、
どの通貨なら残高が足りるかを表示します。そのあと、任意のウォレットから支払うための
入金アドレスが表示されます — **秘密鍵も環境変数も設定も一切不要です**。あとは
インボイスが決済完了するまで待つだけです。

使う通貨が決まっている場合は、この質問を省略できます:

```bash
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

## 支払いに使える通貨

| チェーン | `--with` | チェーン id | 備考 |
|---|---|---|---|
| Ethereum | `usdt-ethereum` `usdc-ethereum` | `1` | 小数点以下 6 桁 |
| BNB Chain | `usdt-bnb` `usdc-bnb` | `56` | 小数点以下 18 桁 |
| Polygon | `usdt-polygon` `usdc-polygon` | `137` | 小数点以下 6 桁 |
| Arbitrum | `usdt-arbitrum` `usdc-arbitrum` | `42161` | 小数点以下 6 桁 |
| Base | `usdc-base` | `8453` | 小数点以下 6 桁 |
| Solana | `usdt-solana` `usdc-solana` | `900` | SPL |
| Stellar | `usdc-stellar` | `1500` | `MEMO_TEXT` のメモが必須 — 入金ブロックに表示されます |
| Bitcoin Lightning | `btc-lightning` | `lightning` | BOLT11。金額は satoshi 単位 |

**ネイティブコイン**（それぞれ自分のチェーン上のみ）：

| コイン | `--with` | チェーン id | 備考 |
|---|---|---|---|
| Ethereum の ETH | `eth-ethereum` | `1` | 小数点以下 18 桁（wei）。最低 $1 |
| Base の ETH | `eth-base` | `8453` | 小数点以下 18 桁（wei） |
| Arbitrum の ETH | `eth-arbitrum` | `42161` | 小数点以下 18 桁（wei） |
| BNB | `bnb-bnb` または `bnb` | `56` | 小数点以下 18 桁 |
| SOL | `sol-solana` または `sol` | `900` | 小数点以下 9 桁（lamports） |
| POL | `pol-polygon` または `pol` | `137` | 小数点以下 18 桁 |

ネイティブコインは、そのインボイスの見積もりに含まれている場合にのみ使えます（`quote` で確認できます）。上限は 1 件 $3,500 です。注文は Lightning と同じく**exact-out（受取額固定）**で、入金ブロックのコイン数量をそのまま正確に送ってください。価格は表示された時刻（約 1 時間）までしか固定されません。OpenRouter の支払いリンク自体は作成から約 24 時間支払い可能です。それを過ぎたら送らず、注文の期限切れを待って新しく作り直してください。コイン数量にはサービス手数料に加えて為替スプレッドが含まれます。ウォレットにはネットワーク手数料用に同じコインが少し余分に必要です。取引所から出金する場合は、着金額が全額になるよう、出金手数料が差し引かれないことを確認してください。`--send` もネイティブコインに対応しており、正確な数量の通常送金として送ります。

オンチェーンの BTC と Tron には対応していません。
Zcash の ZEC（Beta）は https://checkout.rozo.ai/zec を使ってください。この CLI では ZEC の注文は作れません。

## どのウォレットが必要ですか？

**ウォレットは 1 つ、チェーンも 1 つで足ります — チェーンごとに用意する必要はありません。**上の表から、すでに持っている通貨を選び、それが今ある場所から支払ってください。

- **どのウォレットでも構いませんし、取引所からの出金でも構いません。**既定の経路は入金情報を表示するだけです。示された `amount` の `tokenSymbol` を、その `chain` 上で `receiverAddress` へ送るだけです。どのサイトに接続することも、ブラウザで承認することもありません。実際には、EVM チェーンでは MetaMask や Rabby、Solana では Phantom や Solflare、BTC では Phoenix や Wallet of Satoshi といった Lightning ウォレットがよく使われています。
- **注意が必要なのは Stellar です。**Stellar の入金は共有アドレスと `receiverMemo` の組み合わせで振り分けられるため、取引所であれウォレットであれ、送信元で memo を設定できる必要があります。memo を省くと、その支払いは失われます。
- **Lightning はアドレスではなくインボイスに支払います。**`deposit.lnInvoice` をスキャンまたは貼り付けてください。送金先アドレスというものはありません。
- **秘密鍵が必要なのは `--send` だけ**で、`ROZO_CHECKOUT_EVM_KEY` または `ROZO_CHECKOUT_SOL_KEY` から読み込まれ、対象は EVM チェーンと Solana のみです。それ以外はすべて鍵不要です。

## エージェントから使う

渡す内容はどこでも同じです。上のワンライナーそのものか、エージェントに
[llms.txt](../llms.txt) を読ませるかのどちらかです。**自分のウォレットから支払う場合、
鍵は一切不要です。** ローカルで署名するのは任意の `--send` フラグだけで、
`ROZO_CHECKOUT_EVM_KEY` / `ROZO_CHECKOUT_SOL_KEY` を読むのもそのフラグだけです。
エージェントやスクリプトでは必ず `--with` を渡してください。対話式の選択は端末でのみ
表示され、既定の通貨は意図的にありません。

<details>
<summary><b>Claude Code</b> — スキルをインストールするか、ワンライナーを貼り付ける</summary>

このリポジトリは Claude Code のスキルです。`SKILL.md` と `scripts/dist/` 内の実行可能
ファイルが同梱されています。スキルディレクトリにクローンすれば、Claude Code が自動的に
認識します。

```bash
git clone https://github.com/RozoAI/rozo-checkout-skill ~/.claude/skills/rozo-checkout
```

インストールせずに、実行を依頼するだけでも構いません:

```
この OpenRouter のリンクを Solana の USDT で支払ってください:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

ウォレット: どのウォレットでも構いません。**鍵は不要です。** Claude にホットウォレット
から署名させたい場合にだけ `--send` を追加してください。その場合は環境変数の鍵が必要です。
</details>

<details>
<summary><b>Codex CLI</b> — AGENTS.md に書くか、そのまま実行する</summary>

Codex はプロジェクトルートの `AGENTS.md` を読みます。毎回説明しなくても支払い方が
分かるように、常設の指示を追加しておきましょう:

```
OpenRouter / Coinbase の決済リンクを支払うには、次を実行してください:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

ウォレット: どのウォレットでも構いません。**鍵は不要です。** Solana CLI の鍵ペアまたは暗号化された keystore を使う `--send`（EVM チェーンと Solana のみ、Stellar と Lightning はモード A 専用）の場合だけ
環境変数の鍵が必要です。
</details>

<details>
<summary><b>OpenCode</b> — AGENTS.md に書くか、そのまま実行する</summary>

OpenCode もプロジェクトルートの `AGENTS.md` を読むため、上の Codex 用のスニペットが
そのまま使えます。最短経路はやはりコマンドそのものです:

```bash
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

ウォレット: どのウォレットでも構いません。**鍵は不要です。** Solana CLI の鍵ペアまたは暗号化された keystore を使う `--send` の場合だけ
環境変数の鍵が必要です。
</details>

<details>
<summary><b>Cline</b> — .clinerules に書くか、そのまま実行する</summary>

Cline はプロジェクトルートの `.clinerules` から常設の指示を読み込みます:

```
OpenRouter / Coinbase の決済リンクを支払うには、次を実行してください:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

ウォレット: どのウォレットでも構いません。**鍵は不要です。** Solana CLI の鍵ペアまたは暗号化された keystore を使う `--send` の場合だけ
環境変数の鍵が必要です。
</details>

<details>
<summary><b>Cursor</b> — .cursor/rules に書くか、そのまま実行する</summary>

`.cursor/rules/rozo-checkout.mdc` にプロジェクトルールを追加します:

```
OpenRouter / Coinbase の決済リンクを支払うには、次を実行してください:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

ウォレット: どのウォレットでも構いません。**鍵は不要です。** Solana CLI の鍵ペアまたは暗号化された keystore を使う `--send` の場合だけ
環境変数の鍵が必要です。
</details>

<details>
<summary><b>Hermes Agent</b> — セッション内でワンライナーを実行する</summary>

Hermes Agent（Nous Research）はシェルにアクセスでき、独自のスキルシステムを持っています。
`hermes` で起動して、こう依頼してください:

```
https://checkout.rozo.ai/llms.txt を取得したうえで、この OpenRouter のリンクを支払ってください:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

ウォレット: どのウォレットでも構いません。**鍵は不要です。** Solana CLI の鍵ペアまたは暗号化された keystore を使う `--send` の場合だけ
環境変数の鍵が必要です。
</details>

<details>
<summary><b>OpenClaw</b> — openclaw agent exec</summary>

OpenClaw のヘッドレス入口は単発のタスクを実行するため、スクリプトやチャットチャンネル
から起動する支払いに向いています:

```bash
openclaw agent exec "Pay this OpenRouter link with USDT on Solana by running: npx @rozoai/checkout pay <coinbase-link> --with usdt-solana"
```

ウォレット: どのウォレットでも構いません。**鍵は不要です。** Solana CLI の鍵ペアまたは暗号化された keystore を使う `--send` の場合だけ
環境変数の鍵が必要です。
</details>

<details>
<summary><b>Pi</b> — セッション内でワンライナーを実行する</summary>

Pi は BYOK のターミナルエージェントで、組み込みツールに `bash` を含むため、コマンドを
直接実行できます。`pi` で起動して、こう依頼してください:

```
この OpenRouter のリンクを Solana の USDT で支払ってください。次を実行します:
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana
```

ウォレット: どのウォレットでも構いません。**鍵は不要です。** Solana CLI の鍵ペアまたは暗号化された keystore を使う `--send` の場合だけ
環境変数の鍵が必要です。
</details>

<details>
<summary><b>ターミナル — エージェントなし</b> — スクリプトを 1 ステップずつ実行する</summary>

各ステップを自分で進めます。バンドルは自己完結型なので、Node 18 以降のほかに
インストールするものはありません。

```bash
git clone https://github.com/RozoAI/rozo-checkout-skill && cd rozo-checkout-skill
LINK="https://payments.coinbase.com/payment-links/pl_01YOURLINKID"

# 読み取り専用の見積もり。費用はかかりません
node scripts/dist/quote.js --url "$LINK"

# 注文を作成します。ここでは完全な入金アドレスは伏せられ、まず確認用の
# マスクされた要約が返ります。
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT

# 支払うと決めたら、--confirm を付けて再実行し、アドレスを開示します
node scripts/dist/create-order.js --url "$LINK" --chain 900 --token USDT --confirm

# 入金ブロックの内容を任意のウォレットから支払い、決済完了を見守ります
node scripts/dist/status.js --rozo-payment-id <uuid> --watch
```

各スクリプトは標準出力にちょうど 1 個の JSON オブジェクトを出力します。終了コードは
`0` が成功、`1` が拒否/失敗（`error.code` を参照）、`2` が使い方の誤り、`3` が送信済みだが
未確認です。詳しい手順: [クイックスタート](QUICKSTART.ja.md)。

ウォレット: どのウォレットでも構いません。**鍵は不要です。** ホットウォレットからの送金
については、`ROZO_CHECKOUT_EVM_KEY` / `ROZO_CHECKOUT_SOL_KEY` を読む `send-evm.js` /
`send-sol.js` を参照してください。
</details>

<details>
<summary><b>その他のあらゆるエージェント</b> — llms.txt を読ませる</summary>

URL を取得してコマンドを実行できるエージェントであれば、どれでもこれができます:

```
https://checkout.rozo.ai/llms.txt を自分のコンテキストに読み込み、それを使って
この OpenRouter のリンクを支払ってください: <coinbase-link>
```

シェルを持たないエージェントでも、HTTP リクエストが可能なら 4 つの公開エンドポイントを
直接操作できます — [仕組み](how-it-works.md) を参照してください。

ウォレット: どのウォレットでも構いません。**鍵は不要です。** Solana CLI の鍵ペアまたは暗号化された keystore を使う `--send` の場合だけ
環境変数の鍵が必要です。
</details>

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

## 知っておく価値のある 3 つのルール

- **入金アドレスは使い捨てです。** 古い注文、キャッシュされたレスポンス、スクリーンショット
  から得たアドレスを再利用しては決していけません。
- **表示された金額をそのとおりに送金してください。** 通常はインボイス金額より大きくなります
  — ブリッジ手数料とネットワーク手数料が含まれるためです。
- **入金済みの注文に二重に支払っては決していけません。** すでに支払いが検知されている場合は
  中止し、人間に照合を依頼してください。使い捨てアドレスへの 2 回目の支払いは、入金として
  反映される保証がありません。

本ツールが何を拒否するのか、そしてその理由の完全な一覧は
[safety.md](safety.md) にあります。

## リンク

- [クイックスタート](QUICKSTART.ja.md) — 5 つのコマンドと、期待される出力
- [仕組み](how-it-works.md) — フロー、エンドポイント、識別子
- [安全性の設計](safety.md) — すべての安全機構の詳細
- [SKILL.md](../SKILL.md) — エージェント向けの指示書 · [llms.txt](../llms.txt) — 1 ファイルの要約
- [checkout.rozo.ai/agent](https://checkout.rozo.ai/agent.html) — 同じものを Web で
- [Issues](https://github.com/RozoAI/rozo-checkout-skill/issues) — バグと要望

## 変更履歴

- **0.1.3** — 最初の実際の支払いで見つかった不具合の修正。ビルド済みバンドルが Node 22 以降で
  `__filename is not defined` により停止しなくなりました（esbuild の banner が `require` に加えて
  `__filename`/`__dirname` も定義し、テストが各バンドルを実際に実行するようになりました）。Stellar の
  入金では memo の種類（`MEMO_TEXT`。memo が数字に見える場合も同様）を明示します。注文の残り有効時間を
  入金ブロックと `status` の両方で継続時間として表示し（"expires in 47m"）、期限切れ時には新しい注文を
  作るコマンドをそのまま示します。既存の未払い注文の再利用と、それと異なる通貨を指定した場合の双方を、
  エラーではなく説明として提示します。
- **0.1.2** — モード B で環境変数に生の秘密鍵を置く必要がなくなりました。Solana では
  `solana-keygen` が既に作成した `~/.config/solana/id.json` を、EVM では暗号化された
  V3 keystore（パスフレーズは対話的に入力）を使います。`--keyfile` でどちらも明示でき、
  設定は gitignore した `.env` に置くこともできます。環境変数の生の鍵は無人自動化向けに
  引き続き利用できます。鍵ファイルと `.env` は `chmod 600` かつ git 未追跡である必要が
  あります。
- **0.1.1** — 支出上限を 2 つから 1 つに変更しました。1 回の支払いは $1,100 を超えられず
  （$1,000 のクレジット購入とその 5% の手数料に合わせた値です）、セッション累計の上限と
  `--yes-large` による上書きは削除されました。自分のウォレットから支払う場合は鍵も設定も
  不要であることを、ドキュメントで明示しました。
- **0.1.0** — 最初のリリース: `npx @rozoai/checkout`。

## ライセンス

MIT.
