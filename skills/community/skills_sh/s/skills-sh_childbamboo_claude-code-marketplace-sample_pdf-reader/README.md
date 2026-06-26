# PDF Reader Skill

PDF ファイルをテキスト抽出して Markdown 形式に変換するスキルです。

## ファイル構成

```
pdf-reader/
├── SKILL.md           # メインスキル定義（Claude が読む）
├── README.md          # このファイル（人間向けドキュメント）
└── scripts/
    └── read_pdf.py    # テキスト抽出用 Python スクリプト
```

## インストール

### 前提条件

- WSL (Windows Subsystem for Linux)
- Python 3.x
- pdfplumber パッケージ

### セットアップ

```bash
# pdfplumber のインストール
wsl pip3 install pdfplumber
```

## 使い方

Claude に以下のように依頼します：

```
「C:\Users\keita\repos\guideline.pdf を読み込んで」
```

Claude が自動的に：
1. Windows パスを WSL パスに変換
2. スクリプトを実行してテキスト抽出
3. Markdown 形式で構造化
4. 結果を表示または Markdown ファイルとして保存

## スクリプトの直接実行

```bash
# 基本的な使い方
wsl python3 scripts/read_pdf.py "/mnt/c/path/to/file.pdf"

# 出力をファイルに保存
wsl python3 scripts/read_pdf.py "/mnt/c/path/to/file.pdf" > output.md
```

## 機能

### テキスト抽出

- ✅ 全ページからテキスト抽出
- ✅ ページごとに構造化
- ✅ 見出しとして整理
- ❌ OCR 機能（未対応）

### テーブル処理

- ✅ テーブルの自動検出
- ✅ Markdown テーブル形式に変換
- ✅ 複数テーブルの処理
- ⚠️ 複雑なレイアウトは簡略化

### 出力形式

- ✅ Markdown 形式
- ✅ ページ番号付き
- ✅ 階層構造
- ✅ テーブル対応

## 出力例

```markdown
# document.pdf

**Total Pages:** 3

---

## Page 1

これはページ1のテキスト内容です。

### Tables

**Table 1:**

| ヘッダー1 | ヘッダー2 | ヘッダー3 |
| --- | --- | --- |
| データ1 | データ2 | データ3 |

---

## Page 2

これはページ2のテキスト内容です。

---
```

## トラブルシューティング

### pdfplumber が見つからない

```bash
wsl pip3 install pdfplumber
```

### テキストが抽出できない

**原因1: スキャン画像 PDF**
- OCR が必要です
- 対策: OCR ツールで前処理するか、OCR 対応の別スキルを使用

**原因2: 暗号化された PDF**
- パスワード保護されている
- 対策: パスワードを解除してから実行

**原因3: テキストレイヤーがない**
- PDF にテキスト情報が埋め込まれていない
- 対策: OCR を使用

### 文字化けする

```bash
# ロケール設定を確認
wsl locale

# 必要に応じて UTF-8 を設定
export LANG=ja_JP.UTF-8
```

### 大きな PDF でメモリ不足

- ページ数が多い場合は分割処理を検討
- スクリプトを修正してページ範囲を指定

## 開発

### スクリプトの修正

`scripts/read_pdf.py` を編集して機能を追加・修正できます。

### カスタマイズ例

#### 特定ページのみ抽出

```python
# ページ 1-5 のみ抽出
for page_num, page in enumerate(pdf.pages[0:5], start=1):
    ...
```

#### テーブルのみ抽出

```python
# テキストを無視してテーブルのみ
tables = page.extract_tables()
```

### テスト

```bash
# テスト用の PDF ファイルで動作確認
wsl python3 scripts/read_pdf.py "/mnt/c/path/to/test.pdf"
```

## 関連スキル

- **docx-reader**: Word 文書の読み込み
- **ocr-reader** (未作成): スキャン画像からのテキスト抽出

## 技術詳細

### 使用ライブラリ

- **pdfplumber**: PDF からのテキスト・テーブル抽出
  - 高精度なテキスト抽出
  - テーブル構造の保持
  - ページレイアウトの解析

### アルゴリズム

1. PDF ファイルを開く
2. 各ページを順に処理
3. テキストを抽出
4. テーブルを検出・抽出
5. Markdown 形式に整形
6. 全体を結合

## 制限事項

- スキャン画像 PDF は非対応（OCR 必要）
- 複雑なレイアウトは簡略化される
- 画像、図形は抽出されない
- フォント・色などのスタイル情報は失われる
- 巨大な PDF はメモリ制約に注意

## ライセンス

このスキルは個人プロジェクト用です。

## バージョン

- **v1.0.0** (2026-01-06)
  - 初期リリース
  - 基本的なテキスト抽出機能
  - テーブル Markdown 化
  - WSL環境での動作確認済み
  - ページごとの構造化出力
