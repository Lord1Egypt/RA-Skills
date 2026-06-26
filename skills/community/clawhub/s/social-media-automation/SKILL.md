# Social Media Automation

Multi-platform social media management tool for automated posting, scheduling, and analytics.

## 概要

複数のSNSプラットフォーム（X/Twitter, Bluesky, LinkedInなど）を一元管理し、コンテンツのスケジューリング、分析、自動化を行うCLIツール。

## 主な機能

- 複数プラットフォーム対応（X/Twitter）
- 投稿の即時実行とスケジューリング
- ドラフト管理
- テンプレート管理（変数の自動抽出と適用）
- 定期投稿のスケジューリング
- タイムラインの取得
- インタラクション機能（リプライ、リツイート、いいね）
- メンションの監視
- APIレート制限の管理
- OAuth 2.0認証フロー
- SQLiteデータベースによるデータ永続化

## インストール

```bash
cd ~/.openclaw/workspace/skills/social-media-automation
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

または

```bash
pipx install social-media-automation
```

## 使用方法

### 初期設定

```bash
# 設定ファイルの作成
social-media-automation init

# .envファイルを編集してAPIキーを設定
nano .env
```

### 基本的な操作

```bash
# ツイートの投稿
social-media-automation post "Hello, world!"

# 特定のプラットフォームに投稿
social-media-automation post "Hello from Bluesky!" --platform bluesky

# スケジュールされた投稿の確認
social-media-automation schedule list
```

### ドラフト管理

```bash
# ドラフトの作成
social-media-automation draft create --platform x --content "Draft content"

# ドラフトの一覧表示
social-media-automation draft list

# ドラフトの表示
social-media-automation draft show 1

# ドラフトの編集
social-media-automation draft edit 1 --content "Updated content"

# ドラフトの削除
social-media-automation draft delete 1
```

### スケジュール管理

```bash
# 投稿のスケジュール
social-media-automation schedule "Hello at 9 AM!" --schedule 2026-03-14T09:00:00

# スケジュールの一覧表示
social-media-automation schedule list

# スケジュールのキャンセル
social-media-automation schedule cancel 1

# 定期スケジュールの追加
social-media-automation schedule recurring add --platform x --content "Daily post" --type daily --start-time "09:00"

# 定期スケジュールの一覧
social-media-automation schedule recurring list

# 定期スケジュールの削除
social-media-automation schedule recurring remove 1
```

### テンプレート管理

```bash
# テンプレートの作成（変数の自動抽出）
social-media-automation template create --name greeting --platform x \
  --content "Hello {{name}}, welcome to {{company}}!"

# テンプレートの一覧表示
social-media-automation template list

# テンプレートの表示
social-media-automation template show 1

# テンプレートの使用（JSON形式で変数を渡す）
social-media-automation template use greeting '{"name":"John","company":"Acme"}' --output

# テンプレートの使用（key=value形式で変数を渡す）
social-media-automation template use greeting "name=Jane company=Acme" --output

# テンプレートからドラフト作成
social-media-automation template use greeting "name=Bob company=XYZ" --save

# テンプレートの削除
social-media-automation template delete 1
```

### タイムライン管理

```bash
# ホームタイムラインの取得
social-media-automation timeline home

# ユーザータイムラインの取得
social-media-automation timeline user username
```

### インタラクション

```bash
# リプライ
social-media-automation reply <tweet_id> "Great post!"

# リツイート
social-media-automation retweet <tweet_id>

# いいね
social-media-automation like <tweet_id>

# メンションの取得
social-media-automation mentions
```

### 認証管理

```bash
# 認証状態の表示
social-media-automation auth status

# ログイン
social-media-automation auth login

# ログアウト
social-media-automation auth logout
```

### レート制限の確認

```bash
# レート制限の確認
social-media-automation rate-limit
```

### 設定の表示

```bash
# 設定の表示（機密データは表示されません）
social-media-automation config:show
```

## コマンド一覧

- `init` - 設定の初期化
- `post` - コンテンツの投稿
- `draft create` - ドラフトの作成
- `draft list` - ドラフトの一覧
- `draft show` - ドラフトの表示
- `draft edit` - ドラフトの編集
- `draft delete` - ドラフトの削除
- `schedule` - スケジュール管理
- `schedule list` - スケジュールの一覧
- `schedule cancel` - スケジュールのキャンセル
- `schedule recurring` - 定期スケジュール管理
- `template create` - テンプレートの作成
- `template list` - テンプレートの一覧
- `template show` - テンプレートの表示
- `template use` - テンプレートの使用
- `template delete` - テンプレートの削除
- `timeline` - タイムライン管理
- `reply` - リプライ
- `retweet` - リツイート
- `like` - いいね
- `mentions` - メンションの取得
- `auth` - 認証管理
- `rate-limit` - レート制限の確認
- `config:show` - 設定の表示

## 技術スタック

- Python 3.14
- Tweepy (Twitter API v2)
- Pydantic (データ検証)
- Pydantic-Settings (設定管理)
- Typer (CLI)
- Rich (ターミナル出力)
- SQLite (データストレージ)

## 環境変数

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

## テスト

```bash
# テストの実行
pytest

# カバレッジレポートの生成
pytest --cov=social_media_automation --cov-report=html
```

現在のテストカバレッジ: 60%

## 依存関係

- tweepy>=4.14.0
- pydantic>=2.0.0
- pydantic-settings>=2.0.0
- typer>=0.12.0
- rich>=13.0.0
- pyyaml>=6.0.0
- python-dotenv>=1.0.0

## 開発依存関係

- pytest>=7.4.0
- pytest-cov>=4.1.0
- pytest-mock>=3.12.0
- black>=23.0.0
- mypy>=1.5.0

## 注意事項

- Twitter APIには有効な認証情報が必要
- APIレート制限に注意してください
- 環境変数または.envファイルで設定を行ってください

## ライセンス

MIT
