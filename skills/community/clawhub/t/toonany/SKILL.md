---
name: toonany
description: A Claude Code skill for creating AI-generated short dramas (漫剧) from novels and stories. Use when user mentions "漫剧创作", "小说转剧本", "分镜生成", "短剧制作", "故事线生成", "大纲创作", "AI视频", or wants to produce video content from written stories. Activates for tasks involving novel-to-drama conversion, script writing, storyboarding, or complete video production workflows.
version: "1.1.0"
metadata:
  openclaw:
    requires:
      env:
        - DEEPSEEK_API_KEY
        - VOLC_API_KEY
        - VOLC_TTS_API_KEY
      bins:
        - python3
        - ffmpeg
    primaryEnv: DEEPSEEK_API_KEY
---

# Toonany - AI漫剧创作助手

Toonany helps anyone turn any story into an AI-generated short drama through a guided production pipeline.

**核心理念**: Any story, any style, anyone.

## 快速开始（新手推荐）

从未用过？只需两步：

1. **创建项目**: `/toonany new 我的漫剧`
2. **快速出片**: `/toonany quick`（跟随引导完成全部流程）

## 命令列表

### 通用命令

| 命令 | 说明 |
|------|------|
| `/toonany new <name>` | 创建新项目，交互式配置 |
| `/toonany config` | 检查/配置 API 密钥，缺失时自动引导 |
| `/toonany validate` | 运行全量校验（结构 + 一致性） |
| `/toonany export` | 导出完整项目 |

### 快速模式

| 命令 | 说明 |
|------|------|
| `/toonany quick` | 单命令交互式全流程，30分钟出片 |

### 专业模式（分阶段精细控制）

| 命令 | 说明 |
|------|------|
| `/toonany story` | 生成/修改故事线 |
| `/toonany outline [ep]` | 生成/修改分集大纲 |
| `/toonany assets` | 提取/生成角色、场景、道具资产 |
| `/toonany style-sample` | 生成风格样张，确认后再批量生产 |
| `/toonany script [ep]` | 生成剧本 |
| `/toonany storyboard [ep]` | 生成分镜 |
| `/toonany storyboard-image [ep]` | 生成分镜图 |
| `/toonany video [ep]` | 生成视频 |
| `/toonany audio [ep]` | 生成配音和字幕 |
| `/toonany finalize [ep]` | 后期合成（拼接+混音+字幕烧录） |

## 前置检查（自动执行）

执行任何命令前，Toonany 会自动检查：

1. **项目存在**: 是否在有效的 toonany 项目目录中？
2. **API 配置**: 当前步骤所需的模型 API Key 是否已配置？
   - 未配置 → **自动引导**: 告诉用户去哪里申请、怎么设置
3. **上游依赖**: 当前步骤所需的输入文件是否存在？
   - 不存在 → 提示用户先完成上游步骤
4. **变更传播**: 上游文件是否已更新？
   - 已更新 → 提示用户下游产物可能已过期，建议重新生成

## 生产流程

```
小说原文 → 故事线 → 大纲 → 资产 → 风格样张 → 剧本 → 分镜 → 分镜图 → 视频 → 音频/字幕 → 成片
   1)       2)      3)     4)       5)          6)      7)       8)         9)       10)          11)
```

### 快速模式流程

```
/toonany quick
  → 询问小说内容
  → 询问风格/比例/集数
  → 自动生成故事线 + 大纲（第1集）
  → 自动生成资产
  → **生成风格样张 → 用户确认**
  → 批量生成分镜图
  → 生成视频
  → 生成音频/字幕
  → 后期合成输出成片
```

### 专业模式流程

用户逐步控制每个阶段，每步可审、可改、可回退。

## 数据模型

### Project

```json
{
  "name": "项目名称",
  "type": "都市/古风/悬疑/科幻",
  "artStyle": "2D动漫风格/真人写实/吉卜力",
  "videoRatio": "16:9/9:16/1:1",
  "episodeCount": 12,
  "styleReference": "assets/style-sample.jpg",
  "versions": {},
  "models": {
    "text": { "provider": "deepseek", "model": "deepseek-chat", "apiKey": "${DEEPSEEK_API_KEY}" },
    "image": { "provider": "volcengine", "model": "doubao-seedream-4-5", "apiKey": "${VOLC_API_KEY}" },
    "video": { "provider": "kling", "model": "kling-v1-pro", "apiKey": "${KLING_API_KEY}" },
    "audio": { "provider": "volcengine", "model": "...", "apiKey": "${VOLC_TTS_API_KEY}" }
  },
  "characters": [
    {"name": "角色名", "seed": 12345, "voiceType": "...", "consistencyId": "..."}
  ]
}
```

### 项目结构

```
output/{project-name}/
├── project.json              # 项目元数据
├── storyline.md              # 故事线
├── outline/
│   ├── outline-01.md         # 第1集大纲
│   └── ...
├── assets/
│   ├── characters.md         # 角色资产（详细描述）
│   ├── props.md              # 道具资产
│   ├── scenes.md             # 场景资产
│   ├── data.json             # 资产数据（程序格式）
│   ├── images/
│   │   ├── characters/       # 角色四视图 + 单张
│   │   ├── props/            # 道具图
│   │   └── scenes/           # 场景图
│   └── style-sample.jpg      # 风格样张
├── script/
│   ├── script-01.md          # 第1集剧本
│   └── ...
├── storyboard/
│   ├── storyboard-01.md      # 第1集分镜
│   └── images/               # 分镜图
├── video/
│   └── ep01-*.mp4            # 生成的视频片段
├── audio/
│   └── ep01/                 # 音频文件
├── subtitle/
│   └── ep01.srt              # 字幕文件
└── final/
    └── episode01.mp4         # 最终成片
```

## 新手引导

### 第一次使用？

1. 执行 `/toonany new 我的项目`
2. 系统会创建项目并检查 API Key
3. 如果缺少 API Key，会自动显示引导信息：
   - 告诉你需要哪些 provider
   - 提供申请链接
   - 告诉你怎么设置环境变量
4. 配置完成后，执行 `/toonany quick` 开始创作

### 缺少 API Key 时的引导示例

```
检测到缺少图像生成 API Key（火山引擎）。

请按以下步骤配置：
1. 访问 https://console.volcengine.com/ark/ 注册账号
2. 开通方舟大模型服务
3. 创建 API Key
4. 在终端执行: export VOLC_API_KEY=你的密钥

配置完成后，请告诉我"已配置"，我会继续。
```

## 质量保障

### 自动化检查

- **结构校验**: 检查项目目录和必需字段
- **一致性校验**: 检查角色名、场景名、道具名在全文中是否一致
- **风格漂移检测**: 对比不同阶段的风格描述是否一致

### 风格锚定

每部漫剧必须有1张**风格样张**作为视觉锚点。所有后续生成强制引用该样张，确保风格统一。

### 角色一致性

每个角色生成**四视图参考图**（正面、侧面、背面、特写），记录 seed 值。后续生成时复用 seed 和参考图，最大限度保持角色外观一致。

## 模型配置

支持的 provider：

| 类型 | Provider | 用途 |
|------|----------|------|
| text | deepseek, openai, anthropic, gemini | 故事线、大纲、剧本 |
| image | volcengine, kling, gemini | 资产图、分镜图 |
| video | kling, volcengine, vidu, gemini | 视频生成 |
| audio | volcengine, aliyun, edge-tts | 配音 |

在 `project.json` 的 `models` 字段中配置。API Key 推荐使用环境变量：`${ENV_VAR_NAME}`。

## 参考资料

- [详细教程](TUTORIAL.md) - 完整使用指南
- [数据模型](references/data-model.md) - 完整数据结构
- [生产流程](references/workflow.md) - Pipeline详解
- [模型配置](references/model-config.md) - AI模型配置指南
- [命令参考](references/commands.md) - 完整命令说明
