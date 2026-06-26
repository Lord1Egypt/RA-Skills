# PDF Vision Reader Skill

図表が多い PDF を画像化して、Claude の vision 機能で内容を解析・Markdown 化するスキルです。

## ファイル構成

```
pdf-vision-reader/
├── SKILL.md              # メインスキル定義（Claude が読む）
├── README.md             # このファイル（人間向けドキュメント）
└── scripts/
    └── pdf_to_images.py  # PDF → 画像変換スクリプト
```

## インストール

### 前提条件

- WSL (Windows Subsystem for Linux)
- Python 3.x
- pdf2image パッケージ
- poppler-utils（システムパッケージ）

### セットアップ

```bash
# Python パッケージのインストール
wsl pip3 install pdf2image Pillow

# poppler-utils のインストール
wsl sudo apt-get update
wsl sudo apt-get install -y poppler-utils
```

## 使い方

Claude に以下のように依頼します：

```
「presentation.pdf を vision で解析して Markdown 化して」
```

Claude が自動的に：
1. PDF を各ページの画像に変換
2. 各画像を Claude の vision 機能で解析
3. タイトル、図表、グラフ、テキストを抽出
4. Markdown 形式で構造化
5. 結果をファイルに保存

## ワークフロー

### ステップ1: PDF を画像に変換

```bash
wsl python3 scripts/pdf_to_images.py "/mnt/c/path/to/document.pdf"
```

出力例：
```
document_pages/
├── page_001.png
├── page_002.png
├── page_003.png
└── ...
```

### ステップ2: 各画像を解析

Claude が Read ツールで各画像を読み込み、以下を抽出：
- タイトルと見出し
- 本文テキスト
- 図表の説明
- グラフやチャートのデータ
- テーブルの内容

### ステップ3: Markdown に統合

全ページの解析結果を統合して、一つの Markdown ファイルを作成。

## 機能

### 対応コンテンツ

- ✅ テキスト（日本語・英語）
- ✅ 図表・ダイアグラム（フローチャート、組織図など）
- ✅ グラフ・チャート（棒グラフ、円グラフなど）
- ✅ テーブル（Markdown テーブルに変換）
- ✅ スクリーンショット
- ✅ インフォグラフィック
- ✅ 複雑なレイアウト

### 抽出される情報

1. **テキスト情報**
   - タイトル、見出し
   - 本文、箇条書き
   - 注釈、キャプション

2. **ビジュアル要素**
   - 図の種類と説明
   - グラフのデータとトレンド
   - テーブルの構造と内容
   - レイアウトと強調箇所

## 出力例

```markdown
# プレゼンテーションタイトル

**解析日時:** 2026-01-06
**総ページ数:** 10

---

## Page 1: イントロダクション

### 概要
このページは全体の概要を説明するタイトルスライドです。

### 主要な内容
- プロジェクト名：AI-Driven Bootcamp
- 対象：新入社員向け研修プログラム
- 期間：2026年度

---

## Page 2: 市場分析

### 概要
市場規模の推移を示すグラフが中心のページ。

### 図表
**図1: 市場規模の推移（2020-2025）**
- 棒グラフで年次推移を表示
- 2020年: 100億円
- 2025年: 500億円（予測）
- 年平均成長率: 38%

### テキスト内容
市場は急速に拡大しており、今後5年間で5倍の成長が見込まれる。
```

## pdf-reader との比較

### pdf-reader (テキスト抽出)

**メリット:**
- 高速処理
- 低コスト
- テキストの正確な抽出

**デメリット:**
- 図表は抽出不可
- レイアウトは失われる
- ビジュアル要素は無視

### pdf-vision-reader (画像解析)

**メリット:**
- 図表・グラフを理解
- 複雑なレイアウトを保持
- ビジュアル要素の説明
- プレゼン資料に最適

**デメリット:**
- 処理時間が長い
- API コスト（画像解析）
- テキストの精度はやや低い

## 使い分けガイド

| PDF の種類 | 推奨スキル | 理由 |
|-----------|----------|------|
| 契約書、規約 | pdf-reader | テキスト中心 |
| 論文（図表なし） | pdf-reader | テキスト中心 |
| プレゼン資料 | **pdf-vision-reader** | 図表・ビジュアル多い |
| 技術図面 | **pdf-vision-reader** | 図が主体 |
| グラフ・チャート資料 | **pdf-vision-reader** | データビジュアライズ |
| 設計書（図表あり） | **pdf-vision-reader** | 複雑なレイアウト |

## パフォーマンス

### 処理時間

| ページ数 | 変換時間 | 解析時間 | 合計 |
|---------|---------|---------|------|
| 10ページ | ~5秒 | 30-60秒 | ~1分 |
| 30ページ | ~15秒 | 90-180秒 | ~3分 |
| 100ページ | ~50秒 | 300-600秒 | ~10分 |

### 最適化

- 重要なページのみ選択して解析
- DPI を調整（図表多い: 300 DPI、テキスト中心: 150-200 DPI）
- 大きな PDF は分割処理

## トラブルシューティング

### pdf2image が見つからない

```bash
wsl pip3 install pdf2image
```

### poppler-utils が見つからない

```bash
wsl sudo apt-get update
wsl sudo apt-get install -y poppler-utils
```

### 画像変換が失敗する

**原因と対策:**
- PDF が破損 → 別の PDF で確認
- ディスク容量不足 → 空き容量を確保
- メモリ不足 → ページ数を減らして試行

### 解析精度が低い

**改善策:**
- DPI を上げる（300 推奨）
  ```bash
  python scripts/pdf_to_images.py document.pdf ./images 300
  ```
- 元の PDF の画質を確認
- スキャン画像の場合は OCR 前処理を検討

## 開発・カスタマイズ

### スクリプトの修正

`scripts/pdf_to_images.py` を編集して機能追加可能。

### カスタマイズ例

#### 特定ページのみ変換

```python
# ページ 5-10 のみ変換
from pdf2image import convert_from_path
images = convert_from_path(pdf_path, first_page=5, last_page=10)
```

#### DPI の変更

```bash
# 高解像度（300 DPI）
python scripts/pdf_to_images.py document.pdf ./images 300
```

#### 出力形式の変更

```python
# JPEG で保存（ファイルサイズ削減）
image.save(str(image_path), "JPEG", quality=85)
```

## 技術詳細

### 使用ライブラリ

- **pdf2image**: PDF → 画像変換
  - poppler-utils のラッパー
  - 高品質な画像生成

- **Pillow**: 画像処理
  - 画像保存
  - 形式変換

### Claude Vision API

- 画像解析に Claude の vision 機能を使用
- 図表、グラフ、レイアウトを理解
- 自然言語で説明を生成

## 制限事項

- スキャン品質が低い PDF は精度低下
- 手書きメモは状況により精度が変わる
- 非常に複雑なレイアウトは簡略化される可能性
- 巨大な PDF（100ページ超）は処理時間に注意

## 関連スキル

- **pdf-reader**: テキスト中心の PDF 用
- **docx-reader**: Word 文書用

## ライセンス

このスキルは個人プロジェクト用です。

## バージョン

- **v1.0.0** (2026-01-06)
  - 初期リリース
  - PDF → 画像変換機能
  - Vision ベースの解析ワークフロー
  - 図表・グラフ・テーブルの理解
  - Markdown 出力フォーマット
