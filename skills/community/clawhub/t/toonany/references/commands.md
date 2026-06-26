# Toonany 命令参考

## 通用命令

### `/toonany new <name>`

创建新项目。

**前置条件**: 无
**交互**: 询问项目类型、风格、比例、集数
**输出**: 创建项目目录结构和 `project.json`

### `/toonany config`

检查并配置 API Key。

**前置条件**: 在项目目录中
**行为**:
- 检查 `project.json` 中各模型的 `apiKey`
- 解析 `${ENV_VAR}` 语法
- 发现缺失时，显示 provider 名称 + 申请链接 + 配置指引

### `/toonany validate`

运行全量校验。

**检查项**:
- 项目结构完整性
- 跨文件角色/场景/道具名称一致性
- 风格描述一致性
- 依赖追踪（检测过期文件）

### `/toonany export`

导出完整项目。

**输出**: `exports/{project-name}_{timestamp}/` 目录，包含所有文件和清单

## 快速模式

### `/toonany quick`

单命令交互式全流程。

**流程**:
1. 询问小说内容
2. 询问风格/比例/集数（或使用默认值）
3. 自动生成故事线 + 第1集大纲
4. 自动生成资产
5. 生成风格样张 → **用户确认**
6. 批量生成分镜图
7. 生成视频
8. 生成音频/字幕
9. 后期合成成片

**适合**: 新手快速体验

## 专业模式

### `/toonany story`

生成或修改故事线。

**输入**: 小说原文
**输出**: `storyline.md`
**需要模型**: `models.text`

### `/toonany outline [episode]`

生成或修改分集大纲。

**参数**:
- `episode`: 集数，如 `1` 或 `1-3`

**输入**: `storyline.md`
**输出**: `outline/outline-{ep}.md`
**需要模型**: `models.text`

### `/toonany assets`

提取并生成资产。

**输入**: `outline/*.md`
**输出**:
- `assets/characters.md`
- `assets/scenes.md`
- `assets/props.md`
- `assets/data.json`
- `assets/images/*`

**需要模型**: `models.text`（提取）, `models.image`（生成图片）

### `/toonany style-sample`

生成风格样张。

**输入**: `project.json` 中的 `artStyle`
**输出**: `assets/style-sample.jpg`
**需要模型**: `models.image`

**说明**: 风格样张是后续所有生成的视觉锚点，用户确认后再批量生产。

### `/toonany script [episode]`

生成剧本。

**输入**: `outline/outline-{ep}.md`
**输出**: `script/script-{ep}.md`
**需要模型**: `models.text`

### `/toonany storyboard [episode]`

生成分镜。

**输入**: `script/script-{ep}.md`
**输出**: `storyboard/storyboard-{ep}.md`
**需要模型**: `models.text`

### `/toonany storyboard-image [episode]`

生成分镜图。

**输入**:
- `storyboard/storyboard-{ep}.md`
- `assets/data.json`（资产引用）
- `assets/style-sample.jpg`（风格锚定）

**输出**: `storyboard/images/*.jpg`
**需要模型**: `models.image`

### `/toonany video [episode]`

生成视频。

**输入**: `storyboard/images/*.jpg`
**输出**: `video/ep{ep}-*.mp4`
**需要模型**: `models.video`

### `/toonany audio [episode]`

生成配音和字幕。

**输入**: `script/script-{ep}.md`
**输出**:
- `audio/ep{ep}/`（音频文件）
- `subtitle/ep{ep}.srt`（字幕）

**需要模型**: `models.audio`

### `/toonany finalize [episode]`

后期合成成片。

**输入**:
- `video/ep{ep}-*.mp4`
- `audio/ep{ep}/`（可选）
- `subtitle/ep{ep}.srt`（可选）

**输出**: `final/episode{ep}.mp4`

**依赖**: ffmpeg
