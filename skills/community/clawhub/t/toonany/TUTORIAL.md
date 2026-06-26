# Toonany 使用教程

Toonany 是一款 AI 漫剧创作助手，能够将小说自动转化为短剧内容。本教程将详细介绍如何使用 Toonany 完成从小说原文到完整漫剧的创作流程。

---

## 1. 简介

### 什么是 Toonany

Toonany 是一个基于 AI 的漫剧创作系统，核心理念是 **"Any story, any style, anyone"** —— 任何人都能把任何故事变成任何风格的漫剧。

### 核心特点

- **新手友好**: 引导式交互，缺什么补什么
- **快速模式**: `/toonany quick` 单命令走完完整流程
- **风格锚定**: 先确认风格样张，再批量生成，确保风格统一
- **角色一致**: 四视图参考图 + seed 锁定，跨集不变脸
- **完整管线**: 从小说到成片（含配音、字幕、混音）一站式完成

### 适用场景

- 网络小说作者将作品改编为短剧
- 内容创作者快速生成视频脚本和分镜
- 影视团队进行剧本开发和视觉预览
- AI 视频制作团队的工作流程管理

---

## 2. 安装

### 前提条件

- Python 3.9+
- ffmpeg（用于后期合成）

### 安装 ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows (使用 chocolatey)
choco install ffmpeg
```

### 安装 Python 依赖

```bash
cd ~/.claude/skills/toonany
pip install -r requirements.txt
```

### 验证安装

```bash
python scripts/init_project.py --help
```

---

## 3. 快速开始

### 3.1 创建项目

```
/toonany new 我的漫剧项目
```

系统会交互式询问：
- 项目类型（都市/古风/悬疑/科幻等）
- 艺术风格（从预设列表选择或自定义）
- 视频比例（16:9/9:16/1:1等）
- 计划集数

### 3.2 配置 API Key

首次使用时，系统会自动检测缺失的 API Key 并给出引导：

```
检测到以下 API Key 未配置：

【DeepSeek】- 用于 text 生成
申请地址: https://platform.deepseek.com/api_keys
配置步骤:
1. 访问 https://platform.deepseek.com 注册账号
2. 进入 API Keys 页面创建密钥
3. 复制密钥并执行: export DEEPSEEK_API_KEY=sk-xxx

配置完成后，请告诉我"已配置"，我会继续执行。
```

设置环境变量：
```bash
export DEEPSEEK_API_KEY="sk-xxx"
export VOLC_API_KEY="xxx"
export KLING_API_KEY="xxx"
export VOLC_TTS_API_KEY="xxx"
```

### 3.3 快速出片（推荐新手）

```
/toonany quick
```

跟随引导：
1. 提供小说内容（直接粘贴或上传文件）
2. 选择风格（从 20+ 种预设风格中选择）
3. 等待生成故事线和大纲
4. **确认风格样张**（关键步骤！确保风格符合预期）
5. 继续生成，最终输出成片

### 3.4 专业模式（推荐有经验的用户）

分阶段精细控制：

```
/toonany story           # 生成故事线
/toonany outline 1       # 生成第1集大纲
/toonany assets          # 提取资产
/toonany style-sample    # 生成风格样张
/toonany script 1        # 生成剧本
/toonany storyboard 1    # 生成分镜
/toonany storyboard-image 1  # 生成分镜图
/toonany video 1         # 生成视频
/toonany audio 1         # 生成配音和字幕
/toonany finalize 1      # 后期合成成片
```

---

## 4. 项目结构

```
output/{project-name}/
├── project.json              # 项目配置（含模型配置、角色seed等）
├── storyline.md              # 故事线
├── outline/                  # 分集大纲
│   ├── outline-01.md
│   └── ...
├── assets/                   # 资产
│   ├── characters.md         # 角色资产
│   ├── props.md              # 道具资产
│   ├── scenes.md             # 场景资产
│   ├── data.json             # 资产数据（程序格式）
│   ├── images/               # 资产图片
│   │   ├── characters/       # 角色四视图
│   │   ├── props/            # 道具图
│   │   └── scenes/           # 场景图
│   └── style-sample.jpg      # 风格样张（视觉锚点）
├── script/                   # 剧本
│   ├── script-01.md
│   └── ...
├── storyboard/               # 分镜
│   ├── storyboard-01.md      # 分镜文档
│   └── images/               # 分镜图
├── video/                    # 视频片段
│   └── ep01-*.mp4
├── audio/                    # 音频
│   └── ep01/
├── subtitle/                 # 字幕
│   └── episode01.srt
└── final/                    # 最终成片
    └── episode01.mp4
```

### project.json 说明

```json
{
  "name": "项目名称",
  "type": "都市",
  "artStyle": "2D动漫风格",
  "videoRatio": "16:9",
  "episodeCount": 12,
  "styleReference": "assets/style-sample.jpg",
  "versions": {},
  "models": {
    "text": {
      "provider": "deepseek",
      "model": "deepseek-chat",
      "apiKey": "${DEEPSEEK_API_KEY}",
      "baseUrl": "https://api.deepseek.com"
    },
    "image": {
      "provider": "volcengine",
      "model": "doubao-seedream-4-5",
      "apiKey": "${VOLC_API_KEY}",
      "baseUrl": "https://ark.cn-beijing.volces.com/api/v3"
    },
    "video": {
      "provider": "kling",
      "model": "kling-v1-pro",
      "apiKey": "${KLING_API_KEY}"
    },
    "audio": {
      "provider": "volcengine",
      "model": "zh_male_shaonianzixin_uranus_bigtts",
      "apiKey": "${VOLC_TTS_API_KEY}",
      "baseUrl": "https://openspeech.bytedance.com/api/v3/tts"
    }
  },
  "characters": [
    {
      "name": "角色名",
      "seed": 12345,
      "voiceType": "zh_male_shaonianzixin_uranus_bigtts",
      "filePath": "images/characters/角色名_grid.jpg"
    }
  ]
}
```

**重要字段说明**：
- `styleReference`: 风格样张路径，所有生成强制引用
- `versions`: 文件版本追踪，用于变更传播
- `characters[].seed`: 角色图像生成种子，确保一致性
- `characters[].voiceType`: 角色配音音色

---

## 5. 详细流程说明

### 5.1 故事线生成

Claude 分析小说内容，生成故事主线文档：

- **主题定位**: 一句话概括核心主题
- **主线剧情**: 2-3段概括主要剧情走向
- **人物关系**: 主要人物关系图或列表
- **情感基调**: 整体情感氛围描述

### 5.2 大纲生成

指定要生成的集数范围，系统生成分集大纲：

每集包含：
- **标题**: 8字以内，疑问/感叹句，含情绪爆点
- **章节范围**: 关联的原文章节号
- **核心矛盾**: `A 想要 X vs B 阻碍 X`
- **剧情主干**: 100-300字，按时间顺序
- **开场镜头**: 第一个视觉画面描述
- **剧情节点**: 【起】【承】【转】【合】四个事件
- **情绪曲线**: 如 `2→5→9→3`
- **视觉重点**: 3-5个标志性镜头
- **结尾悬念**: 下集预告钩子
- **角色/场景/道具**: 按出场顺序列出

### 5.3 资产提取与生成

系统自动提取三类资产：

- **角色资产**: 姓名、外貌、性格、服装、seed
- **道具资产**: 名称、外观、象征意义
- **场景资产**: 名称、环境、光线氛围

每个角色生成**四视图参考图**（正面、侧面、背面、特写），使用相同 seed 确保一致性。

### 5.4 风格样张（关键质量控制点）

在批量生成前，先生成 1-2 张风格样张：

```
/toonany style-sample
```

用户确认风格后，后续所有生成强制引用该样张作为参考图。如果不满意，修改 `artStyle` 后重新生成。

### 5.5 剧本创作

基于大纲生成详细对白剧本，格式规范：

- 纯文本格式，使用分镜符号（※ $ △ 【】等）
- 无 Markdown 语法
- 角色描述仅限服化道，禁止样貌描写
- 所有描写必须具体可拍摄

### 5.6 分镜设计

将剧本转化为可视化分镜：

- 每个分镜包含多个镜头（默认4个）
- 每个镜头标注：景别、角度、构图、光线、色彩、氛围
- 新增：建议时长、运镜方式（影响视频生成）

### 5.7 分镜图生成

使用图像模型生成分镜图：

- 强制引用风格样张
- 引用角色/场景参考图
- 生成宫格图后自动拆分为单张镜头图

### 5.8 视频生成

使用视频模型生成片段：

支持模式：
| 模式 | 说明 |
|------|------|
| text | 文生视频 |
| single | 单图生视频（最常用） |
| startEnd | 首尾帧模式 |
| multi | 多图参考模式 |

### 5.9 音频与字幕

- TTS 生成配音，按角色分配不同音色
- 字粒度时间戳智能合并为**句子级字幕**
- 支持情感标签

### 5.10 后期合成

```
/toonany finalize 1
```

自动执行：
1. 拼接视频片段
2. 混音（BGM + 配音 + 音效）
3. 字幕烧录
4. 输出最终成片

---

## 6. 常见问题

### Q: 没有 API Key 怎么办？

A: 执行 `/toonany config`，系统会自动检测缺失的 Key 并给出申请链接和配置指引。

### Q: 生成的角色在多集中不一致怎么办？

A: Toonany 使用四视图参考图 + seed 锁定机制。在 `project.json` 中检查角色的 `seed` 字段是否一致。如需调整，修改后重新运行 `/toonany assets`。

### Q: 风格不满意怎么办？

A: 在批量生成前，Toonany 会生成风格样张供你确认。如果不满意，可以修改 `project.json` 中的 `artStyle` 字段，然后重新运行 `/toonany style-sample`。

### Q: 修改了大纲，后续文件会联动更新吗？

A: Toonany 有依赖追踪机制。修改上游文件后，执行 `/toonany validate` 会提示哪些下游文件需要重新生成。你也可以手动重新运行对应阶段的命令。

### Q: 支持哪些视频比例？

- `16:9` - 横向标准视频
- `9:16` - 纵向短视频
- `1:1` - 方形
- `4:3` - 经典比例
- `3:4` - 纵向 3:4
- `21:9` - 宽银幕

### Q: 如何处理长篇小说？

对于长篇小说，建议分批处理：

1. 先导入前几章内容，生成故事线和前几集大纲
2. 确认风格和方向后，再导入后续章节
3. 可以针对特定章节范围生成大纲

### Q: 生成的提示词不理想怎么办？

1. **调整艺术风格**: 不同的 artStyle 会影响生成的提示词风格
2. **手动优化**: 在生成资产后，手动修改 `assets/` 目录下的提示词
3. **自定义提示词模板**: 修改 `prompts/assets/` 下的润色提示词文件

---

## 7. 命令参考

| 命令 | 说明 |
|------|------|
| `/toonany new <name>` | 创建新项目 |
| `/toonany config` | 配置/检查 API Key |
| `/toonany quick` | 快速模式（一键出片） |
| `/toonany story` | 生成故事线 |
| `/toonany outline [ep]` | 生成/修改分集大纲 |
| `/toonany assets` | 提取/生成资产 |
| `/toonany style-sample` | 生成风格样张 |
| `/toonany script [ep]` | 生成剧本 |
| `/toonany storyboard [ep]` | 生成分镜 |
| `/toonany storyboard-image [ep]` | 生成分镜图 |
| `/toonany video [ep]` | 生成视频 |
| `/toonany audio [ep]` | 生成配音和字幕 |
| `/toonany finalize [ep]` | 后期合成成片 |
| `/toonany validate` | 运行全量校验 |
| `/toonany export` | 导出项目 |

---

## 8. 脚本直接调用

除了通过 Claude Code 命令使用，你也可以直接调用 Python 脚本：

```bash
# 初始化项目
python scripts/init_project.py -i

# 生成资产
python scripts/generate_assets.py -p output/我的项目

# 生成分镜图
python scripts/generate_storyboard_images.py -p output/我的项目 -s storyboard-01.md

# 生成视频
python scripts/generate_video.py -p output/我的项目 --mode single

# 生成音频
python scripts/generate_audio.py -p output/我的项目 --episode 1

# 后期合成
python scripts/post_process.py -p output/我的项目 --episode 1

# 校验
python scripts/validate_project.py -p output/我的项目
python scripts/validate_consistency.py -p output/我的项目
```

---

## 9. 进阶技巧

### 自定义音色

在 `project.json` 中为每个角色配置 `voiceType`：

```json
{
  "characters": [
    {
      "name": "王林",
      "voiceType": "zh_male_shaonianzixin_uranus_bigtts",
      "voiceEmotion": "neutral"
    },
    {
      "name": "云梦",
      "voiceType": "zh_female_qingxin_wanquanxiaohe",
      "voiceEmotion": "gentle"
    }
  ]
}
```

### 批量生成多集

```bash
for i in {1..5}; do
  python scripts/generate_video.py -p output/我的项目 --episode $i
done
```

### 使用不同模型

修改 `project.json` 中的 `models` 配置即可切换不同 provider。

---

如需更多技术细节，请参考：

- [数据模型参考](references/data-model.md)
- [生产流程详解](references/workflow.md)
- [模型配置指南](references/model-config.md)
- [命令参考](references/commands.md)
