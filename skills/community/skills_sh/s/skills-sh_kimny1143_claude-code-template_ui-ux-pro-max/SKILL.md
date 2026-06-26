---
name: ui-ux-pro-max
description: "UI/UX design intelligence. Plan, build, design, implement, review, improve UI/UX code. Styles: image-first, editorial design, minimalism, dark mode, responsive. Projects: landing page, dashboard, SaaS, mobile app."
---

# UI/UX Pro Max

UI/UXデザインおよび実装の専門スキル。

**核心: 「全部ちゃんとやる」がAI生成感の正体。「何を捨てるか」がデザイン。**

## 対応領域

- ランディングページ設計
- ダッシュボードUI
- SaaSプロダクト
- モバイルアプリ（レスポンシブ）

---

## 行動原則（5つの鉄則）

### 1. 作る前に疑え

- 全要素に「本当に要る？」を問え
- 答えが曖昧なら、まず無しで作れ

### 2. 主役を1つ決めろ

- 各セクションで「一番見せたいもの」を1つだけ決めろ
- **決まるまでコードを書くな**

### 3. 70点を並べるな

- 全要素が同じ存在感 = 失敗
- 1つを120点、残りを60点にしろ

### 4. 「できます」より「やめましょう」

- 追加より削除を提案しろ
- 迷ったら削れ

### 5. 批判してから作れ

- 現状の問題点を3つ以上挙げてから改善案を出せ
- 「いい感じですね」は禁止

---

## AI生成感を避ける

### やってはいけないこと

- **全要素が同じ存在感**（均一な余白、安全な色）
- **決断の不在**（AとBどちらでも、お好みで）
- **過剰な装飾**（意味のないグラデーション、アニメーション）

### 「いい感じですね」禁止

- 完成後も「改善の余地があるとすれば〜」を添えよ
- 決断を求められたら決断せよ（根拠を添えて一つを推奨）

---

## プレミアムデザインの公式

```
Premium = (画像の質 × サイズ) + (余白) - (装飾)
```

**3つの柱:**

1. **大きな画像** - カードの70-85%を画像が占める
2. **大胆な余白** - セクション間112px以上
3. **抑制** - すべての効果に理由が必要

**参照ブランド:** Spitfire Audio, Native Instruments, iZotope

---

## 画像ガイドライン

| コンテキスト | 画像サイズ | アスペクト比 |
|-------------|-----------|-------------|
| 製品カード | カード面積の70-85% | 16:9 or 4:3 |
| ヒーローセクション | フルビューポート幅 | 可変 |
| ギャラリーグリッド | 高さ統一、幅可変 | 混合 |

**画像の扱い:**

- 画像がコンテンツの主役
- テキストは最小限（名前 + 1行説明）
- 画像上に機能リストを重ねない
- 高品質なスクリーンショット/レンダリングを使用

---

## 余白トークン

| トークン | 値 | 用途 |
|---------|-----|------|
| `--space-section` | 112px | セクション間 |
| `--space-group` | 64px | 関連コンテンツ間 |
| `--space-element` | 24px | 要素間 |

**セクションパディング:**

```css
/* プレミアムセクション */
padding-top: 112px;    /* py-28 */
padding-bottom: 112px;

/* コンパクトセクション */
padding-top: 64px;     /* py-16 */
padding-bottom: 64px;
```

**Tailwind対応:**

```tsx
// プレミアムセクション
<section className="py-28">...</section>

// コンパクトセクション
<section className="py-16">...</section>
```

---

## グリッドシステム

| 列数 | 用途 | ギャップ |
|-----|------|---------|
| 4列 | 製品ショーケース | 24px (gap-6) |
| 3列 | 機能カード、価格 | 32px (gap-8) |
| 2列 | ヒーロー、比較 | 48px (gap-12) |

---

## 視覚階層チェックリスト

### 作業開始前

- [ ] 「このセクションの主役は何か」を言語化したか
- [ ] 「削除できる要素はないか」を検討したか
- [ ] 「なぜこの色か」を説明できるか

### 作業中

- [ ] 全要素が同じ存在感になっていないか
- [ ] 視線の流れは意図通りか
- [ ] 背景がコンテンツの邪魔をしていないか

### 作業完了前

- [ ] スマホで見て3秒以内に「何をすればいいか」分かるか
- [ ] 「AI生成感」の原因がないか
- [ ] 「ここは削れたのでは」と思う要素がないか

---

## CRITICAL: アクセシビリティ優先

**このセクションは最優先事項。デザインの美しさよりもアクセシビリティを優先する。**

### WCAG 2.1 コントラスト要件

| テキストサイズ | 最小コントラスト比 |
|---------------|-------------------|
| 通常テキスト (< 18px) | **4.5:1** |
| 大きいテキスト (≥ 18px bold / ≥ 24px) | **3:1** |
| UI コンポーネント・アイコン | **3:1** |

### 必須: プロジェクトの globals.css を使用

**Tailwind のデフォルト色を直接使わない。** プロジェクトの `globals.css` で定義されたトークンを優先する。

```tsx
// NG: Tailwind デフォルトをそのまま使用
<p className="text-slate-400">...</p>
<p className="text-slate-500">...</p>

// OK: プロジェクトトークンを使用
<p className="text-muted">...</p>
<p className="text-subtle">...</p>
```

実装前に必ず `app/globals.css` を確認し、定義済みトークンを把握すること。

### バッジ・タグのコントラスト

**同系色の組み合わせは危険:**

```tsx
// NG: 同系色でコントラスト不足
<span className="bg-indigo-600/20 text-indigo-400">Badge</span>
<span className="bg-amber-500/20 text-amber-400">開発中</span>

// OK: 十分なコントラストを確保
<span className="bg-indigo-600/30 text-indigo-300">Badge</span>
<span className="bg-amber-600/30 text-amber-200">開発中</span>
```

### 無効状態のテキスト

```tsx
// NG: 薄すぎてコントラスト不足
<button className="text-white/50" disabled>...</button>

// OK: 無効でも読める濃さ
<button className="text-white/70" disabled>...</button>
```

---

## 多言語タイポグラフィ

**なぜ必要か:** 日本語は同じフォントサイズでも英語より視覚的に重く見える（画数が多いため）。同じサイズだと日本語が窮屈・重く見えるため、1段階小さくして視覚的バランスを取る。

### タイポグラフィトークン（globals.css で定義済み）

| トークン | 用途 | 英語 (デスクトップ) | 日本語 (デスクトップ) |
|---------|------|-------------------|---------------------|
| `.text-hero` | ランディングページのメインタイトル | 96px | 80px |
| `.text-section` | セクション見出し（h2） | 48px | 40px |
| `.text-headline` | 機能タイトル、製品見出し | 30px | 24px |
| `.text-subhead` | タグライン、リード文 | 24px | 20px |

### 使用方法

```tsx
// NG: Tailwind直接指定（言語による調整なし）
<h1 className="text-5xl md:text-8xl font-bold">...</h1>

// OK: トークン使用（自動で言語対応）
<h1 className="text-hero text-white">...</h1>
```

### レスポンシブ対応

トークンにはモバイル・タブレット・デスクトップのレスポンシブサイズが含まれる。追加のブレークポイント指定は不要。

```tsx
// NG: 冗長なブレークポイント指定
<h1 className="text-hero sm:text-hero md:text-hero">...</h1>

// OK: トークンのみ
<h1 className="text-hero">...</h1>
```

### 適用対象

- ランディングページの見出し（h1, h2）
- セクションタイトル
- 製品名、機能名
- タグライン、リード文

**注意:** 本文テキスト（p要素の長文）には適用しない。本文は `text-white/80` 等の通常スタイルを使用。

---

## デザイントークン遵守ルール

**原則:** Tailwindのデフォルト値を直接使用せず、`globals.css` で定義されたデザイントークンを使用する。

### 角丸（Border Radius）

| トークン | 値 | 用途 |
|---------|-----|------|
| `--radius-sm` | 8px | 小さいバッジ、タグ |
| `--radius-md` | 12px | ボタン、入力フィールド |
| `--radius-lg` | 16px | カード、モーダル |
| `--radius-full` | 999px | ピル型ボタン、アバター |

```tsx
// NG: Tailwind直接指定
<button className="rounded-lg">...</button>
<div className="rounded-xl">...</div>

// OK: トークン使用
<button className="rounded-[var(--radius-md)]">...</button>
<div className="rounded-[var(--radius-lg)]">...</div>
```

### 色

```tsx
// NG: Tailwind色を直接使用
<p className="text-slate-400">...</p>
<div className="bg-gray-900">...</div>

// OK: プロジェクトトークン使用
<p className="text-muted">...</p>
<div className="bg-mued-bg">...</div>
```

### トークン違反チェック

実装後は以下で違反を確認:

```bash
# 角丸のTailwind直接指定を検索
grep -r "rounded-sm\|rounded-md\|rounded-lg\|rounded-xl\|rounded-2xl" components/

# 色のTailwind直接指定を検索
grep -r "bg-slate-\|bg-gray-\|text-slate-\|text-gray-" components/
```

検出されたものは順次トークンに置換する。

---

## ボタンスタイル

### Primary CTA（デフォルト: 白ベース）

```tsx
<button className="bg-white text-black px-8 py-4 text-lg font-medium rounded-[var(--radius-md)] hover:bg-white/90 transition-colors cursor-pointer">
  Download Now
</button>
```

### Secondary（枠線のみ）

```tsx
<button className="border-2 border-white text-white px-8 py-4 text-lg font-medium rounded-[var(--radius-md)] hover:bg-white/10 transition-colors cursor-pointer">
  Learn More
</button>
```

### ブランド固有（限定的に使用）

色付きボタンの使用条件:
- ブランド固有セクション（MUEDear amber等）のみ
- 1ページに1-2箇所まで
- デフォルトにはしない

```tsx
// MUEDear用: amber
<button className="border-2 border-amber-500 text-amber-400 hover:bg-amber-500 hover:text-white ...">
  Download App
</button>
```

### Disabled

```tsx
<button className="bg-white/5 text-white/70 cursor-not-allowed" disabled>
  Disabled
</button>
```

---

## 背景スタイル

### 使用する背景

```tsx
// プレミアム: 単色のみ
<section className="bg-black">...</section>
<section className="bg-[#0f0f0f]">...</section>
<section className="bg-white">...</section>
```

### 避ける装飾

| パターン | 問題 | 代替案 |
|---------|------|-------|
| フローティンググローオーブ | 気が散る | 削除 |
| `bg-gradient-to-b from-violet-900/20` | 装飾的ノイズ | 単色 |
| グレインテクスチャ | 不要な複雑さ | 削除 |
| アニメーション背景 | パフォーマンス悪化 | 静的 |

---

## カードスタイル

### 画像中心カード（デフォルト）

```tsx
<div className="bg-[#0f0f0f] rounded-[var(--radius-lg)] overflow-hidden">
  {/* 画像: カードの70-85% */}
  <div className="aspect-video">
    <Image src="..." alt="..." fill className="object-cover" />
  </div>
  {/* テキスト: 最小限 */}
  <div className="p-6">
    <h3 className="text-white text-lg font-medium">製品名</h3>
    <p className="text-white/60 text-sm">一行の説明</p>
  </div>
</div>
```

### Glass Card（限定的に使用）

**注意:** Glassmorphism は特定のコンテキスト（価格表、機能比較など）でのみ使用。デフォルトにしない。

```tsx
<div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-[var(--radius-lg)] p-6">
  <h3 className="text-white font-semibold">Title</h3>
  <p className="text-white/80">Description</p>
</div>
```

**Glass Card 使用時の注意:**
- テキストは `text-white` または `text-white/80` 以上
- `text-slate-*` や `text-gray-*` は使用しない
- 背景が半透明なためコントラスト計算が複雑

---

## 指示エスカレーションプロトコル

ユーザーの表現に応じて対応レベルを変える:

| ユーザーの表現 | 解釈 | 必要な対応 |
|--------------|------|-----------|
| 「Spitfireレベル」「Native Instrumentsレベル」 | 全面的な視覚改修 | 微調整ではなく完全リデザイン |
| 「もっとプレミアムに」 | 実質的な変更 | 効果を削除、余白を増加 |
| 「クリーンに」 | 中程度のクリーンアップ | 装飾要素の30%削除 |
| 「調整」「微調整」 | 小さな修正 | CSS変更のみ |

**重要ルール:** 参照ブランドが名指しされたら、提案前に現在の実装をそのブランドと比較すること。

---

## 実装チェックリスト

### 実装前チェック

- [ ] 高品質な製品スクリーンショットはあるか？
- [ ] テキストを50%削減できるか？
- [ ] 参照したい美的水準を確認したか？
- [ ] その抑制レベルに合わせているか？

### 実装中チェック

| 質問 | 「No」の場合のアクション |
|------|------------------------|
| セクションパディング >= 100px？ | `py-28`以上に増加 |
| 画像がカード面積の60%以上？ | 画像を拡大 |
| ボタンは白または枠線のみ？ | 色付きから変更 |
| 背景は単色（グラデーションなし）？ | 装飾要素を削除 |

### 実装後チェック

1. **スキントテスト:** 目を細めて見る。製品を識別できるか？効果が支配的なら削減。
2. **「1つ削除」テスト:** 各セクションから1要素削除。まだ機能するか？機能するなら不要だった。
3. **Spitfire比較:** スクリーンショットをSpitfire.comと並べる。視覚的「重さ」は似ているか？

---

## 避けるべきパターン（明示的禁止リスト）

> "Claude defaults to safe choices" - 明示的に禁止しないと汎用的な選択に収束する

### 背景・装飾

| 禁止パターン | 問題 | 代替案 |
|-------------|------|-------|
| `bg-white/5 backdrop-blur-xl` 多用 | 「2023テンプレート」感 | `bg-black` or `bg-[#0f0f0f]` |
| `bg-gradient-to-b from-violet-900/20` | 装飾的ノイズ | 削除 |
| `bg-gradient-to-br from-indigo-500/10` | 同上 | 削除 |
| アニメーションブロブ背景 | 気が散る、パフォーマンス悪化 | 静的、単色 |
| グレインテクスチャ (`noise.svg`) | 不要な複雑さ | 削除 |
| フローティンググローオーブ | 2020年代前半のトレンド | 削除 |

### 影・グロー

| 禁止パターン | 問題 | 代替案 |
|-------------|------|-------|
| `shadow-lg shadow-indigo-500/20` | 人工的な「ポップ」 | 影なし or `shadow-sm shadow-black/20` |
| `shadow-xl shadow-violet-500/30` | 同上 | 同上 |
| `shadow-2xl shadow-amber-500/25` | 同上 | 同上 |
| `hover:shadow-*-500/40` | ホバー時のグロー強調 | `hover:bg-white/10` など控えめに |
| `drop-shadow-[0_0_*px_rgba()]` | カスタムグロー | 削除 |

### レイアウト

| 禁止パターン | 問題 | 代替案 |
|-------------|------|-------|
| アイコン付き3列機能グリッド | 汎用SaaSデザイン | 大きな画像 + 最小テキスト |
| 均等な3列カード（同サイズ） | 「全部同じ存在感」 | 1つを大きく、残りを小さく |
| `py-12` 以下のセクション間隔 | 窮屈 | `py-28` (112px) 以上 |
| 中央寄せのすべて | 安全すぎる | 左寄せ or 非対称を検討 |

### コンポーネント

| 禁止パターン | 問題 | 代替案 |
|-------------|------|-------|
| `hover:scale-105` + `hover:shadow-*` | 過剰なホバーエフェクト | `hover:bg-white/10` のみ |
| `transition-all duration-300` | 重い、予測不能 | `transition-colors duration-200` |
| `group-hover:translate-x-2` 矢印 | よく見るパターン | 削除 or `translate-x-1` |
| 色付きCTAボタン（デフォルト使用） | AI safe choice | 白背景 or 白枠線 |

### アニメーション

| 禁止パターン | 問題 | 代替案 |
|-------------|------|-------|
| 散らばったマイクロインタラクション | 統一感なし | 1つのページロード演出に集中 |
| `animate-pulse` 多用 | 気が散る | 削除 or 1箇所のみ |
| `animate-bounce` 常時 | 同上 | ユーザーアクション時のみ |
| 複数要素の同時アニメーション | カオス | staggered delays で順次 |

### 色（AI Safe Choices）

| 禁止パターン | 問題 | 代替案 |
|-------------|------|-------|
| 紫グラデーション on 白背景 | 最も汎用的なAI選択 | 単色ダーク |
| `from-violet-600 to-indigo-600` | 同上 | 削除 |
| `text-indigo-400` をデフォルトに | ブランド色の乱用 | `text-white` or `text-white/80` |
| 同系色バッジ（indigo on indigo） | コントラスト不足 | 白背景 + 黒テキスト |

---

## アイコン

- **使用ライブラリ**: Lucide Icons
- **禁止**: 絵文字をアイコンとして使用しない

```tsx
import { Music, Brain, Sparkles, Check, X } from 'lucide-react';
```

---

## レスポンシブブレークポイント

```css
/* Mobile first */
/* sm: 640px */
/* md: 768px */
/* lg: 1024px */
/* xl: 1280px */
/* 2xl: 1536px */
```

検証すべき画面幅:
- 320px (最小モバイル)
- 768px (タブレット)
- 1024px (デスクトップ)
- 1440px (大画面)

---

## Pre-Delivery Checklist

- [ ] **Lighthouse アクセシビリティ 100%**（最重要）
- [ ] プロジェクトの globals.css トークンを使用
- [ ] 画像が主役になっているか
- [ ] セクション間余白 >= 112px (py-28)
- [ ] ボタンは白/枠線ベースか
- [ ] 背景は単色か
- [ ] 絵文字アイコン不使用（Lucide使用）
- [ ] ダークモード対応
- [ ] cursor-pointer on clickables
- [ ] レスポンシブ対応
- [ ] パフォーマンス最適化（画像、アニメーション）

---

## コントラスト確認方法

実装後は必ず Lighthouse でアクセシビリティを確認:

```bash
# ローカル確認
npm run dev
lighthouse http://localhost:3000 --only-categories=accessibility --view

# 詳細な失敗項目の確認
lighthouse http://localhost:3000 --only-categories=accessibility --output=json | jq '.audits["color-contrast"]'
```

**目標: Lighthouse Accessibility Score 100%**
