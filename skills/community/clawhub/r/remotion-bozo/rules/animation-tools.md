# 动画工具函数

预定义的动画工具函数，快速实现常见动画效果。

## 导入

```typescript
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
  Easing,
} from 'remotion';
```

## Spring 动画配置

### 基础配置

```typescript
const springConfig = {
  damping: 12,      // 阻尼系数，控制震荡（推荐 10-15）
  stiffness: 80,    // 刚度，控制速度（推荐 60-100）
  mass: 1,          // 质量（推荐 1）
};
```

### 使用示例

```typescript
// 缩放动画
const scale = spring({
  frame: progress * 30,
  fps: 30,
  config: springConfig,
});

// 应用到元素
<div style={{ transform: `scale(${scale})` }}>
  内容
</div>
```

### 配置建议

| 效果 | damping | stiffness | mass |
|------|---------|-----------|------|
| 快速响应 | 8-10 | 100-120 | 0.5-1 |
| 标准动画 | 12-15 | 70-90 | 1 |
| 慢速柔和 | 15-20 | 40-60 | 1-2 |
| 强弹跳 | 5-8 | 80-100 | 1 |

## Easing 缓动函数

### 基础缓动

```typescript
const easingConfig = {
  easeInOut: Easing.inOut(Easing.cubic),  // 进入和退出都平滑
  easeOut: Easing.out(Easing.cubic),      // 退出平滑（最常用）
  easeIn: Easing.in(Easing.cubic),        // 进入平滑
  linear: Easing.linear,                  // 线性
};
```

### 使用示例

```typescript
// 淡入动画
const opacity = interpolate(progress, [0, 0.3], [0, 1], {
  extrapolateRight: 'clamp',
  easing: easingConfig.easeOut,
});

// 滑入动画
const y = interpolate(progress, [0, 0.5], [100, 0], {
  extrapolateRight: 'clamp',
  easing: easingConfig.easeOut,
});
```

## 贝塞尔曲线

### 预设曲线

```typescript
const bezierPresets = {
  bouncy: Easing.bezier(0.68, -0.55, 0.265, 1.55),    // 强弹跳
  smooth: Easing.bezier(0.25, 0.1, 0.25, 1.0),        // 平滑
  dramatic: Easing.bezier(0.68, -0.6, 0.32, 1.6),     // 戏剧性
  ease: Easing.bezier(0.25, 0.46, 0.45, 0.94),        // 标准 ease
};
```

### 自定义贝塞尔

```typescript
// Easing.bezier(x1, y1, x2, y2)
const custom = Easing.bezier(0.5, 0, 0.5, 1);
```

## 场景进度计算

### 基础函数

```typescript
const useSceneProgress = (startFrame: number, duration: number) => {
  const frame = useCurrentFrame();
  const progress = (frame - startFrame) / duration;
  return {
    progress: Math.max(0, Math.min(1, progress)), // Clamp to [0, 1]
    frame,
    isPlaying: frame >= startFrame && frame < startFrame + duration
  };
};
```

### 使用示例

```typescript
const MyScene: React.FC = () => {
  const {progress} = useSceneProgress(0, 120); // 从第0帧开始，持续120帧

  return <div style={{opacity: progress}}>内容</div>;
};
```

## 延迟动画

### 计算延迟进度

```typescript
const getDelayedProgress = (progress: number, delay: number) => {
  return Math.max(0, (progress - delay) / (1 - delay));
};
```

### 使用示例

```typescript
// 元素 A 无延迟
const opacityA = interpolate(progress, [0, 0.3], [0, 1]);

// 元素 B 延迟 20%
const progressB = getDelayedProgress(progress, 0.2);
const opacityB = interpolate(progressB, [0, 0.3], [0, 1]);

// 元素 C 延迟 40%
const progressC = getDelayedProgress(progress, 0.4);
const opacityC = interpolate(progressC, [0, 0.3], [0, 1]);
```

## 常用动画组合

### 淡入 + 上移

```typescript
const fadeSlideUp = (progress: number) => ({
  opacity: interpolate(progress, [0, 0.3], [0, 1], {
    extrapolateRight: 'clamp',
  }),
  y: interpolate(progress, [0, 0.5], [50, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  }),
});

// 使用
const {opacity, y} = fadeSlideUp(progress);
<div style={{opacity, transform: `translateY(${y}px)`}}>内容</div>
```

### 弹跳缩放

```typescript
const bounceScale = (progress: number) => {
  const scale = spring({
    frame: progress * 30,
    fps: 30,
    config: { damping: 8, stiffness: 100, mass: 1 },
  });
  return scale;
};
```

### 逐个显示列表

```typescript
const listItems = ['项目1', '项目2', '项目3', '项目4'];

listItems.map((item, index) => {
  const itemDelay = 0.2 + (index * 0.1);
  const itemProgress = Math.max(0, (progress - itemDelay) / (1 - itemDelay));

  return {
    text: item,
    opacity: interpolate(itemProgress, [0, 0.3], [0, 1], {
      extrapolateRight: 'clamp',
    }),
    x: interpolate(itemProgress, [0, 0.3], [-30, 0], {
      extrapolateRight: 'clamp',
      easing: Easing.out(Easing.cubic),
    }),
  };
});
```

## 完整组件示例

```typescript
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  Easing,
} from 'remotion';

const AnimatedScene: React.FC = () => {
  const frame = useCurrentFrame();
  const progress = frame / 120; // 0 到 1

  // Spring 缩放
  const scale = spring({
    frame: progress * 30,
    fps: 30,
    config: { damping: 12, stiffness: 80, mass: 1 },
  });

  // 淡入
  const opacity = interpolate(progress, [0, 0.3], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // 滑入
  const y = interpolate(progress, [0, 0.5], [100, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.68, -0.55, 0.265, 1.55),
  });

  return (
    <AbsoluteFill style={{background: '#1a1a2e'}}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          opacity,
          transform: `translateY(${y}px) scale(${scale})`,
        }}
      >
        <h1 style={{color: 'white', fontSize: 72}}>动画内容</h1>
      </div>
    </AbsoluteFill>
  );
};
```
