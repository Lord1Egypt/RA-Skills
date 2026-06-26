---
name: qwen-vision-rename
description: 根据图片内容批量重命名本地图片文件。这是一个 skill，不是可调用工具；先用 read 打开本文件，再执行脚本命令，绝不能直接发出名为 qwen-vision-rename 的 tool call。用户提到“改名/重命名/按图片内容命名/整理图片文件名/整理图片”时必须使用本技能。默认直接执行改名，仅在用户明确要求“预览/试运行/dry-run”时先出计划不改文件。
metadata: {"openclaw":{"emoji":"🧭","requires":{"bins":["python3"],"env":["DASHSCOPE_API_KEY"]},"primaryEnv":"DASHSCOPE_API_KEY"}}
---

# Qwen Vision Rename Skill

Use this skill for:
- understanding image content (single image)
- batch generating content-based filenames for local image folders
- direct batch rename with rollback support
- naming pattern `类型-主题` (example: `邀请函-万人大会主视觉`)

## Runtime behavior (strict)

- `qwen-vision-rename` is a skill name, not a built-in tool name.
- First use the `read` tool to open this `SKILL.md`, then run the Python command below.
- Never emit a tool call named `qwen-vision-rename`.
- Always execute the script. Do not fabricate recognition results.
- For rename requests, default to direct execution: run `rename-dir --apply`.
- If the user explicitly says "预览/试运行/dry-run/先看方案", run without `--apply`.
- Do not call `qwen-image` for rename tasks.
- Requests like "整理图片/按内容分类整理" still map to this skill. This skill renames by content first; if the user explicitly asks to move files into folders, explain that separately.
- If user does not provide a folder path, run `rename-dir` without `--dir` and let script auto-select default image directory.
- Filename style should be `类型-主题` first, not only plain title.
- If `--apply` is used, return both `plan_file` and `rollback_file`.
- If command fails, explain failure in 2 short Chinese sentences and provide next fix.

## Setup

Install dependencies:

```bash
pip3 install -r {baseDir}/requirements.txt
```

Set API key:

```bash
export DASHSCOPE_API_KEY="your_api_key"
```

Optional model and endpoint:

```bash
export DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export DASHSCOPE_VISION_MODEL="qwen-vl-max-latest"
```

## Commands

Describe one image:

```bash
python3 {baseDir}/scripts/vision_rename.py describe \
  --image /path/to/image.jpg
```

Batch dry-run plan (recommended first step):

```bash
python3 {baseDir}/scripts/vision_rename.py rename-dir \
  --dir /path/to/images
```

Batch apply rename:

```bash
python3 {baseDir}/scripts/vision_rename.py rename-dir \
  --dir /path/to/images \
  --apply
```

Auto directory (no explicit `--dir`, script picks default image directory):

```bash
python3 {baseDir}/scripts/vision_rename.py rename-dir --apply
```

Rollback by rollback file:

```bash
python3 {baseDir}/scripts/vision_rename.py rollback \
  --rollback-file /path/to/rename-rollback-YYYYMMDD-HHMMSS.json
```

## Notes

- Supported image extensions: jpg, jpeg, png, webp, bmp, gif, tif, tiff, heic, heif.
- Default naming style: `类型-主题` (for example `邀请函-活动主视觉.jpg`).
- Duplicate names auto-suffix with `-02`, `-03` ...
- `rename-dir` writes a JSON plan file every run.
- `--apply` creates rollback JSON for reverse operation.
- If `--dir` is omitted, script tries `OPENCLAW_RENAME_DEFAULT_DIR`, then `~/图片`, then `~/Pictures`.
- On API failure for a single image, the default behavior is skip that file and continue.
