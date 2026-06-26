---
name: video-to-skill
description: 自动从任意视频链接（YouTube、Bilibili、西瓜视频、抖音、小红书视频等）生成 OpenClaw Skill 并上传到 GitHub。用户分享任意视频链接，希望将其内容自动转化为 Skill 时触发。
---

# 视频 → Skill 生成器

将全平台视频自动转化为 OpenClaw Skill 并推送到 GitHub。

## 支持平台

| 平台 | 字幕/音频 | 备注 |
|------|-----------|------|
| YouTube | ✅ | 字幕 API 直接提取 |
| Bilibili（哔哩哔哩） | ✅ | 字幕或音频提取 |
| 西瓜视频 | ✅ | 音频为主 |
| 抖音 | ⚠️ | 音频提取 |
| 小红书视频 | ⚠️ | 音频提取 |
| 其他平台 | ⚠️ | 音频提取 |

## 工作流程

```
video_url
    │
    ▼
┌─────────────────────────┐
│  1. detect_platform     │  ← 识别平台类型
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│  2. extract_content     │  ← 提取字幕/音频
│     (平台适配)           │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│  3. transcribe_summarize│  ← MiniMax 统一处理
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│  4. extract_skill       │  ← 生成 SKILL.md
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│  5. git_push             │  ← 推送到 GitHub
└─────────────────────────┘
```

## 输入

- `video_url`: 任意平台视频链接

## 输出

- `skill_md_file`: 生成的 SKILL.md 文件路径
- `github_link`: GitHub 文件访问链接

---

## Step 1: detect_platform

根据 URL 判断平台：

| 平台 | URL 特征 |
|------|---------|
| YouTube | `youtube.com`, `youtu.be` |
| Bilibili | `bilibili.com`, `b23.tv` |
| 西瓜视频 | `ixigua.com` |
| 抖音 | `douyin.com`, `v.douyin.com` |
| 小红书 | `xiaohongshu.com`, `xhslink.com` |

## Step 2: extract_content

### YouTube
使用 `audios_understand` 工具直接分析视频 URL：
```
prompt: "请提取视频的完整字幕/文字内容，以及视频主题和摘要"
file: video_url
```

### Bilibili / 西瓜 / 抖音 / 其他
尝试 `extract_content_from_websites` 提取页面字幕：
- 访问视频页面
- 从 HTML 中提取字幕 JSON 或 SRT 格式内容

若字幕提取失败，降级为**音频下载**：
```bash
# 通过 MiniMax audios_understand 直接处理
使用 audios_understand 工具：
  file: 直接传音频URL（部分平台支持）
  prompt: "请完整转录这段音频内容，保留所有关键信息"
```

## Step 3: transcribe_summarize

使用 MiniMax `audios_understand` 或 `llm-task` 处理：

```json
{
  "prompt": "你是一个视频内容分析助手。请根据以下视频字幕/转录，生成：1）完整文字稿（video_transcript_md）；2）视频摘要（video_summary_md，包含主题、关键知识点、主要内容、总结）。",
  "input": "<字幕或转录内容>",
  "schema": {
    "type": "object",
    "properties": {
      "topic": {"type": "string"},
      "key_points": {"type": "array", "items": {"type": "string"}},
      "summary": {"type": "string"},
      "transcript": {"type": "string"}
    }
  }
}
```

## Step 4: extract_skill

调用 LLM 根据摘要生成 SKILL.md：

```json
{
  "prompt": "你是一个 Skill 设计助手。请根据以下视频摘要，生成一个标准的 OpenClaw SKILL.md 文件。\n\n【视频摘要】\n{video_summary_md}\n\n要求：\n1. name: 英文小写+短横线（最多64字符）\n2. description: 具体说明触发条件和使用场景\n3. 正文包含：工作流程、步骤、示例、注意事项\n4. 用中文输出，工作流程要可执行",
  "model": "minimax/auto"
}
```

保存到 `/tmp/generated_skill.md`。

## Step 5: git_push

```bash
SKILL_FILE="/tmp/generated_skill.md"
REPO="https://github.com/eeyan2025-art/skillhub.git"
BRANCH="main"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

# 提取 skill name
SKILL_NAME=$(sed -n '/^---$/,/^---$/p' "$SKILL_FILE" | grep '^name:' | sed 's/^name: *//' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# 克隆仓库
git clone "https://${GITHUB_TOKEN}@github.com/eeyan2025-art/skillhub.git" /tmp/skillhub_push

# 复制文件
mkdir -p "/tmp/skillhub_push/skills/$SKILL_NAME"
cp "$SKILL_FILE" "/tmp/skillhub_push/skills/$SKILL_NAME/SKILL.md"

# 提交推送
cd /tmp/skillhub_push
git add .
git commit -m "Add skill from video: $SKILL_NAME"
git push

echo "https://github.com/eeyan2025-art/skillhub/blob/main/skills/$SKILL_NAME/SKILL.md"
```

## 环境变量

```bash
export GITHUB_TOKEN="your_github_pat_token"
# MiniMax API Key（若使用 llm-task 或 audios_understand）
export MINIMAX_API_KEY="your_minimax_key"
```

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 字幕提取失败 | 自动降级：尝试音频分析 |
| 音频分析失败 | 尝试 videos_understand 直接分析视频 |
| Git 推送失败 | 输出本地文件路径，提示手动处理 |
| API 超时 | 重试 1 次，间隔 10 秒 |
