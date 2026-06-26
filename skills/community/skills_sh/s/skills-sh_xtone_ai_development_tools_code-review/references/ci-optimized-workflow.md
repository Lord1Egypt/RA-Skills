# CI環境でのコスト最適化ワークフロー

Opus単体で全ステップを実行する構成から、**Haiku（トリアージ）+ Opus（深層レビュー）の2ジョブ構成**に変更することで、トークン使用量を大幅に削減する。

## 目次

1. [最適化の概要](#1-最適化の概要)
2. [GitHub Actionsワークフロー設定例](#2-github-actionsワークフロー設定例)
3. [Haiku使用時の注意点](#3-haiku使用時の注意点)
4. [段階的な導入](#4-段階的な導入)

---

## 1. 最適化の概要

### 従来構成（Opus単体）

```
[Opus] PR情報取得 → ファイル分類 → リファレンス全読み → 全チェック → 判定 → 投稿
       ~40ターン、リファレンス全読み込み
```

### 最適化構成（Haiku + Opus）

```
[Haiku] PR情報取得 → ファイル分類 → 表層チェック → .pr-triage.json出力
        ~10ターン

[Opus]  トリアージ読み込み → 必要なリファレンスのみ読み → Critical/Major集中 → 判定 → 投稿
        ~20ターン、リファレンス選択的読み込み
```

### インクリメンタル構成（Haiku + Opus、PR更新時）

```
[Cache] 前回の .pr-review-state.json を復元

[Haiku] PR差分取得 → 前回との差分比較 → 変更ファイルのみ表層チェック → .pr-triage.json（incremental）出力
        ~5-8ターン（未変更ファイルのチェックをスキップ）

[Opus]  トリアージ読み込み → resolved_issuesへのコメントリプライ → 変更箇所のCritical/Major集中 → 判定 → 投稿
        ~15-20ターン

[Cache] .pr-review-state.json を保存（コメントID含む）
```

### 期待されるコスト削減効果

| 項目 | 従来 | 最適化後 | 削減率 |
|------|------|---------|--------|
| Opusターン数 | ~40 | ~20 | 50% |
| Opusトークン入力（リファレンス） | 全ファイル（~500行） | 必要分のみ（~100-200行） | 60-80% |
| Haikuコスト追加 | - | ~10ターン | （Opusの1/10以下） |
| **合計コスト** | **100%** | **約40-50%** | **50-60%** |

> Haikuの料金はOpusの約1/50（入力）〜1/100（出力）のため、Haikuフェーズの追加コストは無視できるレベル。

**インクリメンタルモード時の追加削減（PR更新時）：**

| 項目 | 初回レビュー | 2回目以降（インクリメンタル） | 追加削減率 |
|------|-------------|---------------------------|-----------|
| Haikuトリアージ | ~10ターン | ~5-8ターン | 20-50% |
| Opus表層チェック | 全ファイル | 変更ファイルのみ | 変更量に依存 |
| Opusターン数 | ~20 | ~15-20 | 0-25% |
| **合計コスト（初回比）** | **約40-50%** | **約25-40%** | **追加10-15%削減** |

---

## 2. GitHub Actionsワークフロー設定例

### 完全な設定例（Vertex AI経由）

```yaml
name: Automated PR Review (Optimized)

on:
  pull_request:
    types: [opened, synchronize, reopened]
    paths-ignore:
      - '.claude/skills/**'
      - '*.md'
      - 'LICENSE'

permissions:
  contents: read
  pull-requests: write
  issues: write
  id-token: write  # Vertex AI Workload Identity Federation用

concurrency:
  group: pr-review-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  # ==========================================================
  # Phase 1: トリアージ（Haiku - 軽量・高速・低コスト）
  # ==========================================================
  triage:
    if: github.actor != 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Restore previous review state
        id: restore-state
        uses: actions/cache/restore@v4
        with:
          path: .pr-review-state.json
          key: pr-review-state-${{ github.event.pull_request.number }}-dummy
          restore-keys: |
            pr-review-state-${{ github.event.pull_request.number }}-

      - name: Authenticate to Google Cloud
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Install skills
        run: npx -y skills add xtone/ai_development_tools --skill pr-triage --agent claude-code --yes

      - name: Run Triage with Haiku
        uses: anthropics/claude-code-action@v1
        env:
          ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
          CLOUD_ML_REGION: global
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          use_vertex: "true"
          prompt: |
            PR #${{ github.event.pull_request.number }} のトリアージを実行してください。
            `.pr-review-state.json` が存在する場合はインクリメンタルモードで実行してください。
            /pr-triage
          claude_args: |
            --model claude-haiku-4-5@20251001
            --max-turns 10
            --allowedTools "Skill,Read,Glob,Grep,Bash(gh:*),Write"

      - name: Upload triage results
        uses: actions/upload-artifact@v4
        with:
          name: pr-triage
          path: |
            .pr-triage.json
            .pr-review-state.json
          retention-days: 1

  # ==========================================================
  # Phase 2: 深層レビュー（Opus - 高精度・Critical/Major集中）
  # ==========================================================
  review:
    needs: triage
    if: github.actor != 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Download triage results
        uses: actions/download-artifact@v4
        with:
          name: pr-triage
          path: .

      - name: Restore previous review state
        uses: actions/cache/restore@v4
        with:
          path: .pr-review-state.json
          key: pr-review-state-${{ github.event.pull_request.number }}-dummy
          restore-keys: |
            pr-review-state-${{ github.event.pull_request.number }}-

      - name: Authenticate to Google Cloud
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Install vercel-react-best-practices skill
        run: npx -y skills add vercel-labs/agent-skills --skill vercel-react-best-practices --agent claude-code --yes

      - name: Run Claude Code PR Review via Vertex AI
        uses: anthropics/claude-code-action@v1
        env:
          ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
          CLOUD_ML_REGION: global

          CLAUDE_CODE_ENABLE_TELEMETRY: "1"
          OTEL_METRICS_EXPORTER: "otlp"
          OTEL_LOGS_EXPORTER: "otlp"
          OTEL_EXPORTER_OTLP_PROTOCOL: "http/protobuf"
          OTEL_EXPORTER_OTLP_ENDPOINT: ${{ secrets.GRAFANA_OTLP_ENDPOINT }}
          OTEL_EXPORTER_OTLP_HEADERS: "Authorization=Basic ${{ secrets.GRAFANA_OTLP_TOKEN }}"
          OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE: "cumulative"
          OTEL_METRIC_EXPORT_INTERVAL: "30000"
          OTEL_LOGS_EXPORT_INTERVAL: "5000"
          OTEL_RESOURCE_ATTRIBUTES: "github.repository=${{ github.repository }},github.repository_owner=${{ github.repository_owner }},github.actor=${{ github.actor }},github.event_name=${{ github.event_name }},deployment.environment=production"
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          use_vertex: "true"
          show_full_output: "true"
          prompt: |
            PR #${{ github.event.pull_request.number }} をコードレビューしてください。

            重要: まず `.pr-triage.json` ファイルを読み込んでください。トリアージフェーズの分析結果が含まれています。
            このファイルの内容に基づき、必要なリファレンスのみを読み込み、Critical/Majorレベルの問題に集中してレビューを行ってください。

            ## 修正済み問題へのフォローアップ（インクリメンタルレビュー時）

            `.pr-triage.json` の `resolved_issues` に要素がある場合、各問題の `comment_id` に対してリプライを投稿してください：

            ```bash
            gh api repos/${{ github.repository }}/pulls/${{ github.event.pull_request.number }}/comments/{comment_id}/replies \
              -f body="この問題は修正されました。"
            ```

            ## レビュー投稿

            レビュー完了後、必ず以下の2つのアクションをGitHub上で実行してください。
            1. 問題のあるコード行にインラインコメントを投稿する（mcp__github_inline_comment__create_inline_comment または gh api を使用）
            2. `gh pr review` コマンドでレビュー結果（approve/request-changes）を投稿する

            ## レビュー状態の保存

            レビュー完了後、投稿したインラインコメントのIDを記録した `.pr-review-state.json` を作成してください：

            1. `gh api repos/${{ github.repository }}/pulls/${{ github.event.pull_request.number }}/comments --jq '[.[] | select(.user.login == "github-actions[bot]" or .user.type == "Bot") | {comment_id: .id, file: .path, line: .line, issue: (.body | split("\n") | first), commit_id: .commit_id}]'` で投稿済みコメントを取得
            2. 以下の構造で `.pr-review-state.json` を出力する：

            ```json
            {
              "pr_number": ${{ github.event.pull_request.number }},
              "last_reviewed_commit": "<現在のHEADコミットSHA>",
              "last_reviewed_at": "<現在時刻（ISO 8601）>",
              "triage": {
                "surface_issues": [<.pr-triage.jsonのsurface_issuesをコピー（carried_over含む）>]
              },
              "review_comments": [<上記で取得したコメント情報>]
            }
            ```

            テキスト出力のみで終了せず、必ずGitHub上にレビューを投稿してください。

            /code-review
          claude_args: |
            --model claude-opus-4-6@default
            --max-turns 25
            --allowedTools "Skill,Read,Glob,Grep,WebSearch,mcp__github_inline_comment__create_inline_comment,Bash(gh:*),Write"

      - name: Save review state to cache
        if: always()
        uses: actions/cache/save@v4
        with:
          path: .pr-review-state.json
          key: pr-review-state-${{ github.event.pull_request.number }}-${{ github.sha }}
```

---

## 3. Haiku使用時の注意点

### Vertex AIでのHaikuモデルID

Vertex AI経由でHaikuを使用する場合、モデルIDは環境によって異なる場合がある。
使用可能なモデルIDを事前に確認すること：

```bash
# 利用可能なモデル一覧の確認（gcloud CLI）
gcloud ai models list --region=global --filter="displayName:claude"
```

一般的なVertex AIのモデルID：
- `claude-haiku-4-5@20251001` (Claude 4.5 Haiku)
- `claude-opus-4-6@default` (Claude Opus 4.6)

### トリアージ失敗時のフォールバック

トリアージジョブが失敗した場合、レビュージョブはスキップされる。
必要に応じて、トリアージなしでOpus単体レビューを行うフォールバックジョブを追加できる：

```yaml
  review-fallback:
    needs: triage
    if: failure() && github.actor != 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      # トリアージなしでOpus単体レビュー（従来構成と同じ）
      # ...
```

---

## 4. 段階的な導入

### Step 1: まず効果を測定

既存のワークフローと並行して最適化版を実行し、以下を比較する：
- トークン使用量（OTel メトリクス）
- レビュー品質（検出された問題の差分）
- 実行時間

### Step 2: チューニング

実測結果に基づき以下を調整：
- Haikuの `max-turns`（デフォルト10、必要に応じて増減）
- Opusの `max-turns`（デフォルト25、トリアージ品質次第で削減可能）
- トリアージプロンプトの表層チェック項目

### Step 3: 本番切り替え

品質に問題がなければ、最適化版に完全移行する。
