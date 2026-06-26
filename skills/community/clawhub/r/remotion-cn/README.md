# Remotion CN - 示例项目

这是一个简单的 Remotion 项目示例，展示如何用代码创建视频。

## 项目结构

```
remotion-cn-example/
├── package.json
├── tsconfig.json
├── remotion.config.ts
├── src/
│   ├── App.tsx
│   ├── HelloWorld.tsx
│   └── AnimatedText.tsx
└── public/
    └── index.html
```

## 安装

```bash
# 创建新项目
npx create-video@latest my-video

cd my-video

# 安装 Remotion
npm install remotion @remotion/cli
```

## 示例代码

### 1. Hello World

```tsx
// src/HelloWorld.tsx
import { Composition } from 'remotion';

export const HelloWorld: React.FC = () => {
  return (
    <Composition>
      <HelloWorld />
    </Composition>
  );
};
```

### 2. 动画文本

```tsx
// src/AnimatedText.tsx
import { AbsoluteFill, useCurrentFrame } from 'remotion';

export const AnimatedText: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: '#1a1a2a' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        fontFamily: 'sans-serif',
        fontSize: 80,
        color: 'white',
        opacity: frame % 60, // 闪烁效果
        transform: `translateY(${Math.sin(frame * 0.1) * 20}px)`
      }}>
        Remotion + AI = 🎥
      </div>
    </AbsoluteFill>
  );
};
```

### 3. 图片动画

```tsx
// src/AnimatedImage.tsx
import { AbsoluteFill, useCurrentFrame, Img } from 'remotion';

export const AnimatedImage: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      <Img
        src="https://github.com/remotion-dev/remotion/blob/main/packages/remotion/example/public/logo.png"
        style={{
          width: 400,
          height: 400,
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: `translate(-50%, -50%) rotate(${frame}deg)`
        }}
      />
    </AbsoluteFill>
  );
};
```

## 渲染命令

```bash
# 开发服务器（实时预览）
npx remotion studio

# 渲染为 MP4
npx remotion render src/HelloWorld.tsx out/video.mp4

# 渲染为 WebM
npx remotion render src/HelloWorld.tsx out/video.webm

# 渲染 GIF
npx remotion render src/AnimatedText.tsx out/video.gif --gif
```

## 配置文件

```typescript
// remotion.config.ts
import { Config } from '@remotion/cli/config';

export default {
  concurrency: 1, // 并发数量
  chromiumPath: null, // 使用默认 Chromium
  ffmpegExecutable: null, // 使用默认 FFmpeg
  log: 'verbose', // 日志级别
  overwrite: true, // 覆盖已存在的文件
} as Config;
```

## 实战用例

### 1. 产品展示视频

创建一个旋转的产品图片展示：
- 360 度旋转
- 3 秒循环
- 带文字说明

### 2. 文字动画

用 Remotion 的文字效果：
- 闪烁效果（opacity 0-60-0）
- 缩放效果
- 淡入淡出

### 3. 音频可视化

创建一个随音乐跳动的音频可视化：
- 条纹随音量变化
- 颜色随时间变化

---

*项目大小: 适合快速学习*
*预计学习时间: 30 分钟*
*难度: ⭐⭐*
