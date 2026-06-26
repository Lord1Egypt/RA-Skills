# xiaoshan-journal / 小山日记

> A personal diary automation skill for OpenClaw that writes daily journals and generates 1080px wide images.
> 
> OpenClaw 个人日记自动化 skill，自动撰写日记并生成 1080px 宽的标准图片。

## Features / 功能特性

**English:**
- **One-click execution**: Auto-detect config → Initialize (first run) → Write → Generate image
- **Config-driven**: All private paths (soul, memory, diary location) externalized to `config.yaml`
- **Auto-initialization**: Automatically detects environment paths on first use
- **1080px standard**: Generates images with exact 1080px width, auto-adaptive height
- **Triple fallback**: Browser → Chrome headless → Python PIL for image generation

**中文：**
- **一键执行**：自动检测配置 → 首次初始化 → 写作 → 生成图片
- **配置驱动**：私人路径（灵魂文件、记忆、日记目录）全部外置到 `config.yaml`
- **自动初始化**：首次使用时自动探测环境路径
- **1080px 标准**：生成宽度精确 1080px、高度自适应的图片
- **三级兜底**：Playwright（推荐）→ Chrome headless → Python PIL 绘图

## Installation / 安装

```bash
# Clone the repository
git clone https://github.com/1204TMax/xiaoshan-journal.git

# Copy the skill to your OpenClaw skills directory
cp -r xiaoshan-journal ~/.openclaw/skills/
```

## First Run / 首次使用

**English:**

1. The skill will detect that `config.yaml` doesn't exist
2. It will automatically:
   - Detect your environment paths (workspace, SOUL.md, MEMORY.md, etc.)
   - Create the diary directory if needed
   - Generate `config.yaml` with detected paths
3. Then proceed to write the diary for yesterday

**中文：**

1. Skill 会自动检测到 `config.yaml` 不存在
2. 自动执行：
   - 探测环境路径（工作区、SOUL.md、MEMORY.md 等）
   - 自动创建日记目录
   - 生成包含探测路径的 `config.yaml`
3. 然后继续执行写作流程（目标日期为昨天）

## Configuration / 配置

Copy the template and customize:

```bash
cd ~/.openclaw/skills/xiaoshan-journal
cp config.template.yaml config.yaml
```

Key settings / 关键配置项：

```yaml
profile:
  assistant_name: "Your Assistant Name"  # AI assistant persona / AI助手人设
  user_name: "Your Name"                 # User name / 用户名称

environment:
  timezone: "Asia/Shanghai"              # Timezone for date calculation / 时区

paths:
  soul_path: "~/.openclaw/workspace/SOUL.md"           # Assistant's soul / 助手灵魂文件
  memory_root_path: "~/.openclaw/workspace/MEMORY.md"  # Long-term memory / 长期记忆
  daily_memory_dir: "~/.openclaw/memory"               # Daily memory folder / 每日记忆目录
  diary_text_dir: "~/.openclaw/workspace/diary/text"   # Diary output folder / 日记输出目录

output:
  image_width: 1080                      # Image width in pixels / 图片宽度（像素）
```

## How It Works / 工作流程

### Step 0: Config Check / 配置检查
- If `config.yaml` exists → proceed to main workflow
- If not → run initialization workflow

### Step 1: Collect Materials / 收集素材
- Read `SOUL.md` (assistant's personality)
- Read daily memory (`YYYY-MM-DD.md`)
- Read recent journals (for style consistency)
- Optional: Read news summaries

### Step 2: Write / 写作
- First-person perspective
- Based on real materials (no fabrication)
- Natural, emotional tone
- Save to `diary_text_dir/YYYY-MM-DD.md`

### Step 3: Generate Image / 生成图片
Convert diary text to PNG with exact 1080px width:

1. **Option A**: OpenClaw Browser (preferred)
2. **Option B**: Chrome Headless
3. **Option C**: Python PIL (fallback)

All options validate pixel width after generation.

## File Structure / 文件结构

```
xiaoshan-journal/
├── SKILL.md                 # Main skill documentation / 主技能文档
├── INIT.md                  # Initialization workflow / 初始化工作流
├── config.template.yaml     # Configuration template / 配置模板
├── config.yaml              # Your private config (gitignored) / 私人配置（已忽略）
└── .gitignore               # Excludes private files / 排除私人文件
```

## Requirements / 依赖

- OpenClaw environment
- One of:
  - OpenClaw Browser (for screenshot)
  - Google Chrome (for headless screenshot)
  - Python with PIL (fallback rendering)
- `sips` (macOS) or ImageMagick (Linux) for image resizing

## Privacy / 隐私说明

Your personal configuration (`config.yaml`) containing names, paths, and preferences is **excluded from git** via `.gitignore`. Only the template and skill logic are shared.

你的个人配置（`config.yaml`，包含名称、路径、偏好）已通过 `.gitignore` **排除在版本控制外**。只有模板和技能逻辑会被分享。

## License / 许可

MIT License - Feel free to use and modify for your own diary automation.

## Credits / 致谢

Created by 小山 (Xiao Shan) for 大山 (Da Shan).

Originally a private customization, now open-sourced for anyone who wants an AI assistant to keep their daily journal.

最初为私人定制，现开源给任何想让 AI 助手帮忙写日记的人。
