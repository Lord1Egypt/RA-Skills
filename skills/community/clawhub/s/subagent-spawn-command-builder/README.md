# subagent-spawn-command-builder

`sessions_spawn` を**実行せず**、コマンド用payload JSONだけを生成するスキルです。

## 作成意図

このスキルは、以下の課題を解消するために作成しました。

- subagent呼び出し時の `model/thinking/timeout/cleanup` を毎回手で書くとミスが増える
- `agents.list` 依存の運用は、single-agent中心の使い方では設定コストが高い
- 実行まで1つのスキルに含めると責務が重くなり、トラブル時の切り分けが難しくなる

そのため、**「実行」と「生成」を分離**し、このスキルは

- `sessions_spawn` payload生成

だけに責務を限定しています。

## 目的

- subagent実行パラメータをCLI引数で明示的に渡す
- `sessions_spawn` に渡すJSONを安定して生成する
- 実行は呼び出し側に任せる(このスキルは生成専用)

## 対応パラメータ

生成するpayloadは以下を扱います。

- `task` (required)
- `label` (optional)
- `agentId` (optional)
- `model` (optional)
- `thinking` (optional)
- `runTimeoutSeconds` (optional)
- `cleanup` (`keep|delete`, optional)
- `cwd` (optional) — subagentの作業ディレクトリ
- `mode` (`run|session`, optional)

## ファイル構成

- 生成スクリプト: `scripts/build_spawn_payload.mjs`
- 生成ログ: `state/build-log.jsonl`

## 使い方

TOOLS.md の "Subagent Spawn Profiles" テーブルから対象プロファイルの値を読み取り、CLI引数で渡します。

```bash
skills/subagent-spawn-command-builder/scripts/build_spawn_payload.mjs \
  --profile heartbeat \
  --task "Analyze recent context and return a compact summary" \
  --label heartbeat-test \
  --model openai/gpt-5.4-nano \
  --thinking medium \
  --run-timeout-seconds 180 \
  --cleanup keep
```

`--cwd` / `--mode` が必要な場合は追加します。

```bash
  --cwd /home/altair/.openclaw/workspace/val \
  --mode run
```

## 値の決め方

全ての値はCLI引数から取得します。プロファイル設定ファイルは存在しません。

- モデル・思考レベル・タイムアウトなどのデフォルト値は TOOLS.md の "Subagent Spawn Profiles" テーブルを参照
- `--profile` はログラベルのみ(設定ファイルのlookupキーではない)
- `task` は必ず `--task` で渡す

## 注意

- このスキルは payload/command 生成専用です
- `sessions_spawn` の実行はこのスキルの責務外です
- Python実行コマンドをtaskに含める場合は `python3` を使ってください(`python` は環境によって未定義)
