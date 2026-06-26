---
name: slide-creator
description: AIを使った資料作成ワークフロー。Gemini Gem × Claude Code × Slidevでプロ級スライドを作る。AI感を徹底排除するための鉄則を含む。コムギさんが「資料を作りたい」「スライド作って」と言ったら必ずこのスキルを使う。GemのURLを先に案内してからSTEP1に入ること。
---

# slide-creator — AIスライド作成ワークフロー

---

## ⚠️ 必ず最初にこのURLを案内する

資料作成を頼まれたら、**作り始める前に**まずこれを送る：

```
資料作成のフローを案内します！

【STEP 1】構成案を作る
▶ 構成Gem: https://gemini.google.com/gem/1n4WJG5tY6MlVpO2qM5PghGoNxY99z5v0
→「スタート」と入力 → 資料を入力 → 3つの質問に答える

【STEP 2】デザインプロンプトを作る
▶ デザインGem: https://gemini.google.com/gem/1iLz7X88qkvl4hhT98AD8eEfHL8ptOVAC
→ 雰囲気・参考資料を入力 → 20項目デザインプロンプト完成

【STEP 3】キャラクター素材を用意する（推奨）
→ DALL-E / Midjourney でキャラクター画像を生成して送ってください

【STEP 4】私に送ってください
① 構成案テキスト
② デザインプロンプト（20項目）
③ キャラクター画像（あれば）
④ 補足（クライアント名・目的）
```

---

## AI感を排除するための絶対ルール

### ❌ 絶対禁止
- **絵文字・記号をスライド本文に使わない**（🎯📊✅💡🚀など一切NG）
- **テキストの装飾記号を使わない**（→ ◆ ■ ▶ ・ などの多用NG）
- **デフォルトフォントのまま使わない**（Slidevデフォルトは必ず上書き）
- **等幅・均一なレイアウトにしない**（全スライド同じ構造はAI感の原因）
- **情報を詰め込まない**（1スライド1メッセージ厳守）
- **SVGを単純な四角・丸で構成しない**（幾何学形状の羅列はAI感が出る）

### ✅ 必ずやること

#### フォント
```css
/* Google Fonts から本格的な組み合わせを読み込む */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Zen+Kaku+Gothic+New:wght@700;900&display=swap');

/* 見出し: 極太（900）でインパクト */
.heading { font-family: 'Zen Kaku Gothic New', sans-serif; font-weight: 900; }

/* 本文: 細め（300〜400）で余白を感じさせる */
.body { font-family: 'Noto Sans JP', sans-serif; font-weight: 300; }
```

#### タイポグラフィの対比
- 見出しと本文で**フォントウェイトを極端に変える**（900 vs 300）
- 見出しは大きく（60〜80pt相当）、本文は小さく抑える
- 行間（line-height）は1.8以上を本文に設定
- 文字間隔（letter-spacing）を見出しに-0.02em〜適度に設定

#### SVGアニメーション（本格的なもの）
```html
<!-- 単純なfadeではなく、パスドローイングやモーフィングを使う -->
<svg viewBox="0 0 200 200">
  <!-- パスドローイングアニメーション -->
  <path d="M10,100 Q100,10 190,100" stroke="#e63946" fill="none" stroke-width="2"
    stroke-dasharray="300" stroke-dashoffset="300">
    <animate attributeName="stroke-dashoffset" from="300" to="0" dur="1.5s" fill="freeze"/>
  </path>
  <!-- グラデーションマスクを使った表示 -->
  <defs>
    <linearGradient id="grad" x1="0%" x2="100%">
      <stop offset="0%" style="stop-color:#a855f7"/>
      <stop offset="100%" style="stop-color:#e879f9"/>
    </linearGradient>
  </defs>
</svg>

<!-- スクロールトリガーアニメーション（Intersection Observer） -->
<script>
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => e.isIntersecting && e.target.classList.add('visible'));
});
</script>
```

#### レイアウトの非対称性
- 全スライド同じレイアウトにしない
- 左右の重さを意図的にずらす（テキスト左寄り、ビジュアル右に大きく）
- 余白は「多すぎるくらい」で良い
- グリッドは12カラムを使い、カラムスパンを変える

---

## Claude Codeへのプロンプト鉄則

Claude Codeに渡すプロンプトには必ず以下を含める：

```
【デザイン品質の絶対要件】

1. 絵文字・装飾記号（→ ◆ ■ など）をスライド本文で使わないこと
2. フォントは必ずGoogle Fontsを読み込み、見出し極太（900）・本文細め（300）の対比をつけること
3. SVGアニメーションはパスドローイング・モーフィング・Intersection Observerを使うこと
4. 各スライドのレイアウトを変える（全スライド同じ構造にしない）
5. 余白を大胆に取る（窮屈な印象を絶対に作らない）
6. 色は指定パレットのみ使用し、グラデーションを積極活用する
7. キャラクター画像がある場合は、コンテンツの一部として意味のある配置をすること
8. 完成後、スライドを見て「AI感がないか」を自己チェックしてから報告すること
```

---

## ワークフロー全体

```
コムギさん
  ↓ 「資料作りたい」
URL案内（Gem2本）
  ↓
STEP 1: 構成Gem → 構成案
  ↓
STEP 2: デザインGem → デザインプロンプト20項目
  ↓
STEP 3: 画像生成AI → キャラクター素材（任意・推奨）
  ↓
STEP 4: 3〜4点を私（ポニョ）に送る
  ↓
STEP 5: Claude Code → Slidev HTML 生成
        ※ AI感排除ルールをプロンプトに含める
  ↓
STEP 6: ブラウザで全スライドスクリーンショット
  ↓
STEP 7: PDF化 → Telegram に1ファイルで送信（filePath使用）
  ↓
STEP 8: （希望時）Google Drive にもアップ
```

---

## STEP 5｜Claude Code 実行

```bash
WORK="/Users/meruemu/.openclaw/workspace/slides/<資料名>"
mkdir -p "$WORK" && cd "$WORK" && git init -q

/Users/meruemu/.local/bin/claude --dangerously-skip-permissions --print '
<構成案・デザインプロンプト・補足>

【デザイン品質の絶対要件】
1. 絵文字・装飾記号をスライド本文で使わない
2. フォントはGoogle Fonts（見出し:Zen Kaku Gothic New 900、本文:Noto Sans JP 300）
3. SVGはパスドローイング・モーフィングアニメーションを使う
4. 各スライドのレイアウトを変える
5. 余白を大胆に取る
6. 完成後にnpm run buildを実行

完了後: openclaw system event --text "スライド完了: <資料名>" --mode now
'
```

---

## STEP 6〜7｜スクリーンショット → PDF → Telegram

```bash
# サーバー起動
cd /Users/meruemu/.openclaw/workspace/slides/<資料名>/dist
python3 -m http.server 9877 &

# browser ツールで各スライドをスクリーンショット → slide{N}.png に保存

# PIL でPDF化
python3 << 'EOF'
from PIL import Image
images = [Image.open(f"/Users/meruemu/.openclaw/media/slides/slide{i}.png").convert("RGB") for i in range(1, <N+1>)]
images[0].save("/Users/meruemu/.openclaw/workspace/slides/<資料名>.pdf", save_all=True, append_images=images[1:])
EOF

# Telegram に1ファイルで送信
# message tool: filePath, caption付き
```

---

## STEP 8｜Google Drive（希望時）

```bash
GOG_KEYRING_PASSWORD=openclaw_gog_2026 GOG_ACCOUNT=bestgrp0604@gmail.com \
gog drive upload /tmp/<資料名>.zip \
  --name "<資料名>.zip" \
  --parent 1yoqOZt1QJ9mWiejGabAeNxdGSB8QU2k1

gog drive share <fileId> --to anyone --role reader
```

---

## 仕様まとめ

| 項目 | 内容 |
|---|---|
| 出力フォーマット | Slidev HTML → PDF（Telegram送信） |
| 作成エンジン | Claude Code（/Users/meruemu/.local/bin/claude） |
| スクリーンショット | browser ツール |
| PDF化 | Python PIL（Pillow） |
| Telegram送信 | message tool filePath で1ファイル送信 |
| Google Drive保存先 | フォルダID: 1yoqOZt1QJ9mWiejGabAeNxdGSB8QU2k1 |
| 渡す情報 | 構成案 + デザインプロンプト + キャラ画像（任意） + 補足 |

---

## 学習ログ（2026-03-04）

- **絵文字・記号禁止**: AIが生成しやすい絵文字は人間らしさを損なう
- **フォントウェイトの対比**: 900 vs 300の組み合わせで一気にプロ感が出る
- **SVGアニメーション**: パスドローイング・モーフィング・Intersection Observerを使うと本格的
- **レイアウトの非対称**: 全スライド同じ構造はAI感の最大原因
- **キャラクターは画像生成AIで**: Claude CodeのSVGキャラはAI感が強い
- **参考PDF**: ウォームベージュ背景・赤×白・3D猫キャラ・大きな見出し・余白たっぷり
- **Telegram配信**: 写真でなくfilePath（ファイル送信）で1枚PDFが最も使いやすい
