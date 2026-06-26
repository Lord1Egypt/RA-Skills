# 🎨 Visual Muse — ComfyUI AI 视觉缪斯


## 效果展示（Visual Muse 示例）

| ![赛博朋克霓虹少女](examples/cyberpunk_neon_girl.png) | ![赛博雨夜兜帽少女](examples/cyberpunk_hooded_hacker.png) | ![赛博都市耳机少女](examples/cyberpunk_street_girl.png) |
|---|---|---|
| 画一张赛博朋克风，霓虹雨夜中的未来少女特写 | 画一张赛博朋克风，绿色霓虹与兜帽黑客少女 | 画一张赛博朋克风，雨夜街头的耳机少女 |

| ![动漫霓虹机甲少女](examples/anime_neon_girl.png) | ![吉卜力花田小猫](examples/ghibli_cat_meadow.png) |  |
|---|---|---|
| 画一张高饱和动漫风，霓虹机甲耳机少女 | 画一张宫崎骏风格的猫在花田里奔跑 |  |

> 用自然语言对话生成 AI 图片的 OpenClaw 技能包

## 效果演示

对 OpenClaw 说：

```
画一张宫崎骏风格的猫在花田里奔跑
```

Agent 自动完成：中文理解 → 英文 prompt → 风格模板匹配 → ComfyUI 渲染 → 质量评分 → 输出图片

## 特性

- 🗣️ **自然语言驱动**：说中文就能出图，不需要懂 prompt 工程
- 🎭 **风格模板自动匹配**：电影感 / 动漫 / 写实 / 概念艺术 / 水彩
- 🔄 **多模型智能切换**：根据风格自动选择最合适的 checkpoint
- 📊 **质量评分**：自动评估构图、色彩、风格、细节、氛围
- 🧠 **偏好记忆**：记住你喜欢什么风格，越用越准
- 📋 **运行追踪**：每次生成的完整链路都有记录，方便复盘和优化

## 系统要求

- OpenClaw（最新版本）
- ComfyUI（本地运行，API 端口 8188）
- macOS Apple Silicon（推荐 16GB+ 内存）或 Linux + NVIDIA GPU
- 至少一个 SDXL checkpoint 模型（约 6.5GB）

## 安装

```bash
clawhub install visual-muse
```

安装后运行 setup 向导：

```bash
bash ~/.openclaw/workspace/skills/visual-muse/scripts/setup.sh
```

向导会帮你检查 ComfyUI 连接、模型状态，并初始化工作文件。

## 手动安装

如果不通过 ClawHub：

```bash
# 克隆到 workspace skills 目录
cd ~/.openclaw/workspace/skills/
git clone https://github.com/你的用户名/visual-muse.git

# 运行 setup
bash visual-muse/scripts/setup.sh
```

## 推荐模型

| 模型 | 风格 | 下载 |
|------|------|------|
| SDXL Base 1.0 | 基础通用 | [HuggingFace](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| DreamShaper XL | 万能型 | [HuggingFace](https://huggingface.co/Lykon/DreamShaper) |
| Juggernaut XL | 电影写实 | [HuggingFace](https://huggingface.co/RunDiffusion/Juggernaut-XL-v9) |
| Animagine XL 3.1 | 动漫 | [HuggingFace](https://huggingface.co/cagliostrolab/animagine-xl-3.1) |

## 风格关键词

| 你说的 | 匹配风格 | 使用模型 |
|--------|----------|----------|
| 电影感、大片、cinematic | cinematic | DreamShaper XL |
| 动漫、二次元、anime | anime | Animagine XL |
| 写实、照片、photo | photorealistic | Juggernaut XL |
| 概念、插画、concept | concept_art | DreamShaper XL |
| 水彩、水墨 | watercolor | DreamShaper XL |

## 目录结构

```
visual-muse/
├── SKILL.md                    # 主技能定义（ClawHub 入口）
├── README.md                   # 本文件
├── scripts/
│   └── setup.sh                # 安装向导
├── skills/
│   ├── prompt-agent/SKILL.md   # 中文→英文 prompt
│   ├── workflow-agent/SKILL.md # 工作流组装
│   ├── render-agent/SKILL.md   # ComfyUI 渲染执行
│   ├── critic-agent/SKILL.md   # 质量评分
│   └── memory-agent/SKILL.md   # 偏好记忆
├── tools/
│   ├── comfyui-client.py       # ComfyUI API 客户端
│   └── run-tracker.py          # 运行追踪
├── workflows/
│   └── sdxl_basic.json         # SDXL 基础工作流模板
└── resources/
    ├── prompt-templates.json   # 风格模板库
    └── preferences.json        # 偏好档案初始模板
```

## 工作原理

```
你说中文需求
    ↓
Prompt Agent（匹配风格模板 → 生成英文 prompt）
    ↓
Workflow Agent（选择 checkpoint → 填入工作流模板）
    ↓
Render Agent（调用 ComfyUI API → 等待生成）
    ↓
Critic Agent（评分 → 推荐最佳 → 给出改进建议）
    ↓
Memory Agent（记录你的偏好 → 下次更准）
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| COMFYUI_API_URL | http://127.0.0.1:8188 | ComfyUI API 地址 |

Docker 环境下通常设为 `http://host.docker.internal:8188`

## 常见问题

### ComfyUI 连不上
确保 ComfyUI 正在运行。macOS 用户可以安装 [ComfyUI Desktop](https://www.comfy.org/download) 或命令行启动。

### 出图很慢
M1/M2 芯片约 30-60 秒一张，M3/M4/M5 约 10-30 秒。首次加载模型会额外花 10-20 秒。

### 模型不存在
agent 会自动回退到 SDXL Base。确保至少下载了一个 checkpoint 到 ComfyUI 的 models/checkpoints/ 目录。

### 风格没变化
检查 prompt-templates.json 是否在 workspace 根目录，并确认 agent 能读取到。

## License

MIT-0

## 作者

Built with OpenClaw + ComfyUI + Claude

## 踩坑指南

首次使用遇到问题？查看 [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)，覆盖常见问题：黑图修复、Skill调度、Token优化、记忆系统、模型选择建议。

## 模型热切换

Visual Muse 支持一行命令在不同 LLM 之间切换 painter 模型：
```bash
bash scripts/switch-painter-model.sh gemini       # ~$0.005/次（推荐日常）
bash scripts/switch-painter-model.sh gpt-nano     # ~$0.003/次（最便宜）
bash scripts/switch-painter-model.sh claude       # ~$0.07/次（最强）
bash scripts/switch-painter-model.sh claude-haiku # ~$0.01/次
```

所有模型通过 Ofox (ofox.ai) 统一调用，无需分别注册。ComfyUI 本地推理完全免费，花钱的只是 LLM 理解需求的那一轮调用。
