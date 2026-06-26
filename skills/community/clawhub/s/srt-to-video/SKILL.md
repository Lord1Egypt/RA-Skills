---
name: srt-to-video
description: Convert SRT subtitle files into Remotion typing-animation videos with character-by-character text reveal and cinematic animated backgrounds. Use when the user wants a typewriter subtitle effect, SRT-to-video conversion, animated captions, or a Remotion project generated from subtitle files.
---

# SRT → 打字动画视频 Skill

将 `.srt` 字幕文件一键转化为 **Remotion (React)** 视频项目，生成带有"逐字打字机"特效 + 科幻星空背景的精美视频。

---

## 输入

用户提供：
1. **一个 `.srt` 字幕文件**（标准 SRT 格式）
2. **可选参数**：
   - 画幅：`1920x1080`（横版，默认） 或 `1080x1920`（竖版/短视频）
   - 背景风格：`starfield`（默认星空） / `gradient`（纯渐变） / `custom`（用户自定义）
   - 打字速度：`slow`(8帧/字) / `normal`(5帧/字，默认) / `fast`(3帧/字)
   - 字体颜色方案：默认自动分配（白色/金色/蓝色/紫色交替）

---

## 工作流程

### Step 1: 解析 SRT 文件

将 SRT 文件解析为时间轴数据结构：

```typescript
interface SubtitleSegment {
  index: number;
  startTime: number;  // in seconds
  endTime: number;    // in seconds
  text: string;
}
```

SRT 格式示例：
```
1
00:00:01,000 --> 00:00:04,000
人是怎样变强的？

2
00:00:04,500 --> 00:00:06,500
答：表演
```

解析规则：
- 每个字幕块由空行分隔
- 第一行是序号
- 第二行是时间码：`HH:MM:SS,mmm --> HH:MM:SS,mmm`
- 第三行起是字幕文本（可多行）
- 时间码用于确定每段字幕的开始帧和结束帧

### Step 2: 生成时间轴

根据解析结果生成帧级时间轴：

```typescript
// 将 SRT 时间转化为帧号
function timeToFrame(timeStr: string, fps: number): number {
  const [hours, minutes, rest] = timeStr.split(':');
  const [seconds, ms] = rest.split(',');
  const totalSeconds = parseInt(hours) * 3600 + parseInt(minutes) * 60 +
    parseInt(seconds) + parseInt(ms) / 1000;
  return Math.round(totalSeconds * fps);
}
```

为每段字幕计算：
- `startFrame`：字幕开始帧（从 SRT 时间码）
- `endFrame`：字幕结束帧（从 SRT 时间码）
- `typingSpeed`：按文本长度和持续时间自动计算（确保在持续时间的 60-70% 内打完字，剩余时间保持显示）
- `fontSize`：根据文本长度自动调节（短文本大号，长文本小号）
- `color`：自动分配颜色方案

自动 fontSize 计算规则：
- ≤ 5 字: 88px
- 6-10 字: 72px
- 11-15 字: 56px
- 16-20 字: 48px
- > 20 字: 42px

自动颜色循环：
```typescript
const COLOR_PALETTE = [
  '#FFFFFF',   // 白色 — 叙述
  '#FFD866',   // 金色 — 强调/结论
  '#87CEEB',   // 天蓝 — 解释/分析
  '#DDA0DD',   // 紫色 — 情感/转折
  '#C8C8D0',   // 灰白 — 过渡/补充
];
```

### Step 3: 创建 Remotion 项目

在用户指定目录（或默认 scratch 目录）下创建完整的 Remotion 项目：

```
<project-name>/
├── src/
│   ├── components/
│   │   ├── TypingText.tsx      ← 逐字打字组件
│   │   └── Background.tsx      ← 动态星空背景
│   ├── Composition.tsx          ← 主合成：时间轴 + 字幕渲染
│   └── index.tsx                ← Root 注册
├── package.json
└── tsconfig.json
```

### Step 4: 渲染

项目创建后，按以下流程操作：

```bash
# 1. 安装依赖
cd <project-name> && npm install

# 2. 预览（Remotion Studio）
npm start
# 浏览器打开 http://localhost:3000 预览效果

# 3. 渲染最终视频
npm run build
# 输出到 out/video.mp4
```

---

## 核心组件规范

### TypingText 组件

逐字符显示文本，每个字符出现时带轻微缩放弹入效果：

- **打字效果**：`localFrame / typingSpeed` 决定已显示字符数
- **字符动画**：每个新出现的字符从 `scale(1.15)` → `scale(1)`, `opacity: 0.5` → `1`
- **光标**：打字时常亮，完成后闪烁（`Math.sin(frame * 0.15) > 0`）
- **文字阴影**：`0 0 30px rgba(100, 200, 255, 0.3)` 营造发光感
- **字间距**：`letterSpacing: '0.05em'`

### Background 组件

动态科幻星空背景，纯 `useCurrentFrame()` 驱动：

- **渐变底色**：三色渐变（深蓝→深紫→暗灰），色相随帧缓慢偏移
- **星星**：40 个随机分布的点，亮度按帧做正弦闪烁
- **流星**：5 条周期性流星，带角度和拖尾
- **星云光晕**：2 个模糊的椭圆径向渐变，缓慢漫游
- **极光丝带**：模糊的椭圆形色带，带 `skewX` 变形
- **暗角**：`radial-gradient` 压暗四角

### Composition 主合成

- 每次屏幕上只显示 **一行字幕**
- 每段字幕有 `fadeIn`（8 帧渐入）和 `fadeOut`（15 帧渐出）
- 只在当前帧 ± 范围内渲染对应字幕，避免性能浪费
- 总时长根据 SRT 最后一条字幕的 endTime 自动计算

---

## 硬规则

1. **禁止 CSS transition/animation**，所有动画必须用 `useCurrentFrame()` + `interpolate()` / `spring()` 驱动（Remotion 核心规则）
2. **SRT 时间码优先**，严格按照 SRT 文件的时间码定位每段字幕，不自行重算除非用户明确要求
3. **一屏一句**，屏幕上同时只显示一条字幕
4. **自动适配**，fontSize、color、typingSpeed 全部自动计算，用户无需手动指定
5. **项目可独立运行**，生成的项目 `npm install && npm start` 即可预览

---

## 示例

输入 SRT：
```
1
00:00:01,000 --> 00:00:04,000
人是怎样变强的？

2
00:00:04,500 --> 00:00:07,000
答：表演

3
00:00:08,000 --> 00:00:12,000
心理学上叫神经可塑性
```

输出：一个完整的 Remotion 项目，3 段字幕按时间轴依次以打字效果展示，配合星空背景动画。
