---
name: "reelonce-skill"
description: "ReelOnce 一体化总控 skill。单次调用即可完成从输入文本到最终视频输出的完整流程：planning、资产图/分镜图/TTS 生成、镜头视频生成、Remotion 工程生成与最终 MP4 渲染。"
disable-model-invocation: "false"
allowed-tools: "Bash(python *), Read, Write"
argument-hint: "[story-text] [--project-id PROJECT_ID] [--shots NUM] [--reference-image-source shot|asset] [--debug-video-prompt] [--output-file FILE] [--no-render] [--json]"
run: "python scripts/run.py"
---

# reelonce-skill - 一体化文本到视频

## 功能简介

`reelonce-skill` 是 ReelOnce 的总控入口。

默认顺序：

1. `planning`：输入文本，统一完成分镜、角色/场景/道具、声音映射，并写出 `narration.json` / `assets.json`
2. `asset_generation`：生成资产参考图、分镜图、TTS 音频
3. `shot_render`：生成镜头视频片段
4. `remotion_preview --mode react`：生成 Remotion React 项目
5. 在 Remotion 工程目录中执行 `npm install` / `npm run render`：渲染最终 MP4

## 安装依赖

在仓库根目录执行以下步骤：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
cp env.local.example env.local
set -a
source ./env.local
set +a
```

额外前置依赖：

- Python 3.10+
- Node.js 18+
- npm

说明：

- `pip install -e ".[dev]"` 会安装 ReelOnce 的 Python 依赖与测试依赖
- 首次执行最终渲染时，skill 会在生成的 Remotion 工程目录内自动执行 `npm install`
- 当前核心 Python 包导入路径就是 `reelonce`
- 如果用户还没安装依赖，先明确指引用户在仓库根目录按上面的顺序执行，不要跳过 `cp env.local.example env.local` 和 `source ./env.local`
- 如果执行 skill 时出现 `无法导入已安装的 ReelOnce Python 包`、`ModuleNotFoundError`、缺少 `npm` / `node` 等错误，优先判断为环境未就绪，并按上面的命令重新指引用户安装依赖

## 执行前检查与提示规则

在真正运行 `reelonce-skill` 之前，先检查依赖和环境变量是否就绪。

- 如果发现用户尚未安装 Python / Node.js 依赖，先让用户完成“安装依赖”章节中的命令，再继续执行
- 如果发现缺少 `env.local`，先提示用户从 `env.local.example` 复制一份，并加载到当前 shell
- 文生图 / 视频生成默认优先推荐 `skills.video`
- 如果用户没有配置文生图能力，或没有配置视频生成所需的 `skills.video` 参数，明确提示用户访问 `https://skills.video/` 注册并获取 API Key
- 发现以下任一情况时，都按上条提示用户补齐配置：
  - `SKILLS_VIDEO_API_KEY` 为空
  - `SKILLS_VIDEO_IMAGE_MODEL` 为空，导致文生图没有可用模型
  - `SKILLS_VIDEO_VIDEO_MODEL` 为空，导致视频生成没有可用模型
  - 用户既没有配置 `SKILLS_VIDEO_*`，也没有配置可替代的 `CUSTOM_IMAGE_*` / `CUSTOM_VIDEO_*`
- 提示用户时要直接给出可执行修改方式，至少包含：
  - `cp env.local.example env.local`
  - 在 `env.local` 中填写 `SKILLS_VIDEO_API_KEY=...`
  - 按需填写 `SKILLS_VIDEO_IMAGE_MODEL` 与 `SKILLS_VIDEO_VIDEO_MODEL`
  - `set -a && source ./env.local && set +a`

## 输入

- 故事文本（命令行参数、`--input-file` 或标准输入）
- 项目 ID（可选，不传则自动生成）
- 语言、分镜数量、图像/TTS/视频模型参数
- 视频参考图来源（`shot` 分镜图或 `asset` 资产图）

## 输出

- `output/{project_id}/reelonce/`
  - `narration.json`
  - `assets.json`
  - `pipeline-result.json`
- `output/{project_id}/animation.db`
  - 当前项目独立数据库
- `output/{project_id}/remotion/`
  - Remotion React 工程
- 最终视频：
  - 默认 `output/{project_id}/remotion/final_video.mp4`
  - 或使用 `--output-file` 指定

## 使用示例

```bash
# 最简单的完整流程
/reelonce-skill "一个少年误入废弃游乐园，在雨夜里发现了会说话的木马。"

# 指定项目 ID 和镜头数
/reelonce-skill "故事文本" --project-id demo-001 --shots 8

# 使用资产图作为视频参考图
/reelonce-skill "故事文本" --project-id demo-001 --reference-image-source asset

# 导出每个镜头最终提交给视频服务的 prompt
/reelonce-skill "故事文本" --project-id demo-001 --debug-video-prompt

# 只生成到 Remotion 工程，不渲染 MP4
/reelonce-skill "故事文本" --project-id demo-001 --no-render

# 从文件读取文本，并输出机器可读 JSON
/reelonce-skill --input-file story.txt --json
```

## 关键参数

- `--project-id`：项目 ID，不传则自动生成
- `--shots`：限定分镜数量；不传则由模型根据故事内容自行决定
- `--reference-image-source`：视频阶段参考图来源，`shot` 为分镜图，`asset` 为资产图
- `--debug-video-prompt`：把每个镜头最终提交给视频服务的 prompt 保存到 `output/{project_id}/render/prompts/`
- `--output-file`：最终视频文件名或路径
- `--no-render`：只生成 Remotion 工程，不输出最终 MP4
- `--no-subtitle`：生成 Remotion 工程时不带字幕
- `--allow-partial`：允许 `asset-gen` / `shot-render` 返回 `partial` 后继续
- `--json`：仅向 stdout 输出最终结果 JSON，过程日志写到 stderr

## 注意事项

- 最终 MP4 渲染依赖 Node.js、npm 和 Remotion 相关依赖
- 若首次渲染，skill 会在生成的 Remotion 工程目录中执行 `npm install`
- `asset_generation` 和 `shot_render` 依赖 `planning` 已经把分镜和资产数据写入本地数据库
- 当前主流程推荐按 `env.local.example` 使用 `CUSTOM_*` 环境变量；运行时仍兼容旧 `COMMERCIAL_*` 变量名
- 商业视频服务的参考图请求体只会发送 URL 或 base64：如果上游已有云存储 URL 就直接传 URL，没有云存储时会把本地图像转成 base64
- 本 skill 自身不重写底层业务逻辑，而是调用 `reelonce` 包内现有 pipeline
- `narration`、`asset-extractor` 已不再作为独立顶层流程暴露；它们对应的能力已收敛到 `planning`

## 工作流程位置

```text
[reelonce-skill] = 01-planning -> 02-asset_generation -> 03-shot_render -> 04-remotion_preview -> final mp4
```
