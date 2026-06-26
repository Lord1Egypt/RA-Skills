# Resume/ATS Optimization

OpenClawスキル - レジュメとATSの最適化ツール

## 概要

レジュメの構造化、キーワード最適化、フォーマット調整、セクションの整理を行い、ATS（Applicant Tracking System）でのスコアリングを向上させるCLIツール。

## 技術スタック

- Python 3.14
- Pydantic（データ検証）
- Typer（CLI）
- Rich（ターミナル出力）
- PyPDF2（PDF解析）

## インストール

```bash
# 仮想環境の作成
python -m venv .venv
source .venv/bin/activate

# パッケージのインストール
uv pip install -e .
```

## 使用方法

### 初期設定

```bash
resume-ats init
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

### キーワード最適化

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

## 設定

環境変数または設定ファイルで設定します。

## 機能一覧

### 実装済み機能
- ✅ プロジェクト構築
- ✅ 依存関係の設定
- ✅ 基本的なCLIフレームワーク
- ✅ 設定管理

### 機能予定
- ⏳ PDF解析エンジン
- ⏳ ATSスコアリング
- ⏳ キーワード抽出と最適化
- ⏳ レジュメテンプレート
- ⏳ レジュメ生成
- ⏳ 複数フォーマット対応
- ⏳ セクションの自動整理

## ドキュメント

詳細なドキュメントは[docs/](docs/)ディレクトリを参照してください。

## テスト

```bash
# テストの実行
pytest

# カバレッジレポートの生成
pytest --cov=resume_ats --cov-report=html
```

## ライセンス

MIT
