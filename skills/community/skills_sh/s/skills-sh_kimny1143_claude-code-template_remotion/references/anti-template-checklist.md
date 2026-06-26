# Anti-Template Quality Checklist

> **核心原則: 「全部ちゃんとやる」がAI生成感の正体。「何を捨てるか」がデザイン。**

実装完了後、レンダリング前にこのチェックリストで確認する。
自動チェック（`scripts/check-quality.sh`）で検出できる項目は [AUTO] マーク付き。

---

## 1. アニメーション多様性

### [AUTO] UNIFORM_STAGGER — 均等ディレイを避ける
```tsx
// ❌ Bad: 機械的な等間隔
{items.map((item, i) => <Icon delay={i * 8} />)}

// ✅ Good: 有機的なリズム
const ORGANIC_DELAYS = [0, 5, 13, 21];
{items.map((item, i) => <Icon delay={ORGANIC_DELAYS[i]} />)}
```

### [AUTO] UNIFORM_SPRING — 要素の重さでspring configを変える
| 要素タイプ | damping | mass | 例 |
|-----------|---------|------|-----|
| 重い (mockup, 全画面) | 18-25 | 1.0-1.5 | iPhone, フルスクリーン画像 |
| 普通 (テキスト, カード) | 12-16 | 0.5-0.8 | タイトル, UI要素 |
| 軽い (ドット, バッジ) | 6-10 | 0.2-0.4 | インジケーター, 小アイコン |
| バウンス要求 | 5-8 | 0.3-0.5 | CTA, 注目させたい要素 |

### [AUTO] GENERIC_REVEAL — テキスト演出に種類を持たせる
1つの動画内で最低2種類のテキスト演出を使うこと:

| 技法 | 実装 | 印象 |
|------|------|------|
| マスクリビール | `clipPath: inset(0 ${100-p}% 0 0)` | シネマティック |
| 単語ごとスタガー | `text.split(' ').map()` + 個別spring | ダイナミック |
| スケール+トラッキング | `scale(1.3→1)` + `letterSpacing(10→0)` | エレガント |
| ハードカット | アニメーションなし、突然出現 | インパクト |
| タイプライター | 1文字ずつ表示 | テクニカル |

```tsx
// マスクリビール実装例
const MaskReveal: React.FC<{ text: string; delay?: number }> = ({ text, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: { damping: 20, mass: 1.0 } });
  const clipX = interpolate(p, [0, 1], [0, 100]);
  return (
    <div style={{ clipPath: `inset(0 ${100 - clipX}% 0 0)` }}>
      <span style={{ fontSize: 100, fontWeight: 700, color: '#fff' }}>{text}</span>
    </div>
  );
};
```

---

## 2. 構成とペーシング

### [AUTO] LONG_SCENE — 8秒以上の固定構図シーンを避ける
- 1シーン内でもカメラ的変化（scale, position, zoom）を入れる
- mockupの位置やサイズを途中で変える
- サブタイトルやラベルの切り替えでリズムを作る

### [AUTO] SINGLE_TRANSITION — トランジションの種類を混ぜる
1つのコンポジション内で同じトランジションを3回以上使わない。

| 種類 | 用途 |
|------|------|
| Wipe (clipPath) | シーン間の大きな転換 |
| Scale transition | 同カテゴリ内の切り替え |
| Hard cut | 緊張感、インパクト |
| Crossfade | 柔らかい印象、同テーマ内 |

### [AUTO] NO_SOCIAL_PROOF — 30秒プロモには信頼性ビートを入れる
「Free」「4.8 stars」「10K downloads」「No account needed」等

### カット数の目安
| 動画長 | 推奨カット数 | 平均ショット長 |
|--------|-------------|---------------|
| 15秒 | 5-7 | 2-3秒 |
| 30秒 | 8-12 | 2.5-3.5秒 |
| 60秒 | 15-20 | 3-4秒 |

### BPM同期
```tsx
// theme.ts に追加
export const music = {
  bpm: 120,
  framesPerBeat: (30 * 60) / 120, // = 15
  framesPerBar: ((30 * 60) / 120) * 4, // = 60
} as const;
```
カット位置はビートの境界に合わせつつ、**毎拍で切らない**こと。
cut-cut-hold-cut-hold-hold-cut-CUT のリズム変化が手作り感を生む。

---

## 3. レイアウト

### [AUTO] ALL_CENTERED — 全シーンセンター配置を避ける
最低1シーンは非対称レイアウトにする:
- テキスト左寄せ + 右にビジュアル
- 上1/3にタイトル + 下2/3にデモ
- Rule of thirds を意識

---

## 4. サウンド

### [AUTO] NO_SFX — BGMだけでなくSFXを使う
| タイミング | SFXの種類 |
|-----------|----------|
| トランジション5-10f前 | ウーッシュ (whoosh) |
| テキスト出現 | インパクト音 (低域hit + 高域click) |
| フック直前 | **無音 6-10f** → 最強のスクロールストッパー |
| ボタンタップ | ソフトクリック |
| 完了・成功 | チャイム |

---

## 5. 手動チェック項目

自動検出が難しいが重要な項目:

### 意味のあるアニメーション (Semantic Motion)
- [ ] "Track" → 横スライド、"Record" → 赤ドット点滅、等
- [ ] タイマー数字 → カウントアップ/ダウン
- [ ] 各単語の動きがその意味と関連している

### カラーの意図的な逸脱
- [ ] Problem/Agitationシーンでブランドカラーを崩す（彩度低下、寒色寄り等）
- [ ] Solutionで元のカラーに戻すことで「解決感」を演出

### フォントウェイトの対比
- [ ] 同一画面内でfontWeight 300と700が共存している箇所がある
- [ ] 全テキストが同じfontWeightではない

### デモシーンのリアリティ
- [ ] タップインジケーター（指タッチシミュレーション）がある
- [ ] mockupが完全に静止していない（微フロート、微回転）
- [ ] 「Feature名」を1語ずつ急速表示 vs 1行テキストブロック

### 全体の「引き算」
- [ ] 少なくとも1箇所、意図的にアニメーションを使わない（ハードカット）場所がある
- [ ] backdrop-blur, glow, gradient border を使っていない
- [ ] 装飾 < コンテンツの比率になっている
