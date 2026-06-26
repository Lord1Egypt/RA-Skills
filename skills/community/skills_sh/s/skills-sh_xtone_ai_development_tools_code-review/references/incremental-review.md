# インクリメンタルレビュー（PR更新時の差分最適化）

PR更新（`synchronize`イベント）時に、前回のレビュー状態を活用してトークン消費を削減する。

## `.pr-review-state.json` の構造

CI環境で `actions/cache` により実行間で永続化される。

> **注意**: `.pr-review-state.json` が不正な形式（JSONパースエラー等）の場合は、警告を出力してフルトリアージを実行する。破損した状態ファイルに基づいてインクリメンタルモードを実行してはならない。

```json
{
  "pr_number": 123,
  "last_reviewed_commit": "abc123def",
  "last_reviewed_at": "2026-03-06T10:00:00Z",
  "triage": {
    "surface_issues": [
      {
        "severity": "Minor",
        "file": "src/api/users.ts",
        "line": 15,
        "issue": "`any`型が使用されている",
        "suggestion": "具体的な型に変更する"
      }
    ]
  },
  "review_comments": [
    {
      "comment_id": 789,
      "file": "src/api/users.ts",
      "line": 15,
      "severity": "Minor",
      "issue": "`any`型が使用されている",
      "commit_id": "abc123def"
    }
  ]
}
```

## インクリメンタルトリアージの動作

`.pr-review-state.json` が存在する場合、トリアージジョブは以下の最適化を行う：

1. **変更差分の比較** — `last_reviewed_commit` 以降に変更されたファイルを特定する
2. **Minor/Suggestionのスキップ** — 前回から変更のないファイルに対する `surface_issues` はそのまま引き継ぎ、再チェックしない（`"carried_over": true` を付与）
3. **変更ファイルのみ再チェック** — 変更があったファイルについてのみ、表層チェックを実行する
4. **解決済み問題の検出** — 前回の `surface_issues` のうち、該当行が修正されたものを `resolved_issues` として出力する

## インクリメンタルモードの `.pr-triage.json` 追加フィールド

```json
{
  "incremental": true,
  "base_commit": "abc123def",
  "changed_since_last_review": ["src/api/users.ts"],
  "unchanged_since_last_review": ["src/routes/index.ts"],
  "resolved_issues": [
    {
      "comment_id": 789,
      "file": "src/api/users.ts",
      "line": 15,
      "issue": "`any`型が使用されている",
      "resolution": "fixed"
    }
  ],
  "surface_issues": [
    {
      "severity": "Minor",
      "file": "src/routes/index.ts",
      "line": 42,
      "issue": "マジックナンバーの使用",
      "suggestion": "定数に抽出する",
      "carried_over": true
    }
  ]
}
```

## 修正済み問題へのコメントリプライ

レビュージョブは `resolved_issues` に含まれる問題について、元のインラインコメント（`comment_id`）にリプライする：

```
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
  -f body="この問題は修正されました。"
```

> **`.pr-review-state.json` が存在しない場合**（初回レビュー）は、インクリメンタル最適化は適用されず、フルトリアージを実行する。
