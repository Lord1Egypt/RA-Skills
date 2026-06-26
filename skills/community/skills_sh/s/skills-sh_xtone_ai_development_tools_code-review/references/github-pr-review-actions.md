# GitHub PRレビューアクション

GitHub Actions等のCI環境でPRレビューを実行する際の、コメント投稿・評価方法のリファレンス。

---

## 1. このガイドのスコープ

- 対象：**GitHub Actions等のCI環境**でのClaude Code実行時のみ
- 目的：レビュー結果を適切な形式でGitHub上に投稿する
- 前提：`gh` CLI が利用可能であり、適切な権限（`GITHUB_TOKEN`等）が設定されていること
- **非対象**：ローカル環境での実行（ローカルではレビュー結果を標準出力に表示するのみ）

### CI環境の判定

以下の環境変数でCI環境かどうかを判定できる：

| 環境変数 | 説明 |
|----------|------|
| `CI=true` | 一般的なCI環境 |
| `GITHUB_ACTIONS=true` | GitHub Actions |
| `GITHUB_TOKEN` | GitHub APIアクセス用トークンが設定されている |

これらが設定されていない場合は、このリファレンスの内容（GitHub上への投稿）は実行しない。

---

## 2. PR情報の取得

レビュー開始前に、PRの全体像を把握する。

### 基本情報の取得

```bash
# PR基本情報の取得
gh pr view <PR番号> --json title,body,author,createdAt,headRefName,baseRefName,mergeable,reviewDecision

# 変更ファイル一覧の取得
gh pr diff <PR番号> --name-only

# コード差分の取得
gh pr diff <PR番号>

# 既存のレビューとコメントの確認
gh pr view <PR番号> --json reviews,comments
```

### 取得すべき情報

| 情報 | コマンド/フィールド | 用途 |
|------|---------------------|------|
| タイトル・説明 | `title`, `body` | 変更の意図を理解 |
| 作成者 | `author` | コンテキストの把握 |
| ブランチ情報 | `headRefName`, `baseRefName` | 差分の範囲を特定 |
| マージ可否 | `mergeable` | コンフリクトの有無 |
| 既存レビュー | `reviewDecision` | 他レビュアーの判断 |

---

## 3. インラインコメントの投稿

具体的なファイル・行番号が特定できる問題は、インラインコメントで指摘する。

### MCPツールを使用する場合

```
mcp__github_inline_comment__create_inline_comment
```

このツールが利用可能な場合は、ファイルパスと行番号を指定してインラインコメントを投稿できる。

### gh APIを使用する場合

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
  -f body="コメント内容" \
  -f commit_id="$(gh pr view <PR番号> --json headRefOid -q .headRefOid)" \
  -f path="ファイルパス" \
  -F line=行番号 \
  -f side="RIGHT"
```

### インラインコメントのベストプラクティス

- **問題の重要度を明示**: `**Critical**:`, `**Major**:`, `**Minor**:` などのプレフィックスを使用
- **具体的な修正案を提示**: 問題だけでなく解決方法も記載
- **コード例を含める**: 可能であれば修正後のコードスニペットを提示

---

## 4. レビュー結果の投稿

レビュー完了後、結果をPRに投稿する。

### 投稿パターン

#### パターン1: Critical問題あり → REQUEST_CHANGES

マージ前に必ず修正が必要な問題がある場合。

```bash
gh pr review <PR番号> \
  --request-changes \
  --body "## ⚠️ 変更が必要です

以下のCritical問題が検出されました。修正してから再度レビューをリクエストしてください。

### Critical問題

- [問題の概要] - 詳細はインラインコメントを参照

**注**: 具体的な問題箇所と修正方法はファイルのインラインコメントで指摘しています。

修正後、このレビューを解決してください。"
```

#### パターン2: Major/Minor問題あり → 条件付きAPPROVE

重大ではないが改善すべき問題がある場合。

```bash
gh pr review <PR番号> \
  --approve \
  --body "## ✅ 条件付きでApprove

レビューを完了しました。重大な問題は見つかりませんでしたが、いくつかの改善点があります。

### 分析結果

#### 📦 Skill Quality: X/10
- 良い点: [概要]
- 改善点: [件数]件の指摘（インラインコメント参照）

### 改善項目

**注**: 具体的な改善箇所と推奨される対応は、各ファイルのインラインコメントで詳しく説明しています。

これらは次のイテレーションで対応することをお勧めします。"
```

#### パターン3: 問題なし → APPROVE

問題が検出されなかった場合。

```bash
gh pr review <PR番号> \
  --approve \
  --body "## ✅ Approved

レビューを完了しました。問題は見つかりませんでした。

### 分析結果

#### 📦 Skill Quality: 10/10
✅ フロントマターが正しく設定されています
✅ descriptionにトリガー条件が明記されています
✅ ディレクトリ構造が適切です
✅ 参照ファイルがすべて存在します

### Summary

マージして問題ありません。"
```

---

## 5. レビュー結果のフォーマット

### 標準フォーマット

```markdown
## Code Review: [判定結果]

### 変更概要
- **スコープ**: [変更の概要を1-2文で]
- **変更ファイル数**: [N]ファイル
- **主な言語/FW**: [検出された言語/FW]

### スコア: X/10

### 検出された問題

| # | 重要度 | ファイル | 問題 | 推奨される対応 |
|---|--------|---------|------|---------------|
| 1 | [Critical/Major/Minor/Suggestion] | [ファイルパス:行番号] | [問題の説明] | [対応方法] |

### 良い点
- [コードの良い点を具体的に記載]

### 判定
- **結果**: [Approve / Conditional Approve / Reject]
- **理由**: [判定理由の要約]

### 次のステップ
- [修正が必要な場合の具体的なアクション]
```

---

## 6. GitHub Actionsでの実行時の注意事項

### 権限設定

GitHub Actionsで実行する場合、以下の権限が必要：

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### allowedTools の設定（重要）

`claude-code-action` の `claude_args` で `--allowedTools` を指定する場合、以下のツールを**すべて含める**こと。不足するとスキルの実行やコード読み取りに失敗し、レビューが正常に行われない。

| ツール | 用途 | 必須 |
|--------|------|------|
| `Skill` | `/code-review` スキル自体の実行 | 必須 |
| `Read` | ソースコードの読み取り | 必須 |
| `Glob` | ファイルパターンによる検索 | 必須 |
| `Grep` | コード内のパターン検索 | 必須 |
| `Bash(gh:*)` | `gh` CLIによるPR情報取得・レビュー投稿 | 必須 |
| `WebSearch` | ベストプラクティスや公式ドキュメントの参照 | 推奨 |
| `mcp__github_inline_comment__create_inline_comment` | インラインコメント投稿（MCPツール利用時） | 任意 |

**設定例：**

```
--allowedTools "Skill,Read,Glob,Grep,WebSearch,Bash(gh:*)"
```

> **注意**: `allowedTools` を指定しない場合は全ツールが利用可能。指定する場合は上記の必須ツールを漏れなく含めること。過去にこの設定不足により、17ターン消費してもレビューが投稿されない問題が発生した。

### 環境変数

`gh` CLIが正しく動作するために必要：

```yaml
env:
  GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

または、GitHub Appトークンを使用：

```yaml
env:
  GH_TOKEN: ${{ steps.app-token.outputs.token }}
```

### 自動レビューの注意事項

- レビューはAIによる自動分析であり、最終的な判断は人間のレビュアーが行う必要がある
- スキルの実用性やドメイン知識が必要な判断は人間のレビューが必要
- 自動レビューの結果を過信せず、補助的なツールとして活用する

---

## 7. GitHub Actionsワークフローの設定例

> **コスト最適化版**: Haiku + Opus の2ジョブ構成でトークンコストを50-60%削減できる設定例は [ci-optimized-workflow.md](ci-optimized-workflow.md) を参照。

`anthropics/claude-code-action` を使用した、実運用で検証済みの設定例。

```yaml
name: Automated PR Review

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

concurrency:
  group: pr-review-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  automated-review:
    if: github.actor != 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Install vercel-react-best-practices skill
        run: npx -y skills add vercel-labs/agent-skills --skill vercel-react-best-practices --agent claude-code --yes

      - name: Run Claude Code PR Review
        uses: anthropics/claude-code-action@v1
        with:
          github_token: ${{ steps.app-token.outputs.token }}
          prompt: |
            PR #${{ github.event.pull_request.number }} をコードレビューしてください。

            /code-review
          claude_args: |
            --max-turns 40
            --allowedTools "Skill,Read,Glob,Grep,WebSearch,Bash(gh:*)"
```

### 設定のポイント

| 項目 | 説明 |
|------|------|
| `paths-ignore` | スキルファイルやドキュメントの変更ではレビューを実行しない |
| `concurrency` | 同一PRへの重複実行を防止する |
| `if: github.actor != 'dependabot[bot]'` | Dependabot PRではSecretsが利用不可のためスキップ |
| `max-turns 40` | 大規模PRでもレビューを完了できるよう十分なターン数を設定 |
| `Install skill` ステップ | React / Next.js プロジェクトの場合に外部スキルをインストール |

> **Vertex AI経由の場合**: `use_vertex: "true"` と `ANTHROPIC_VERTEX_PROJECT_ID`、`CLOUD_ML_REGION` の設定が追加で必要。認証には Workload Identity Federation を使用し、`id-token: write` 権限も追加する。

---

## 8. チェックリスト

### レビュー投稿前

- [ ] PR情報を取得し、変更の意図を理解した
- [ ] 変更ファイルを確認し、差分を分析した
- [ ] 問題を重要度別に分類した
- [ ] インラインコメントで具体的な箇所を指摘した

### レビュー投稿時

- [ ] 適切なレビューアクション（approve/request-changes/comment）を選択した
- [ ] レビュー本文に分析結果のサマリーを含めた
- [ ] インラインコメントへの参照を含めた
- [ ] 次のステップを明示した
