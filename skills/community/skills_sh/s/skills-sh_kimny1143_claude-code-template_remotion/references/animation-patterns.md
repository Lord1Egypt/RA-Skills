# Remotion アニメーションパターン集

## 基本API

### interpolate — 値の補間
```tsx
import { interpolate, useCurrentFrame } from 'remotion';

const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: 'clamp',
});
```

### spring — 物理ベースアニメーション
```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const scale = spring({ frame, fps, config: { damping: 12, mass: 0.5 } });
```

### Sequence — シーン切り替え
```tsx
import { Sequence } from 'remotion';

<Sequence from={0} durationInFrames={150}>
  <Scene1 />
</Sequence>
<Sequence from={150} durationInFrames={300}>
  <Scene2 />
</Sequence>
```

---

## 共通パターン

### テキストリビール（タイトル出現）
```tsx
const TextReveal: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ overflow: 'hidden' }}>
      <div
        style={{
          transform: `translateY(${interpolate(
            spring({ frame, fps, config: { damping: 15, mass: 0.8 } }),
            [0, 1],
            [100, 0]
          )}%)`,
        }}
      >
        {text}
      </div>
    </div>
  );
};
```

### フェードイン（汎用）
```tsx
const FadeIn: React.FC<{ delay?: number; children: React.ReactNode }> = ({
  delay = 0,
  children,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame - delay, [0, 15], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return <div style={{ opacity }}>{children}</div>;
};
```

### フェードイン + スライドアップ
```tsx
const FadeSlideIn: React.FC<{ children: React.ReactNode; delay?: number }> = ({
  children,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const adjustedFrame = frame - delay;

  const opacity = interpolate(adjustedFrame, [0, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const translateY = interpolate(adjustedFrame, [0, 20], [30, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ opacity, transform: `translateY(${translateY}px)` }}>
      {children}
    </div>
  );
};
```

### タイプライター効果
```tsx
const TypewriterText: React.FC<{ text: string; startFrame?: number }> = ({
  text,
  startFrame = 0,
}) => {
  const frame = useCurrentFrame();
  const adjustedFrame = frame - startFrame;

  const charsToShow = Math.floor(
    interpolate(adjustedFrame, [0, text.length * 3], [0, text.length], {
      extrapolateRight: 'clamp',
    })
  );

  return <span>{text.slice(0, charsToShow)}</span>;
};
```

### スケールバウンス（登場演出）
```tsx
const scaleValue = spring({
  frame: frame - delay,
  fps,
  config: {
    damping: 10,
    stiffness: 100,
    mass: 0.5,
  },
});
```

### キャラクター首傾げ
```tsx
const CharacterTilt: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tilt = spring({
    frame: frame - 10,
    fps,
    config: { damping: 12, mass: 0.5 },
  });

  return (
    <div
      style={{
        transform: `rotate(${interpolate(tilt, [0, 1], [0, -15])}deg)`,
        transformOrigin: 'center bottom',
      }}
    >
      {/* Character SVG */}
    </div>
  );
};
```

### キャラクター目の表情変化
```tsx
// 目を細める → 元に戻る（2段階）
const CharacterSquint: React.FC = () => {
  const frame = useCurrentFrame();
  const eyeSquint = interpolate(frame, [0, 8, 20, 28], [1, 0.3, 0.3, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ transform: `scaleY(${eyeSquint})` }}>
      {/* Eye SVG */}
    </div>
  );
};
```

### ワイプトランジション
```tsx
const WipeTransition: React.FC<{
  direction?: 'left' | 'right';
  color?: string;
}> = ({ direction = 'right', color = '#6366F1' }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, 15], [0, 100], {
    extrapolateRight: 'clamp',
  });
  const exit = interpolate(frame, [15, 30], [0, 100], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const clipPath =
    direction === 'right'
      ? `inset(0 ${100 - progress}% 0 ${exit}%)`
      : `inset(0 ${exit}% 0 ${100 - progress}%)`;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundColor: color,
        clipPath,
      }}
    />
  );
};
```

### BGM同期（ビートマーカー）
```tsx
// BGMのビートタイミングを定義して映像と同期
const BEAT_FRAMES = [0, 30, 60, 90, 120, 150]; // 例: BPM120 @ 30fps

const BeatPulse: React.FC<{ beatIndex: number }> = ({ beatIndex }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const beatFrame = BEAT_FRAMES[beatIndex];
  const pulse = spring({
    frame: frame - beatFrame,
    fps,
    config: { damping: 8, mass: 0.3 },
  });

  return (
    <div style={{ transform: `scale(${1 + pulse * 0.1})` }}>
      {/* ビートに合わせて少し拡大 */}
    </div>
  );
};
```

---

## Tips

- **spring の damping**: 低い値（5-8）= 弾む / 高い値（15-20）= 落ち着いた動き
- **キャラクターの動き**: damping: 12 を基準に統一すると一貫したキャラ性が出る
- **音と映像の同期**: BPMからフレーム数を計算する（BPM120 @ 30fps = 15フレーム/拍）
- **extrapolateRight: 'clamp'**: アニメーション終了後に値が飛ばないようにする（ほぼ必須）
