# Social Media Automation

OpenClawスキル - ソーシャルメディア自動化ツール

## 概要

複数のSNSプラットフォーム（X/Twitter, Bluesky, LinkedInなど）を一元管理し、コンテンツのスケジューリング、分析、自動化を行うCLIツール。

## 技術スタック

- Python 3.14
- Tweepy (Twitter API v2)
- Pydantic (データ検証)
- Typer (CLI)
- Rich (ターミナル出力)
- SQLite (データストレージ)

## インストール

```bash
# 仮想環境の作成
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows

# パッケージのインストール
uv pip install -e .
```

または、システム全体にインストールする場合：

```bash
pipx install social-media-automation
```

## 初期設定

```bash
# 設定ファイルの作成
social-media-automation init

# .envファイルを編集してAPIキーを設定
nano .env
```

### 環境変数の設定

```env
# Twitter/X API Credentials
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_secret_here

# Bluesky Credentials (optional)
BLUESKY_HANDLE=your_handle.bsky.social
BLUESKY_APP_PASSWORD=your_app_password_here

# LinkedIn Credentials (optional)
LINKEDIN_ACCESS_TOKEN=your_access_token_here

# Database
DB_PATH=./data/social_media.db
```

## 使用方法

### 基本操作

#### 初期化

```bash
social-media-automation init
```

#### 投稿の作成

```bash
# ツイートの投稿
social-media-automation post "Hello, world!"

# 特定のプラットフォームに投稿
social-media-automation post "Hello from Bluesky!" --platform bluesky
```

### ドラフト管理

#### ドラフトの作成

```bash
# ドラフトの作成
social-media-automation draft create --platform x --content "Draft content"

# ファイルからドラフトを作成
social-media-automation draft create --platform x --file draft.txt
```

#### ドラフトの一覧表示

```bash
social-media-automation draft list
```

#### ドラフトの表示

```bash
social-media-automation draft show 1
```

#### ドラフトの編集

```bash
social-media-automation draft edit 1 --content "Updated content"
```

#### ドラフトの削除

```bash
social-media-automation draft delete 1
```

### スケジュール管理

#### 投稿のスケジュール

```bash
# 特定時刻に投稿をスケジュール
social-media-automation schedule "Hello at 9 AM!" --schedule 2026-03-14T09:00:00

# ドラフトをスケジュール
social-media-automation schedule "Content" --schedule 2026-03-14T09:00:00 --platform x
```

#### スケジュールの一覧表示

```bash
social-media-automation schedule list
```

#### スケジュールのキャンセル

```bash
social-media-automation schedule cancel 1
```

### テンプレート管理

#### テンプレートの作成

```bash
# テンプレートの作成（変数の自動抽出）
social-media-automation template create --name greeting --platform x \
  --content "Hello {{name}}, welcome to {{company}}!"

# ファイルからテンプレートを作成
social-media-automation template create --name greeting --platform x \
  --file template.txt
```

#### テンプレートの一覧表示

```bash
social-media-automation template list
```

#### テンプレートの表示

```bash
social-media-automation template show 1
```

#### テンプレートの使用

```bash
# JSON形式で変数を渡す
social-media-automation template use greeting '{"name":"John","company":"Acme"}' --output

# key=value形式で変数を渡す
social-media-automation template use greeting "name=Jane company=Acme" --output

# ドラフトとして保存
social-media-automation template use greeting "name=Bob company=XYZ" --save

# スケジュールして保存
social-media-automation template use greeting "name=Alice company=ABC" --save \
  --schedule 2026-03-14T09:00:00
```

#### テンプレートの削除

```bash
social-media-automation template delete 1
```

### タイムライン管理

#### ホームタイムラインの取得

```bash
social-media-automation timeline home
```

#### ユーザータイムラインの取得

```bash
social-media-automation timeline user username
```

### インタラクション

#### リプライ

```bash
social-media-automation reply <tweet_id> "Great post!"
```

#### リツイート

```bash
social-media-automation retweet <tweet_id>
```

#### いいね

```bash
social-media-automation like <tweet_id>
```

#### メンションの取得

```bash
social-media-automation mentions
```

### 認証管理

#### 認証状態の表示

```bash
social-media-automation auth status
```

#### ログイン

```bash
social-media-automation auth login
```

#### ログアウト

```bash
social-media-automation auth logout
```

### 設定

#### 設定の表示

```bash
social-media-automation config:show
```

### APIレート制限

#### レート制限の確認

```bash
social-media-automation rate-limit
```

## 機能一覧

### 実装済み機能

- ✅ 複数プラットフォーム対応（X/Twitter）
- ✅ 投稿の即時実行とスケジューリング
- ✅ ドラフト管理（作成、編集、削除、表示）
- ✅ テンプレート管理（作成、使用、削除、変数の自動抽出）
- ✅ 定期投稿のスケジューリング
- ✅ タイムラインの取得
- ✅ インタラクション機能（リプライ、リツイート、いいね）
- ✅ メンションの監視
- ✅ APIレート制限の管理
- ✅ OAuth 2.0認証フロー
- ✅ JSONとkey=valueの変数形式対応
- ✅ SQLiteデータベースによるデータ永続化

### 機能予定

- ⏳ Blueskyプラットフォーム対応
- ⏳ LinkedInプラットフォーム対応
- ⏳ 分析とレポート機能
- ⏳ メディアファイルのアップロード（画像、動画）
- ⏳ トレンドの監視
- ⏳ 自動返信機能
- ⏳ マルチスレッド投稿
- ⏳ コンテンツ分析

## ドキュメント

詳細なドキュメントは[docs/](docs/)ディレクトリを参照してください。

- [APIドキュメント](docs/API.md)
- [開発者ガイド](docs/DEVELOPER.md)

## テスト

```bash
# テストの実行
pytest

# カバレッジレポートの生成
pytest --cov=social_media_automation --cov-report=html
```

## 開発

### 開発環境のセットアップ

```bash
# 開発依存関係のインストール
uv pip install -e ".[dev]"

# コードフォーマット
black social_media_automation/

# 型チェック
mypy social_media_automation/
```

### プロジェクト構成

```
social-media-automation/
├── social_media_automation/
│   ├── __init__.py
│   ├── cli.py                 # メインCLIインターフェース
│   ├── config.py              # 設定管理
│   ├── core/
│   │   ├── content_manager.py # コンテンツ管理
│   │   ├── scheduler.py        # スケジューラー
│   │   ├── template_manager.py # テンプレート管理
│   │   ├── rate_limiter.py     # レート制限管理
│   │   └── oauth.py           # OAuth 2.0認証
│   ├── storage/
│   │   ├── database.py        # SQLiteデータベース
│   │   └── template_store.py  # テンプレートストア
│   ├── platforms/
│   │   └── x/
│   │       └── client.py      # Twitter APIクライアント
│   └── tests/                 # テスト
├── docs/                      # ドキュメント
└── tests/                     # 統合テスト
```

## トラブルシューティング

### APIエラー

```
✗ Error: Twitter API error: 429 Too Many Requests
```

レート制限に達した場合は、`rate-limit`コマンドで状況を確認し、しばらく待ってから再試行してください。

### 認証エラー

```
✗ Error: Twitter API error: 401 Unauthorized
```

`.env`ファイルのAPIキーを確認し、正しく設定されているか確認してください。

### テンプレート変数エラー

```
✗ Validation error: Missing required variables
```

テンプレートに必要な変数を確認するには、`template show <template_id>`コマンドを使用してください。

## ライセンス

MIT

## コントリビューション

コントリビューションを歓迎します！詳細は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## サポート

問題や質問がある場合は、[GitHub Issues](https://github.com/yourusername/social-media-automation/issues)を開いてください。
