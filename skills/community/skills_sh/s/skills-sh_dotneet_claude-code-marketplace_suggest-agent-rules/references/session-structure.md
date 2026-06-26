# Session File Structure Reference

このドキュメントはClaude CodeとCodex CLIのセッションファイル構造を説明します。

## 1. Claude Code

### ファイル保存場所

```
~/.claude/projects/<project-path-encoded>/
```

プロジェクトパスは`-`区切りでエンコードされます。
例: `/Users/username/projects/myapp` → `-Users-username-projects-myapp`

### ファイルフォーマット

- **形式**: JSONL (JSON Lines)
- **ファイル名**: `<UUID>.jsonl` または `agent-<hash>.jsonl`
- **例**: `7fdbec67-bddd-4dcf-960b-14fa16a2fb44.jsonl`

### レコードタイプ

各行は独立したJSONオブジェクトで、`type`フィールドで種類を判別。

#### user (ユーザーメッセージ)

```json
{
  "type": "user",
  "parentUuid": null,
  "uuid": "c3b9f6d5-50da-44b0-ac5b-1bb9614b724e",
  "sessionId": "7fdbec67-bddd-4dcf-960b-14fa16a2fb44",
  "timestamp": "2026-01-14T09:18:22.684Z",
  "isSidechain": false,
  "userType": "external",
  "cwd": "/Users/username/projects/myapp",
  "version": "2.1.7",
  "gitBranch": "main",
  "message": {
    "role": "user",
    "content": "ユーザーの入力テキスト"
  },
  "todos": []
}
```

#### assistant (アシスタントレスポンス)

```json
{
  "type": "assistant",
  "parentUuid": "c3b9f6d5-50da-44b0-ac5b-1bb9614b724e",
  "uuid": "3c825d7c-eeaf-4ce6-9009-cbc22fc7990d",
  "sessionId": "7fdbec67-bddd-4dcf-960b-14fa16a2fb44",
  "timestamp": "2026-01-14T09:18:26.300Z",
  "message": {
    "model": "claude-opus-4-5-20251101",
    "role": "assistant",
    "content": [
      {
        "type": "thinking",
        "thinking": "思考プロセス..."
      },
      {
        "type": "text",
        "text": "応答テキスト"
      },
      {
        "type": "tool_use",
        "id": "toolu_01GkFFLi3j5PxyAnQmRgbs3v",
        "name": "Read",
        "input": { "file_path": "/path/to/file" }
      }
    ],
    "usage": {
      "input_tokens": 10,
      "output_tokens": 155
    }
  }
}
```

### message.content のブロックタイプ

| タイプ | 説明 |
|-------|------|
| `thinking` | モデルの思考プロセス |
| `text` | テキスト出力 |
| `tool_use` | ツール呼び出し |
| `tool_result` | ツール実行結果（userロールで返される） |

### 会話ツリー構造

`parentUuid`と`uuid`で会話ツリーを構築：

```
user (uuid: A, parentUuid: null)
  └── assistant (uuid: B, parentUuid: A)
       └── user (uuid: C, parentUuid: B)  ← tool_result
            └── assistant (uuid: D, parentUuid: C)
```

### サブエージェントデータ

サブエージェントは専用ディレクトリに保存：

```
~/.claude/projects/<project-path-encoded>/
├── <session-uuid>.jsonl           # メインセッション
└── <session-uuid>/
    └── subagents/
        └── agent-<agent-id>.jsonl # サブエージェントファイル
```

サブエージェントの特徴：
- `agentId`フィールドを持つ
- `isSidechain: true`
- 親セッションと同じ`sessionId`を共有

---

## 2. Codex CLI (新形式)

### ファイル保存場所

```
~/.codex/sessions/YYYY/MM/DD/
```

### ファイルフォーマット

- **形式**: JSONL
- **ファイル名**: `rollout-YYYY-MM-DDThh-mm-ss-<UUID>.jsonl`

### レコードタイプ

#### session_meta (セッションメタデータ)

```json
{
  "timestamp": "2026-01-15T15:42:48.449Z",
  "type": "session_meta",
  "payload": {
    "id": "019bc252-da71-7dc3-9acb-55c6b5993c62",
    "cwd": "/Users/username/projects/myapp",
    "cli_version": "0.80.0",
    "model_provider": "openai",
    "git": {
      "commit_hash": "eb88330",
      "branch": "main"
    }
  }
}
```

#### response_item (メッセージ)

```json
{
  "timestamp": "2026-01-15T15:43:38.571Z",
  "type": "response_item",
  "payload": {
    "type": "message",
    "role": "user",
    "content": [{ "type": "input_text", "text": "ユーザー入力" }]
  }
}
```

#### function_call / function_call_output

```json
{
  "type": "response_item",
  "payload": {
    "type": "function_call",
    "name": "shell_command",
    "arguments": "{\"command\":\"ls\"}",
    "call_id": "call_xxx"
  }
}
```

---

## 3. 比較表

| 項目 | Claude Code | Codex CLI |
|------|-------------|-----------|
| **ファイル形式** | JSONL | JSONL |
| **保存場所** | `~/.claude/projects/<project>/` | `~/.codex/sessions/YYYY/MM/DD/` |
| **メッセージ構造** | ネスト(content blocks) | フラット(payload) |
| **会話ツリー** | `parentUuid` / `uuid` | なし（時系列順） |
| **思考プロセス** | `thinking` content block | `reasoning` item |
| **ツール呼び出し** | `tool_use` / `tool_result` | `function_call` / `function_call_output` |

---

## 4. 解析のポイント

### ルール提案に有用な情報

1. **繰り返しパターン**: 同じツールの使用回数、同じファイルへのアクセス頻度
2. **エラーと修正**: tool_resultでエラーが返り、その後修正が行われたパターン
3. **ユーザーの好み**: 特定の指示パターン、拒否された提案
4. **作業フロー**: ファイル読み取り→編集→テスト のような作業順序

### 抽出すべきデータ

- ユーザーの明示的な指示・好み
- 繰り返し発生した修正（手戻り）
- 使用されたツールとその結果
- プロジェクトのコンテキスト（cwd, gitBranch）
