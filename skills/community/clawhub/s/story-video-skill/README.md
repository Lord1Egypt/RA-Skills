# Story Video Pipeline

**AI-Endowed Screenwriter · Director · Visual Storyteller**

一条从叙事文本到电影级视频的完整 production line。输入任意故事大纲、剧本或叙事片段，系统自动完成结构解构、节拍设计、人物弧线构建、分镜头规划，并调用 MiniMax 多模态模型生成连贯的视觉序列，最终输出具有专业镜头语言和情绪基调的完整影片。

---

## 核心能力

### 编剧能力

**叙事结构设计** — 内置三幕结构（Three-Act）、Blake Snyder 节拍表、中国戏曲起承转合等多种故事骨架模型。输入任意故事文本，自动分析其戏剧张力和结构完整性，输出具有节奏感的叙事设计方案。

**对白风格构建** — 从 *Pulp Fiction*、*Star Wars* 等经典剧本中蒸馏出五种对白风格模式：自然主义对话、机智对驳、潜台词表达、内心独白、仪式化台词。系统根据故事类型和人物设定，自动匹配最合适的人物语音体系。

**人物弧线设计** — 支持成长弧、堕落弧、救赎弧、循环弧、平线弧五种角色转变路径。每组角色均生成外在目标（可观察行为）与内在需求（心理转变）的双重设计，确保人物立体可信。

**冲突架构** — 内置人物vs人物、人物vs自我、人物vs社会、人物vs自然、人物vs命运五类冲突模板。每个冲突节点自动匹配经典"目标→障碍→行动→转折→结果"结构。

### 导演能力

**分镜头语言** — 景别体系（EWS/WS/FS/MS/CU/ECU）、角度体系（仰拍/俯拍/水平/倾斜）、运镜体系（推/拉/摇/跟踪/升降/手持）均可按场景情绪需求自由组合。

**视觉基调规划** — 系统内置六种情绪（快乐/悲伤/紧张/神秘/浪漫/恐惧）的完整视觉解决方案——色调、构图、运镜、光线四大维度的协同设计规范，确保视觉表达与叙事情绪高度一致。

**场景调度** — 从真实剧本中提炼的 mise-en-scène 四要素框架（角色位置/景框构图/美术设计/灯光照明），为每个镜头输出精确的空间关系和视觉层次指令。

**MiniMax 运镜指令** — 支持 15 种标准运镜指令在视觉描述中直接嵌入：`[左移] [右移] [推进] [拉远] [左摇] [上升] [跟随] [固定]` 等，支持同时生效和顺序生效两种组合模式。

### 视频生成能力

**帧间连贯** — 首个镜头独立生成，后续每个镜头自动以前一帧画面作为参考输入，锁定角色外观、场景元素和视觉风格，实现多镜头间的一致性。

**多模型支持** — 文生图调用 MiniMax `image-01` 模型；图生视频调用 MiniMax `MiniMax-Hailuo-2.3`，支持 6s/10s 两种时长和 768P/1080P 两种分辨率。

**ffmpeg 合并** — 使用 concat demuxer 模式无损合并所有视频片段，自动生成文本故事板记录整个叙事脉络。

---

## 工作流

```
用户输入故事（几行大纲 or 完整剧本）
        │
        ▼
┌───────────────────────────────────────┐
│  Step 0: 智能判断故事完整度           │
│  分析叙事结构：结局/弧线/内容长度      │
│  ┌─ 完整故事 → 直接进入 Step 1       │
│  └─ 非完整 → 询问用户需求类型        │
└───────────────────────────────────────┘
        │
        ▼
   【用户确认制作方式（如需）】
        │
        ▼
┌───────────────────────────────────────┐
│  Step 1: 剧本生成                    │
│  输出3个剧本方案（A写实/B喜剧/C奇幻）  │
│  story_to_shots.py 编剧引擎           │
└───────────────────────────────────────┘
        │
        ▼
   【用户选择剧本方案】
        │
        ▼
┌───────────────────────────────────────┐
│  Step 2: 分镜方案                    │
│  输出3个分镜视觉方案                  │
│  (A纪录片质感/B喜剧风格/C超现实奇幻)   │
└───────────────────────────────────────┘
        │
        ▼
   【用户选择分镜方案】
        │
        ▼
┌───────────────────────────────────────┐
│  Step 3: 生成完整分镜 JSON           │
│  景别/运镜/情绪基调/视觉描述          │
└───────────────────────────────────────┘
        │
        ▼
   【用户逐镜确认】 ← 内容无误后进入制作
        │
        ▼
┌───────────────────────────────────────┐
│  Step 4: generate_shot_images.py      │
│  MiniMax image-01 文生图              │
│  帧①无参考 → 帧②-N传入前帧URL        │
└───────────────────────────────────────┘
        │
        ▼
   【用户抽检】 ← 可检查生成图片质量
        │
        ▼
┌───────────────────────────────────────┐
│  Step 5: generate_shot_videos.py      │
│  MiniMax I2V 图生视频                │
│  MiniMax-Hailuo-2.3                  │
│  支持运镜指令嵌入                     │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│  Step 6: merge_videos.py             │
│  ffmpeg concat 合并                  │
│  + storyboard.txt 故事板             │
└───────────────────────────────────────┘
        │
        ▼
最终视频 (./output/final_story.mp4)
```

### ⚠️ 费用说明

| 操作 | 消耗 | 说明 |
|------|------|------|
| LLM 剧本生图 | ~500 tokens/次 | 用于扩写剧本 |
| T2I 文生图 | ~10~30 tokens/张 | 每个镜头1张图 |
| I2V 图生视频 | ~100 tokens/镜头 | 6秒视频 |
| 合并+烧录 | 免费 | ffmpeg本地执行 |

> ⚠️ **MiniMax 图生视频（I2V）和文生图（T2I）均需要充值 Token**，请确保账户余额充足。

---

## ⚠️ 费用说明

**MiniMax API 需要充值 Token 才能使用。**

| 功能 | 消耗 Token | 说明 |
|------|-----------|------|
| 文生图（T2I） | 是 | image-01 模型，生成图片消耗 |
| 图生视频（I2V） | 是 | MiniMax-Hailuo-2.3，6s/10s 视频消耗 |
| LLM 分镜 | 否 | 使用配额内的对话 Token |

> 💡 **建议**：开始制作视频前确保 MiniMax 账户余额充足。T2I + I2V 组合使用消耗较快。

---

## 快速开始

### 环境配置

```bash
export MINIMAX_API_KEY="***"    # 必需
```

### 一键运行

```bash
cd ~/.hermes/skills/story-video-skill

python scripts/pipeline.py "你的故事大纲..."
```

### 分步运行

```bash
# Step 1: 故事 → 专业分镜
python scripts/story_to_shots.py "故事..." -o shots.json

# Step 2: 分镜 → 图片
python scripts/generate_shot_images.py -i shots.json -o images.json

# Step 3: 图片 → 视频
python scripts/generate_shot_videos.py -i images.json -p minimax -d 6

# Step 4: 合并
python scripts/merge_videos.py -i videos/ -o final.mp4
```

---

## 输出示例

### 分镜输出

```json
{
  "story_title": "勇气的旅程",
  "structure": "三幕结构",
  "shots": [
    {
      "shot_number": 1,
      "type": "establishing",
      "shot_size": "WS",
      "camera_movement": "static",
      "duration_suggestion": 5,
      "description": "小兔子站在黑暗山洞入口，阳光被高山遮挡",
      "visual_description": "一只白色小兔子站在阴暗山洞入口处，远处山峦叠嶂，阳光从山峰缝隙中射入一束金光，超广角镜头，电影感，暖色调与冷色调对比",
      "character_mood": "犹豫但坚定",
      "scene_transition": "CUT_TO"
    }
  ]
}
```

---

## 技术规格

| 模块 | 技术选型 |
|------|---------|
| 文生图 | MiniMax `image-01`，prompt ≤ 1500字符 |
| 图生视频 | MiniMax `MiniMax-Hailuo-2.3`，6s/10s，768P/1080P |
| 运镜控制 | 15种标准指令，支持组合与顺序 |
| 视频合并 | ffmpeg concat demuxer |
| LLM 分镜 | MiniMax `MiniMax-M2.7-highspeed` |

---

## 剧本格式规范参考

```
INT./EXT. 场景位置 - 时间
                        （场景描述）
人物正在做某事。

        角色名
    （动作）
对白内容...

                        CUT TO:
```

本 Pipeline 输出的分镜 JSON 可直接对接标准剧本格式，亦可作为 AI 视频生成的专业 Prompt 依据。

---

## 目录结构

```
story-video-skill/
├── SKILL.md                         # 技能定义
├── README.md                        # 本文件
├── scripts/
│   ├── pipeline.py                  # 主流水线
│   ├── story_to_shots.py            # 编剧+导演引擎
│   ├── generate_shot_images.py      # MiniMax 文生图
│   ├── generate_shot_videos.py      # MiniMax 图生视频
│   └── merge_videos.py             # ffmpeg 合并
└── references/
    ├── minimax-api/                 # MiniMax API 文档
    ├── screenwriting/               # 编剧理论体系
    └── director-knowledge/          # 导演知识体系
```
