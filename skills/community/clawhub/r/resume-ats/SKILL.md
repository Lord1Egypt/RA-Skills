# Resume/ATS Optimization

Resume structuring, keyword optimization, format adjustment, and ATS scoring improvement tool.

## 概要

レジュメの構造化、キーワード最適化、フォーマット調整、セクションの整理を行い、ATS（Applicant Tracking System）でのスコアリングを向上させるCLIツール。

## 主な機能

- PDFおよびテキストファイルの解析
- ATSスコアの計算
- キーワードの抽出と比較
- レジュメのテンプレート生成
- 複数フォーマット対応
- セクションの自動整理
- 仕事記述とのキーワードマッチング

## インストール

```bash
cd ~/.openclaw/workspace/skills/resume-ats
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

または

```bash
pipx install resume-ats
```

## 使用方法

### 初期設定

```bash
# 設定ファイルの作成
resume-ats init

# .envファイルを編集して設定
nano .env
```

### レジュメの解析

```bash
# PDFファイルの解析
resume-ats analyze resume.pdf

# テキストファイルの解析
resume-ats analyze resume.txt
```

### ATSスコアリング

```bash
# ATSスコアの計算
resume-ats score resume.pdf job_description.txt
```

### キーワード操作

```bash
# キーワードの抽出
resume-ats keywords extract resume.pdf

# キーワードの比較
resume-ats keywords compare resume.pdf job_keywords.txt
```

### レジュメの生成

```bash
# 最適化されたレジュメの生成
resume-ats generate --template modern --input resume.txt --output optimized_resume.pdf
```

### 設定の表示

```bash
# 設定の表示
resume-ats config:show
```

## コマンド一覧

- `init` - 設定の初期化
- `analyze` - レジュメファイルの解析
- `score` - ATSスコアの計算
- `keywords` - キーワード操作（extract/compare）
- `generate` - 最適化されたレジュメの生成
- `config:show` - 設定の表示

## テンプレート

- `modern` - モダンなレジュメフォーマット
- `classic` - クラシックなレジュメフォーマット
- `minimal` - ミニマルなレジュメフォーマット

## 技術スタック

- Python 3.14
- Pydantic (データ検証)
- Pydantic-Settings (設定管理)
- Typer (CLI)
- Rich (ターミナル出力)
- PyPDF2 (PDF解析)
- PDFPlumber (PDF解析)
- PyYAML (YAML設定)
- python-dotenv (環境変数)

## 環境変数

```env
# OpenAI API (optional, for AI-powered features)
OPENAI_API_KEY=your_openai_api_key_here

# Resume Settings
DEFAULT_TEMPLATE=modern
OUTPUT_FORMAT=pdf
FONT_SIZE=11
FONT_FAMILY=Arial

# Database
DB_PATH=./data/resume_ats.db
```

## テスト

```bash
# テストの実行
pytest

# カバレッジレポートの生成
pytest --cov=resume_ats --cov-report=html
```

## 依存関係

- pydantic>=2.0.0
- pydantic-settings>=2.0.0
- typer>=0.12.0
- rich>=13.0.0
- pyyaml>=6.0.0
- python-dotenv>=1.0.0
- pypdf2>=3.0.0
- pdfplumber>=0.10.0

## 開発依存関係

- pytest>=7.4.0
- pytest-cov>=4.1.0
- black>=23.0.0
- mypy>=1.5.0

## 注意事項

- PDFファイルは解析可能な形式である必要があります
- ATSスコアはあくまで参考値です
- 仕事記述とのキーワードマッチングで最適な結果を得るには、具体的なキーワードを使用してください

## 機能予定

- PDF解析エンジンの実装
- ATSスコアリングアルゴリズムの実装
- キーワード抽出と最適化の実装
- レジュメテンプレートの実装
- 複数フォーマットの出力対応
- セクションの自動整理機能

## ライセンス

MIT
