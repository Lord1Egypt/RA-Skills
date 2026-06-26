---
name: videogen
description: 视频号AI短视频自动化生产流水线（v2）。用户说"做视频"、"生成视频"、"短视频制作"、"视频混剪"时触发。支持三种内容模式自动切换（Mode A纯干货 / Mode B剧情+科普 / Mode C漫剧型）。使用 MiniMax Hailuo AI 生成视频片段，配合 FFmpeg 混剪，输出适合视频号发布的完整短视频。
---

# videogen v2 — 视频号 AI 短视频自动化生产流水线

## ⚠️ 重要前置说明

### API 体系

| API Key 类型 | 开头 | 支持能力 |
|-------------|------|---------|
| MiniMax Key | `sk-cp-` | TTS (speech-2.8-hd) ✅、Hailuo 视频生成 ✅、Music ❌ |
| IMA Key | `ima_` | SeeDream 生图、Wan/Kling 视频（数字分身必需） |

**每日额度**：`usage limit exceeded` (2056) 报错表示当日 Hailuo 视频额度耗尽，需次日恢复。当前 key 不支持 music-2.5+。

### API 错误处理规范

```
错误码      含义                    处理
─────────────────────────────────────────────────────────────
2056       usage limit exceeded   跳过该片段继续后续步骤
其他异常    未知错误               记录错误，换策略继续，不卡死
```

---

## 三种内容模式

系统根据**选题自动判断**最优内容模式（可手动指定覆盖）：

### Mode A — 纯干货型
**适用**：财经分析、技术教程、行业报告、数据解读、科普讲解

**结构**：开场痛点(3s) → 核心要点×3(各12s) → 金句收尾(9s)

**视觉**：PPT/图表为主，AI点缀关键帧（数字动画、光芒效果）

```
开场 → 数据页 → 讲解页 → 数据页 → 讲解页 → 数据页 → 讲解页 → 金句
```

### Mode B — 剧情+科普型 ✨ 新版主打
**适用**：职业发展、认知升级、社会洞察、励志干货

**结构**：剧情钩子(8s) → 问题拆解(15s) → 干货×2(各12s) → 升华收尾(10s)

**视觉**：剧情画面 + 干净科普画面混合，兼顾情感共鸣与信息密度

```
剧情开场(困境) → 问题拆解 → 剧情演绎+干货 → 剧情演绎+干货 → 升华+关注引导
```

### Mode C — 漫剧/剧情型
**适用**：人生转折、励志逆袭、情感故事、人情冷暖

**结构**：起(8s) → 承(12s) → 转(20s) → 合(8s) + 金句收尾

**视觉**：角色全程驱动，强戏剧冲突，色调/情绪变化明显

```
建立(平凡) → 转折(至暗) → 挣扎 → 行动序列×3 → 蜕变(成功) → 金句
```

---

## 增强版分镜字段

```json
{
  "panel_number": 1,
  "scene_type": "剧情场景 | 知识讲解 | 数据展示 | 过渡页",
  "shot_type": "特写 | 近景/中景 | 中景 | 全景 | 远景/建立景 | POV主观视角",
  "camera_move": "固定镜头 | 推进 | 拉出 | 左摇 | 右摇 | 上摇 | 下摇 | 移动摄影 | 跟随",
  "description": "画面文字描述（供PPT/绘图AI使用）",
  "video_prompt": "Hailuo视频生成Prompt（镜头控制+主体+氛围+动态+风格）",
  "narration": "旁白/台词",
  "duration": 5,
  "transition": "硬切 | 淡入淡出 | 溶解 | 滑入"
}
```

**Video Prompt 公式**（参考《AIGC短视频策划与制作》）：
```
镜头描述 + 镜头运动 + 主体内容 + 动态元素 + 风格 + 9:16竖屏
```

---

## 使用方式

### 方式一：直接对话（推荐）

直接告诉我选题或发链接，我来判断模式并执行完整流水线：
```
python scripts/v2/run_pipeline.py gen "选题内容"
python scripts/v2/run_pipeline.py gen "https://mp.weixin.qq.com/s/xxx"   # 微信文章
python scripts/v2/run_pipeline.py gen "https://zhuanlan.zhihu.com/p/xxx" # 知乎文章
```

### URL 内容提取

支持自动识别并提取以下来源的正文内容：

| 来源 | 支持状态 | 提取内容 |
|------|---------|---------|
| 微信公众号文章 | ✅ 完整支持 | 标题、作者、正文 |
| 知乎文章/回答 | ✅ 完整支持 | 标题、作者、发布时间、正文 |
| 通用网页 | ✅ 支持（BS4） | 标题、正文（trafilatura 更优）|

```bash
# 单独测试 URL 提取
python scripts/v2/url_extractor.py "https://mp.weixin.qq.com/s/xxx"
python scripts/v2/url_extractor.py "https://zhuanlan.zhihu.com/p/xxx" --summarize

# 提取 + 生成摘要 + 生成分镜（管道）
python scripts/v2/url_extractor.py "URL" --summarize -o extracted.json
```

### 方式二：分步执行

```bash
# Step 1: 分析选题（自动检测模式）
python scripts/v2/run_pipeline.py analyze "AI将取代哪些职业"

# Step 2: 生成分镜（可指定模式）
python scripts/v2/run_pipeline.py storyboard "失业后的逆袭之路" --mode auto

# Step 3: 完整流水线
python scripts/v2/run_pipeline.py gen "选题" --mode auto --duration 60
```

### 方式三：旧版快速模式（兼容）

```bash
bash skills/videogen/scripts/build_composite.sh [slide_video] [output] [clips...]
```

---

## 完整流水线（v2）

```
选题 → [自动模式检测] → 分镜生成 → TTS配音 → AI视频片段 → FFmpeg混剪 → 最终视频
```

### Step 1: 选题分析

自动检测三要素：
- **剧情关键词**：失业/逆袭/情感/故事/第一人称经历 → Mode C
- **混合关键词**：职场/认知/赚钱/成长 → Mode B
- **干货关键词**：教程/数据/科普/技术/行业报告 → Mode A

### Step 2: 增强分镜生成（参考 waoowaoo 多阶段架构）

- **Phase 1**：结构规划（镜头数量、景别、场景类型）
- **Phase 2**：运镜+表演（cinematography + acting 并行）
- **Phase 3**：细节补充 + video_prompt 生成

### Step 3: TTS 配音（v2 — Harness 模式）

**Harness 核心思路**：在 TTS 这个不确定节点外面套「校验 → 修复 → 循环」控制环，让输出趋向收敛。

**四个组件**：
| 组件 | 作用 |
|------|------|
| **Chunk 化** | 按句子切分（≤200字/段），改一个词只重做该 chunk |
| **约束系统（Rules）** | TTS 前规范化文本（英文品牌名隔断、数字转中文、连字符转空格等） |
| **双层评估** | L1 确定性预检（文件/时长/语速）+ L2 Whisper X 语义校验 |
| **跨轮记忆** | `normalize_patches.json` — 修复确认后写入，下期自动加载 |

**默认启用 Harness**（`--no-harness` 可关闭）：

```bash
# Harness 模式（默认）
python scripts/v2/run_pipeline.py gen "选题" --mode auto --duration 60

# 关闭 Harness（快速旧版）
python scripts/v2/run_pipeline.py gen "选题" --no-harness

# 单独测试 TTS Harness
python scripts/v2/tts_harness.py "配音文本" --output minimax-output

# 指定音色
python scripts/v2/run_pipeline.py gen "选题" --voice female-yujie
```

**自动修复机制**：
- 确定性预检未通过 → 自动修复文本 → 重新生成（最多 3 轮）
- 超过 3 轮 → 标记 `needs_human=True`，人工处理
- 语义校验（Whisper）未通过 → 标记人工处理

**Whisper 语义校验**（可选，需安装）：
```bash
pip install openai-whisper
# 重新运行 Harness 时自动启用
```

### Step 4: AI 视频片段（Hailuo）

```bash
# t2v（文生视频）— 知识/剧情场景
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode t2v \
  --prompt "medium shot, slow push-in, ... modern cinematic, 9:16 vertical" \
  --duration 6 \
  --output minimax-output/clips/clip_01.mp4

# i2v（图生视频）— 关键帧动画化
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode i2v \
  --prompt "subtle character movement, natural breathing..." \
  --first-frame minimax-output/slides/slide_NN.png \
  --duration 6 \
  --output minimax-output/clips/clip_NN.mp4
```

### Step 5: FFmpeg 混剪

```bash
# overlay 模式（AI片段嵌入PPT视频）
ffmpeg -y \
  -stream_loop 1 -i minimax-output/video_pure_slides.mp4 \
  -i minimax-output/clips/clip_01.mp4 \
  -i minimax-output/clips/clip_02.mp4 \
  -filter_complex "
    [0:v][1:v] overlay=0:0:enable='between(t,0,5.875)' [v1];
    [v1][2:v] overlay=0:0:enable='between(t,15,20.875)' [vout]
  " -map "[vout]" -c:v libx264 -crf 18 -preset fast -t 60 \
  minimax-output/video_complete.mp4

# concat 模式（纯视频片段拼接）
ffmpeg -y -f concat -safe 0 \
  -i <(for f in minimax-output/clips/*.mp4; do echo "file '$f'"; done) \
  -c:v libx264 -crf 22 -preset fast \
  minimax-output/video_concat.mp4
```

### Step 6: 添加配音

```bash
ffmpeg -y \
  -i minimax-output/video_complete.mp4 \
  -i minimax-output/voiceover.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  minimax-output/video_final.mp4
```

---

## 数字分身（方案B，需IMA Key）

```bash
# ① 生成数字人形象
python skills/ima-all-ai/scripts/ima_create.py \
  --task-type text_to_image \
  --model-id doubao-seedream-4.5 \
  --prompt "A professional Asian male/female tech speaker, sleek dark suit, confident" \
  --output minimax-output/digital_host.png

# ② S2V-01 图生视频
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode ref \
  --prompt "Person turns to camera, nods slightly, speaks with confidence, natural movement" \
  --subject-image minimax-output/digital_host.png \
  --duration 6 \
  --output minimax-output/digital_host.mp4

# ③ FFmpeg overlay
ffmpeg -y \
  -i minimax-output/video_complete.mp4 \
  -i minimax-output/digital_host.mp4 \
  -filter_complex "[0:v][1:v] overlay=W-w-40:H-h-40:enable='between(t,0,59)'" \
  -c:v libx264 -crf 18 -preset fast \
  minimax-output/video_with_host.mp4
```

---

## 输出目录

```
minimax-output/
├── storyboard.json          # ✅ v2 新增：增强版分镜 JSON
├── script.md               # 脚本/台词
├── voiceover.mp3           # TTS 配音（Harness 模式为合并后结果）
├── presentation.html       # 乔布斯风 HTML 演示稿
├── slides/                 # 幻灯片图片序列
├── video_pure_slides.mp4   # 纯PPT视频
├── clips/                  # ✅ v2：AI视频片段
│   ├── clip_01.mp4
│   ├── clip_02.mp4
│   └── ...
├── chunks/                 # ✅ Harness：TTS chunk 音频
│   ├── chunk_01.mp3
│   └── ...
├── normalize_patches.json  # ✅ Harness：跨轮记忆 patches
├── video_complete.mp4       # AI片段嵌入后
└── video_final.mp4          # 最终版（配音+画面）
```

---

## Remotion 动画渲染引擎（v2 新增）

Remotion 适合**精确动画/流程图/字幕同步**类内容，比 Hailuo 更适合科普动画。

### 快速使用

```bash
# Step 1: 生成 Remotion 项目代码
python scripts/v2/remotion_generator.py gen \
  --scene-names "开场|Agent Loop|MCP" \
  --timings "20|50|35" \
  --narrations "旁白1||旁白2" \
  --visuals "terminal|ring|hub" \
  --output /path/to/video-project

# Step 2: 安装依赖
cd /path/to/video-project && npm install

# Step 3: 渲染视频（两阶段，解耦 timeout 问题）
# 阶段1：渲染帧序列
npx remotion render Video --output=out/frames --sequence Justice
# 阶段2：ffmpeg 独立编码（不被 timeout 中断）
ffmpeg -framerate 30 -i out/frames/element-%04d.png \
       -c:v libx264 -crf 23 -preset fast -pix_fmt yuv420p -r 30 out/video_raw.mp4

# Step 4: 合并配音
ffmpeg -y -i out/video_raw.mp4 -i voiceover.mp3 \
       -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -shortest video_final.mp4
```

### 竖屏字号规范（视频号 · 9:16 · 1080×1920）

> ⚠️ **视频号竖屏字体最小底线 20px**。14-16px 在手机上看基本不可读。

#### 固定字号标准

| 元素 | 字号 | 字重 | 说明 |
|------|------|------|------|
| **主标题** | 72px | Semibold (600) | 前三秒抓眼球 |
| **二级标题/节点** | 32px | Medium (500) | 竖屏最佳阅读尺寸 |
| **注释/标签/来源** | 20px | Regular (400) | 视频号最小可读底线 |

#### 配色标准（Apple 高级科技风）

| 用途 | 色值 | 说明 |
|------|------|------|
| 背景 | `#111111 → #1c1c1e` | 深空黑渐变 |
| 主文字 | `#FFFFFF` | 纯白 |
| 强调色 | `#007AFF` | Apple 蓝（唯一强调色） |
| 次要文字 | `#8E8E93` | 浅灰 |
| 边框/卡片 | `#3a3a3c` / `#2c2c2e` | — |

> ⚠️ 只用黑白+一个强调色，科技类最忌颜色杂乱。

#### 安全区规范

```
上下左右各留 60px，避免被账号头像、进度条遮挡
```

#### 布局常量

```tsx
export const SAFE = {
  top: 60,
  bottom: 60,
  left: 60,
  right: 60,
  titleTop: 80,     // 主标题 top
  contentTop: 280,  // 内容区 top
  bottomPos: 0.88,  // 底部标签位置
};
```

#### 字号配置（固定值，不缩放）

```tsx
// 主标题：72px Semibold
<div style={{ fontSize: 72, fontWeight: 600, ... }}>标题</div>

// 二级标题/节点：32px Medium
<div style={{ fontSize: 32, fontWeight: 500, ... }}>节点</div>

// 注释/标签：20px Regular
<div style={{ fontSize: 20, fontWeight: 400, color: "#8E8E93", ... }}>标签</div>
```

### Apple 风格模板

技术干货/源码解读类内容推荐使用 Apple 风格模板，已内置可复用组件：

```
templates/apple/
├── AppleShared.tsx   # Apple 风格组件库（含 13 个组件）
└── README.md         # 使用文档
```

详见 [templates/apple/README.md](templates/apple/README.md)。

### 竖屏安全布局规范

竖屏视频必须考虑系统 UI 遮挡，所有内容不得超出安全区域：

```tsx
// 每个场景顶部必须定义安全边距
const safeTop    = 80;   // 顶部安全区（标题区）
const safeBottom = 100;  // 底部安全区（系统 UI + 进度条）

// 内容区域可用高度
const availableH = height - safeTop - safeBottom;

// 列表类内容的总高度
const ITEM_H = 80;   // 每个卡片固定高度
const GAP    = 14;   // 间距
const TOTAL_H = items.length * ITEM_H + (items.length - 1) * GAP;

// 垂直居中于安全区内
const stackTop = safeTop + Math.max(0, (availableH - TOTAL_H) / 2);

// 统一宽度（不出屏）
<div style={{ width: 640, height: ITEM_H, /* ... */ }}>
```

**布局三原则：**
1. **固定高度**：每张卡片用固定 `height`，不用 padding 撑开，防止内容溢出
2. **统一宽度**：同一场景所有卡片用同一 `width`，视觉更整洁
3. **垂直居中**：`stackTop` = `safeTop + (availableH - TOTAL_H) / 2`，内容始终在屏幕中央

### Apple 风格设计规范（推荐）

适用于**技术干货/源码解读/知识科普**类内容，参考 Apple 发布会的视觉风格。

#### Apple 设计 Token（精简版）

```tsx
// 背景：深空黑渐变
const bg = "linear-gradient(180deg, #111111 0%, #1c1c1e 100%)";

// 精简色板（只有一种强调色）
const ACCENT = "#007AFF";   // Apple 蓝（唯一强调色）
const TEXT   = "#FFFFFF";  // 主文字
const MUTED  = "#8E8E93"; // 次要文字
const BORDER = "#3a3a3c"; // 边框
const CARD   = "#2c2c2e"; // 卡片背景

// 字体：Inter + -apple-system fallback
const font = "Inter, -apple-system, sans-serif";
```

#### Apple 风格动画规范

```tsx
// 所有动画必须用 useCurrentFrame() 驱动，禁止 CSS transition/animation
import { useCurrentFrame, interpolate } from "remotion";

// fade-up（主标题）
const opacity = interpolate(frame, [start, start + 14], [0, 1], { extrapolateRight: "clamp" });
const translateY = interpolate(frame, [start, start + 14], [30, 0], { extrapolateRight: "clamp" });

// scale（节点出现）
const scale = interpolate(frame, [start, start + 16], [0.4, 1], { extrapolateRight: "clamp" });

// translateX（列表项依次出现）
const tx = interpolate(frame, [start + i * 12, start + i * 12 + 12], [-24, 0]);

// stagger：每项 delay += 12~16 帧
```

#### Apple 风格图表组件（内置于 `AppleShared.tsx`）

| 组件 | 用途 | 关键参数 |
|------|------|---------|
| `AppleBg` | 深空黑渐变背景 | — |
| `SceneTag` | 左上角场景标签 | text, startFrame, color |
| `HeroTitle` | 页面大标题 | text, startFrame, size, color |
| `LayerStack` | 分层堆栈（四层框架） | layers[{label, sub, color}], startFrame |
| `FlowNode` | 流程图节点圆 | label, x, y, color, startFrame, size |
| `ArrowSVG` | 箭头连接线 | x1, y1, x2, y2, color, startFrame |
| `NineGrid` | 九宫格 | items[], startFrame |
| `PipelineFlow` | 横向管线流 | steps[{label, sub, color}], startFrame |
| `FuseSteps` | 熔断器步骤列表 | startFrame |
| `ToolGrid` | 工具网格 | tools[], startFrame |
| `EngineSpin` | 引擎旋转 SVG | startFrame |
| `TagGroup` | 标签组 | tags[{text, color}], startFrame |
| `TagPill` | 单个标签 | text, color |

#### Apple 风格布局模板

```tsx
import React from "react";
import { AbsoluteFill } from "remotion";
import {
  AppleBg, HeroTitle, SceneTag, TagGroup,
  LayerStack, FlowNode, ArrowSVG, NineGrid,
  PipelineFlow, FuseSteps, ToolGrid, EngineSpin
} from "../components/AppleShared";

// 示例：双路径对比（微压缩）
export const 微压缩: React.FC = () => (
  <AppleBg>
    <SceneTag text="第一层 · 微压缩" startFrame={0} color="#0A84FF" />

    {/* 标题区 */}
    <div style={{ position: "absolute", top: "8%", left: 0, right: 0, textAlign: "center" }}>
      <HeroTitle text="两条路径处理 Prompt Cache" startFrame={5} size={28} />
    </div>

    {/* 左路径：卡片堆叠 */}
    <div style={{ position: "absolute", top: "26%", left: "5%", right: "52%" }}>
      {/* 节点1 */}
      <NodeCard label="连续对话" sub="Cache 有效" color="#0A84FF" startFrame={10} />
      <ArrowDown color="#0A84FF" startFrame={18} />
      {/* 节点2 */}
      <NodeCard label="Cached Micro Compact" sub="精细清理" color="#0A84FF" startFrame={22} />
    </div>

    {/* 中间分割线 */}
    <div style={{ position: "absolute", top: "20%", bottom: "20%", left: "50%", width: 1,
      background: "linear-gradient(180deg, transparent, #2C2C2E, transparent)" }} />

    {/* 右路径 */}
    <div style={{ position: "absolute", top: "26%", left: "53%", right: "5%" }}>
      {/* 类似结构 */}
    </div>

    {/* 底部标签 */}
    <div style={{ position: "absolute", bottom: "10%", left: 0, right: 0 }}>
      <TagGroup startFrame={48} tags={[{text:"主线程隔离",color:"#48484A"},...]} />
    </div>
  </AppleBg>
);
```

#### 竖屏布局安全区参考

```
┌────────────────────────────────────┐
│ ██ 顶部 UI 遮挡区 (~120px) ██       │  ← SceneTag 放这里
├────────────────────────────────────┤
│         top: 8%  页面大标题          │
│                                    │
│        top: 24-26%  主体内容         │
│        （图表/卡片/架构图）           │
│                                    │
│        bottom: 10-12%  标签组       │
├────────────────────────────────────┤
│ ██ 底部 UI 遮挡区 (~100px) ██      │
└────────────────────────────────────┘
```

### 列表类场景设计模式：全部可见 + 当前高亮

对于「N 层结构」「N 个问题」类内容，推荐：

```tsx
// 全部 N 项同时渲染，当前项高亮，其余淡化
const activeIdx = findActiveIndex(progress);
LAYERS.map((l, i) => {
  const isActive  = activeIdx === i;
  const isDormant = activeIdx !== undefined && !isActive;
  const alpha = isDormant ? 0.25 : 1; // 淡化非当前项

  return (
    <div style={{
      opacity: isDormant ? 0.25 : 1,
      backgroundColor: isActive ? l.color + "28" : l.color + "0e",
      border: isActive ? `2px solid ${l.color}` : `1px solid ${l.color}33`,
    }}>
      {/* 当前层进度条 */}
      {isActive && <ProgressBar progress={...} color={l.color} />}
    </div>
  );
});
```

**优势：**
- 观众始终能看到整体结构，有全局感
- 当前层高亮 + 进度条提供局部焦点
- 切换时视觉过渡自然，不会有「突然出现/消失」的感觉

### 场景节奏设计规范

每个场景必须包含**分阶段动画**，避免内容停驻感：

```
Phase timeline（0.0-1.0 进度）：
  0.00-0.10: 标题淡入
  0.10-0.40: 第一组内容
  0.40-0.70: 第二组内容
  0.70-0.90: 全家桶叠显/总结
  0.90-1.00: 收尾

每个卡片底部加进度条：
  width: ${cardProgress * 100}%

切换节奏：每块内容停留 ≤ 12 秒（30fps ≈ 360帧）
```

### 标准工作流（Remotion + TTS 同步）

```bash
# Step 1: 生成 TTS，测时长
python scripts/v2/tts_harness.py "完整旁白" --output=minimax-output/video
ffprobe -show_entries format=duration -of csv=p=0 minimax-output/video/voiceover.mp3
# → e.g. 95 秒

# Step 2: 计算总帧数，分配场景
# total_frames = duration_sec * 30
# 分配比例（示例）：
#   开场 14% / 四层 25% / 天花板 20% / 架构 28% / 结尾 13%

# Step 3: 渲染 + 编码（两阶段）
# Step 4: 合并配音 → 压缩 → 发送
```

### 视频号平台规范

| 参数 | 要求 | 当前项目设置 |
|------|------|------------|
| 时长 | 15秒～10分钟（推荐60秒干货型，5分钟深度内容） | **5分钟** |
| 封面 | 3:4 或 16:9，第一帧即封面 | 自动取开场帧 |
| 比例 | **9:16 竖屏**（1080×1920）或 16:9 横屏 | **1080×1920** |
| 字幕 | 必须有，底部居中 | Remotion 渲染含字幕 |
| 文件大小 | ≤ 5MB（视频号）/ ≤ 10MB（B站） | 微信 CDN 上传限制约 5MB，超出会报 500 错误 |
| 字体大小 | 竖屏最小 36px（正文）/ 72px（标题） | **正文 48-72px / 标题 96-144px** |
| BGM | 剪映音乐库 / 无版权音乐 | 自行添加 |
| 标签 | 3-5个：1垂类+1热点+1账号标签 | — |

> ⚠️ **字体规范**：竖屏 9:16 视频中，1080px 宽度下：
> - 标题/金句：**96-144px**（约 2.5-3.7cm 实际宽度）
> - 正文/旁白：**48-72px**（约 1.2-1.8cm）
> - 底部字幕：**40-48px**
> - 所有组件已按此比例放大（相比原始 Remotion 模板）

---

## 发送前压缩（微信 CDN 限制）

微信视频号上传有文件大小限制（约 5MB），直接发送过大的 MP4 会报 CDN 500 错误。

```bash
# 推荐参数（竖屏 1080×1920，目标 ≤ 5MB）
ffmpeg -y -i input.mp4 \
       -c:v libx264 -crf 24 -preset fast \
       -c:a aac -b:a 96k \
       -movflags +faststart \
       output_compressed.mp4

# 目标文件大小参考：
#   视频号/抖音：≤ 5MB（保险）
#   B站/油管：  ≤ 10MB
#   微信直接发送：≤ 5MB（实测 3.6MB 正常，7.5MB 报 500）
```

## 视频号发布检查清单

- [ ] 时长 15秒～3分钟
- [ ] 封面有标题/话题感，第一帧抓眼球
- [ ] 字幕已添加（剪映AI字幕）
- [ ] BGM 热门且不侵权
- [ ] 话题标签 3-5个
- [ ] 视频比例符合目标平台
- [ ] 结尾有关注引导

---

## v2 新增功能索引

| 功能 | 位置 | 说明 |
|------|------|------|
| TTS Harness | `scripts/v2/tts_harness.py` | chunk + 规范化 + 双层评估 + 跨轮记忆 |
| TTS 语速控制 | `scripts/v2/tts_harness.py` | `--speed 1.5` 支持 MiniMax API 直传倍率参数 |
| chunk 合并修复 | `scripts/v2/tts_harness.py` | 强制 AAC 128kbps 转码 + concat muxer fallback |
| Remotion 渲染 | `scripts/v2/remotion_generator.py` | 生成 TypeScript 场景组件（动画/流程图） |
| Remotion 两阶段渲染 | `scripts/v2/remotion_generator.py` | 帧序列输出 → ffmpeg 独立编码，防 timeout |
| 竖屏字号规范 | `SKILL.md` | 9:16 1080×1920 正文 48-72px / 标题 96-144px |
| 场景节奏设计规范 | `SKILL.md` | 分阶段动画 + 进度条，每块 ≤ 12 秒 |
| TTS + Remotion 同步工作流 | `SKILL.md` | 先生成音频 → 测时长 → 分配场景帧数 |
| Whisper 语义校验 | `tts_harness.py::evaluate_semantic` | L2 评估：词汇级转写比对 |
| 选题自动分析 | `scripts/v2/topic_analyzer.py` | 关键词驱动三模式判断 |
| 增强分镜生成 | `scripts/v2/storyboard_generator.py` | 丰富字段 + 多阶段架构 |
| 统一流水线 | `scripts/v2/run_pipeline.py` | analyze/storyboard/gen 三个入口 |
| Video Prompt 公式 | `storyboard_generator.py::build_video_prompt` | 镜头控制 + 主体 + 氛围 + 动态 + 风格 |
| 多模式结构 | `SKILL.md` Mode A/B/C | 自动切换内容风格 |

---

---

## 七、v3 更新记录

### 已安装依赖 skills
- `remotion-video-toolkit` — Remotion 完整工具手册
- `animations` — Web 动画规范（GPU 加速属性、timing functions）

### 模板文件
- `templates/apple/AppleShared.tsx` — Apple 风格可复用组件库（13个组件）
- `templates/apple/README.md` — Apple 模板使用文档

### 本次优化改动
| 改动 | 文件 | 说明 |
|------|------|------|
| TTS 合并 bug 修复 | `scripts/v2/tts_harness.py` | shutil/os 移到文件顶部统一导入 |
| Apple 风格模板 | `templates/apple/` | 深空黑渐变 + Apple 色板 + 大字标题 |
| 竖屏字体规范更新 | `SKILL.md` | 节点标题 22-28px / 标签 14-16px |
| Apple 设计规范 | `SKILL.md` | 设计 Token + 动画规范 + 图表组件 |
| 竖屏安全布局 | `SKILL.md` | top:8% 标题 / top:24% 内容 / bottom:10% 标签 |

### Apple 风格组件（13个）
`AppleBg` · `SceneTag` · `HeroTitle` · `LayerStack` · `FlowNode` · `ArrowSVG` · `NineGrid` · `PipelineFlow` · `FuseSteps` · `ToolGrid` · `EngineSpin` · `TagGroup` · `TagPill`
