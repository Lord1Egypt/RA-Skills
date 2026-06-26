---
name: pdf-reader
description: Reads PDF files and extracts text content in Markdown format. Handles tables and multi-page documents. Use when needing to read PDF documents. Requires pdfplumber package.
---

# PDF Reader

PDF ファイルをテキスト抽出して Markdown 形式に変換するスキルです。

## クイックスタート

### 基本的な使い方

```bash
# WSL環境でPythonスクリプトを実行
wsl python3 scripts/read_pdf.py "/mnt/c/path/to/file.pdf"
```

### Markdown形式で保存

1. スクリプトでテキスト抽出
2. Write ツールで .md ファイルに保存

## 前提条件

pdfplumber パッケージが必要です：

```bash
wsl pip3 install pdfplumber
```

## 使用例

### 例1: PDF ファイルを読み込んで内容を表示

```
User: "C:\Users\keita\repos\guideline.pdf を読み込んで"
Assistant:
1. Windowsパスを WSL パスに変換: /mnt/c/Users/keita/repos/guideline.pdf
2. wsl python3 scripts/read_pdf.py を実行
3. 抽出されたテキストを Markdown 形式で表示
```

### 例2: PDF を Markdown に変換して保存

```
User: "ガイドライン.pdf を Markdown に変換して保存"
Assistant:
1. scripts/read_pdf.py でテキスト抽出
2. Markdown形式で構造化（ページごとに見出し、テーブルも含む）
3. Write ツールで ガイドライン.md に保存
4. 保存完了を報告
```

## ワークフロー

### 単一ファイルの読み込み

1. ユーザーが PDF ファイルパスを指定
2. Windows パスを WSL パス形式に変換 (`C:\` → `/mnt/c/`)
3. `wsl python3 scripts/read_pdf.py` を実行
4. 抽出されたテキストを Markdown 形式で表示または保存

### 複数ファイルの一括処理

1. Glob で .pdf ファイルを検索
2. 各ファイルに対してスクリプトを実行
3. 結果をまとめて報告

## 出力形式

### Markdown 構造

```markdown
# [PDFファイル名]

**Total Pages:** 10

---

## Page 1

[ページ1のテキスト内容]

### Tables

**Table 1:**

| 列1 | 列2 | 列3 |
| --- | --- | --- |
| データ1 | データ2 | データ3 |

---

## Page 2

[ページ2のテキスト内容]

---
```

## スクリプト詳細

Python スクリプトは `scripts/read_pdf.py` に配置されています。

**主な機能:**
- ページごとのテキスト抽出
- テーブルの Markdown 化
- 複数ページの構造化
- エラーハンドリング

**使い方:**
```bash
python scripts/read_pdf.py <file_path>
```

## 対応機能

- ✅ テキスト抽出（全ページ）
- ✅ テーブルの Markdown 化
- ✅ ページ番号の保持
- ✅ 構造化された出力
- ⚠️ 画像からのテキスト抽出（OCR未対応）
- ⚠️ 複雑なレイアウトは簡略化

## 制限事項

- スキャンされた PDF（画像のみ）からはテキスト抽出不可
- OCR 機能は含まれません
- 複雑なレイアウトは簡略化されます
- フォント情報、色などのスタイルは失われます
- 埋め込みオブジェクトは抽出されません

## トラブルシューティング

### pdfplumber がインストールされていない

```bash
wsl pip3 install pdfplumber
```

### テキストが抽出されない

- PDF がスキャン画像の可能性があります（OCR が必要）
- PDF が暗号化されている可能性があります
- テキストレイヤーがない PDF かもしれません

### 文字化けする

```bash
# 日本語対応の確認
wsl locale
# UTF-8 が含まれていることを確認
```

### メモリ不足エラー

大きな PDF ファイルの場合、ページごとに分割して処理することを検討してください。

## パス変換

Windows パスから WSL パスへの変換：

- `C:\Users\...` → `/mnt/c/Users/...`
- `D:\Projects\...` → `/mnt/d/Projects/...`
- バックスラッシュ `\` をスラッシュ `/` に変換

## 関連ツール

- **PyPDF2**: 軽量な代替ライブラリ
- **pdfminer.six**: より詳細な制御が必要な場合
- **Camelot**: テーブル抽出特化
- **OCRmyPDF**: スキャン PDF に OCR を適用

## 高度な使い方

### 特定のページのみ抽出

スクリプトを修正して `pdf.pages[0:5]` のようにスライスを使用できます。

### テーブルのみ抽出

スクリプト内の `extract_tables()` 部分のみを使用します。

### OCR が必要な場合

pytesseract と pdf2image を組み合わせて使用します（別スキルとして作成推奨）。

## バージョン履歴

- v1.0.0 (2026-01-06): 初期リリース
  - 基本的なテキスト抽出機能
  - テーブル Markdown 化対応
  - WSL環境での動作
  - ページごとの構造化
