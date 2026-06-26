# DOCX Reader Skill

Microsoft Word (.docx) ファイルをテキスト形式で読み込むためのスキルです。

## ファイル構成

```
docx-reader/
├── SKILL.md           # メインスキル定義（Claude が読む）
├── README.md          # このファイル（人間向けドキュメント）
└── scripts/
    └── read_docx.py   # テキスト抽出用 Python スクリプト
```

## インストール

### 前提条件

- WSL (Windows Subsystem for Linux)
- Python 3.x
- python-docx パッケージ

### セットアップ

```bash
# python-docx のインストール
wsl pip3 install python-docx
```

## 使い方

Claude に以下のように依頼します：

```
「C:\Users\keita\repos\file.docx を読み込んで」
```

Claude が自動的に：
1. Windows パスを WSL パスに変換
2. スクリプトを実行してテキスト抽出
3. 結果を表示または Markdown ファイルとして保存

## スクリプトの直接実行

```bash
# 基本的な使い方
wsl python3 scripts/read_docx.py "/mnt/c/path/to/file.docx"

# 出力をファイルに保存
wsl python3 scripts/read_docx.py "/mnt/c/path/to/file.docx" > output.txt
```

## 機能

- ✅ 段落テキストの抽出
- ✅ テーブルデータの抽出
- ✅ エラーハンドリング
- ❌ 画像の抽出（未対応）
- ❌ スタイル情報の保持（未対応）

## トラブルシューティング

### python-docx が見つからない

```bash
wsl pip3 install python-docx
```

### "No module named 'docx'" エラー

間違ったパッケージがインストールされている可能性があります：

```bash
wsl pip3 uninstall docx
wsl pip3 install python-docx
```

## 開発

### スクリプトの修正

`scripts/read_docx.py` を編集して機能を追加・修正できます。

### テスト

```bash
# テスト用の .docx ファイルで動作確認
wsl python3 scripts/read_docx.py "/mnt/c/path/to/test.docx"
```

## ライセンス

このスキルは個人プロジェクト用です。

## バージョン

- **v1.0.0** (2026-01-06)
  - 初期リリース
  - 基本的なテキスト抽出機能
  - WSL環境での動作確認済み
