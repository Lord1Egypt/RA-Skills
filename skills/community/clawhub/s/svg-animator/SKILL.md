---
name: svg-animator
description: Generate animated videos from SVG frames using text LLM. Supports any subject (animals, humans, characters, scenes, abstract art), automatic duration calculation, and multi-scene story animations. Perfect替代 AI 视频生成 API，直接用文本模型生成 SVG 代码然后合成视频。
---

# SVG Animator

用文本模型生成 SVG 代码，逐帧渲染后合成视频。完全不需要视频生成 API！

## 支持的场景

- **动物**：小狗奔跑、小猫跳跃、鱼儿游泳、鸟儿飞翔
- **人物**：走路、跑步、跳舞、工作场景
- **场景**：日出日落、云彩飘动、树叶落下、雨滴下落
- **抽象**：几何变换、颜色渐变、粒子效果
- **故事**：多场景连续动画（需要多段拼接）

## 使用流程

```
用户：生成一个"小猫伸懒腰"的动画
↓
1. 理解需求 → 确定主题、动作、时长
2. 设计帧序列 → 每帧的 SVG 代码
3. 生成帧 → Node.js 生成 SVG → rsvg-convert 转 PNG
4. 合成视频 → ffmpeg 合成 MP4/GIF
5. 输出 → 返回文件路径或 nginx 链接
```

## 时长计算规则

| 需求 | 帧数 | 时长 | fps |
|------|------|------|-----|
| 简单动作（伸懒腰、眨眼） | 8-12帧 | 1秒 | 10 |
| 常规动作（走路、跑步） | 16-24帧 | 2秒 | 12 |
| 复杂动作（跳舞、翻滚） | 30-48帧 | 3-4秒 | 12 |
| 短故事（2-3个场景） | 60-120帧 | 5-10秒 | 12 |
| 长故事（5+场景） | 120+帧 | 10秒+ | 15 |

## 动画原理

### 周期性运动（正弦函数）

```javascript
// 帧索引 i，总帧数 totalFrames
const t = (i / totalFrames) * Math.PI * 2;  // 0 → 2π 循环

// 腿部摆动
const legOffset = Math.sin(t) * 40;

// 尾巴摇动
const tailAngle = Math.sin(t * 2) * 25;

// 身体上下颠簸
const bodyY = Math.sin(t) * 5;
```

### 多元素协调

```javascript
// 腿、尾巴、身体用同一个 t，但幅度不同
const legPhase = t;           // 腿部周期
const tailPhase = t * 2;      // 尾巴周期快一倍
const bodyPhase = t;          // 身体与腿同步

// 组合使用
legOffset = Math.sin(legPhase) * 40;
tailAngle = Math.sin(tailPhase) * 25;
bodyY = Math.sin(bodyPhase) * 5;
```

## 帧生成代码模板

```javascript
const fs = require('fs');
const { execSync } = require('child_process');

const frames = 24;  // 根据时长需求调整
const size = 400;

for (let i = 0; i < frames; i++) {
  const t = (i / frames) * Math.PI * 2;
  
  // 计算运动参数
  const legOffset = Math.sin(t) * 40;
  const tailAngle = Math.sin(t * 2) * 25;
  // ... 更多参数

  const svg = `<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
    <!-- 背景 -->
    <rect width='${size}' height='${size}' fill='#87CEEB'/>
    
    <!-- 地面 -->
    <rect x='0' y='${size*0.88}' width='${size}' height='${size*0.12}' fill='#90EE90'/>
    
    <!-- 主体 - 使用运动参数 -->
    <ellipse cx='${200 + legOffset * 0.5}' cy='${250 + Math.sin(t)*5}' ... />
    <!-- 更多元素 -->
  </svg>`;

  fs.writeFileSync(`/tmp/frames/frame_${String(i).padStart(2, '0')}.svg`, svg);
}

// 转 PNG
execSync('rsvg-convert frame_*.svg -o frame_%02d.png');

// 合成视频
execSync('ffmpeg -y -framerate 12 -i frame_%02d.png -c:v mpeg4 -q:v 2 output.mp4');
```

## 常用动画参数

### 走路/奔跑

```javascript
const runCycle = {
  legSwing: Math.sin(t) * 40,      // 腿摆动幅度
  bodyBob: Math.sin(t * 2) * 5,   // 身体颠簸
  tailWag: Math.sin(t * 2) * 30,  // 尾巴摇
  armSwing: Math.sin(t) * 25      // 手臂摆动
};
```

### 飞行

```javascript
const flyCycle = {
  wingUp: Math.sin(t) * -45,      // 翅膀上扬
  wingDown: Math.sin(t) * 45,     // 翅膀下落
  bodyTilt: Math.sin(t) * 10,     // 身体倾斜
  glide: Math.sin(t) * 20         // 滑翔高度变化
};
```

### 跳跃

```javascript
const jumpCycle = {
  yOffset: -Math.abs(Math.sin(t)) * 100,  // 垂直位移
  legTuck: Math.abs(Math.sin(t)) * 30,   // 收腿
  armUp: Math.abs(Math.sin(t)) * -30      // 举手
};
```

### 摇摆/晃动

```javascript
const swayCycle = {
  rotation: Math.sin(t) * 15,     // 整体摇摆角度
  xOffset: Math.sin(t) * 10,     // 水平位移
  wave: Math.sin(t * 3) * 5      // 轻微晃动
};
```

## 场景动画示例

### 日出

```javascript
// 太阳从地平线升起
const progress = i / frames;
const sunY = size * 0.8 - progress * size * 0.6;  // 从下往上
const skyGrad = `rgb(${255 * progress}, ${200 * progress}, ${100 + 155 * progress})`;
```

### 云飘动

```javascript
const cloudX = (i / frames) * size * 1.5;  // 从左往右
// 云朵透明度随位置变化
const opacity = 1 - (cloudX / size) * 0.5;
```

### 雨滴下落

```javascript
// 多滴雨
for (let drop = 0; drop < 10; drop++) {
  const startFrame = (frames / 10) * drop;
  const dropPos = ((i - startFrame) / frames) * size;
  // 绘制雨滴在 dropPos 位置
}
```

## 多场景故事动画

当用户需要"讲一个故事"时，生成多个场景然后拼接：

```javascript
// 场景1：小猫醒来（12帧）
// 场景2：伸懒腰（12帧）  
// 场景3：玩耍（24帧）
// 场景4：吃饭（16帧）
// 场景5：睡觉（12帧）

// 分别生成后用 ffmpeg 拼接
const scenes = ['scene1.mp4', 'scene2.mp4', 'scene3.mp4'];
const concatList = scenes.map(s => `file '${s}'`).join('\n');
fs.writeFileSync('/tmp/concat.txt', concatList);
execSync(`ffmpeg -y -f concat -safe 0 -i /tmp/concat.txt -c copy story.mp4`);
```

## 完整工作流

### Step 1: 分析需求

```
"生成一个小狗追蝴蝶的故事动画"
```

分解：
- 主题：小狗 + 蝴蝶
- 动作：追逐（小狗跑 + 蝴蝶飞）
- 场景：草地、天空
- 时长：5-8秒（3个场景）

### Step 2: 设计场景

1. **场景1**（0-3秒）：小狗看到蝴蝶
   - 小狗站立，尾巴摇
   - 蝴蝶飞过
   
2. **场景2**（3-6秒）：追逐
   - 小狗奔跑（24帧循环）
   - 蝴蝶飞舞（上下移动）
   
3. **场景3**（6-8秒）：抓到/没抓到
   - 小狗停下
   - 蝴蝶继续飞 / 小狗开心

### Step 3: 生成代码

```bash
# 创建帧目录
mkdir -p /tmp/animation_frames

# 用 Node.js 生成 SVG（根据设计的场景）
node generate_story.js

# 转换 PNG
rsvg-convert /tmp/animation_frames/*.svg -o /tmp/animation_frames/frame_%04d.png

# 合成视频
ffmpeg -y -framerate 12 -i /tmp/animation_frames/frame_%04d.png \
  -c:v mpeg4 -q:v 2 /tmp/story.mp4
```

### Step 4: 提供下载

复制到 nginx 目录或直接发送文件路径

## 注意事项

1. **ffmpeg 必须安装** - `dnf install ffmpeg` 或 `apt install ffmpeg`
2. **rsvg-convert 必须** - 用于 SVG → PNG
3. **帧数不要太多** - 超过 200 帧可能很慢
4. **复杂故事分场景** - 不要把所有动作放一帧里
5. **背景简洁** - 复杂背景会影响性能

## 辅助脚本

使用 `scripts/animate.js` 简化流程：

```bash
# 基本动画
node scripts/animate.js --theme "dog running" --frames 24 --output /tmp/dog.mp4

# 自定义时长（秒）
node scripts/animate.js --theme "cat stretching" --duration 2 --output /tmp/cat.mp4

# 多场景故事
node scripts/animate.js --story "小兔子的一天" --scenes 5 --output /tmp/rabbit_day.mp4
```

## 输出格式

- **MP4**：适合分享，文件小
- **GIF**：适合嵌入网页/文档
- **链接**：部署到 nginx 通过 http 提供

```bash
# 转 GIF
ffmpeg -i input.mp4 -vf "fps=12,scale=480:-1:flags=lanczos" output.gif
```
