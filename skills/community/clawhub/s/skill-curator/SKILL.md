---
name: skill-curator
description: OpenClaw 的总调度 Skill。当用户在 Discord 发送「【关键词】URL」格式的消息时，自动触发本 Skill：判断该关键词对应的 Skill 是否已存在 → 提取 URL 内容 → 追加或新建知识 Skill → 推送到 GitHub skillhub 仓库。
---

# Skill Curator — 知识策展人

将任意来源的内容策展为可积累、可迭代的私人 Skill 知识库。

## 触发条件

用户发送格式：`【关键词】URL`

示例：
```
【python】https://bilibili.com/video/BVxxx
【写作技巧】https://mp.weixin.qq.com/s/xxx
【AI绘画】https://xiaohongshu.com/explore/xxx
```

## 完整工作流程

```
Discord 消息： 【关键词】URL
       │
       ▼
┌─────────────────────────┐
│ 1. parse_input          │ ← 解析关键词 + URL
│    keyword: "python"    │
│    url: "https://..."    │
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ 2. clone_repo            │ ← 克隆 GitHub 仓库到本地
│    github.com/           │
│    eeyan2025-art/        │
│    skillhub.git          │
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ 3. check_existing_skill  │ ← 判断 skill 文件是否已存在
│    skills/python/       │
│      └── SKILL.md        │
└──────────┬──────────────┘
    │ 存在       │ 不存在
    ▼            ▼
┌─────────┐  ┌──────────────────┐
│ 追加模式 │  │ 新建模式          │
└────┬────┘  └────────┬─────────┘
     │                 │
     ▼                 ▼
┌─────────────────────────┐
│ 4. extract_content      │ ← 根据 URL 类型提取内容
│   • 视频 → MiniMax 音视频 │
│   • 文章 → 网页抓取       │
│   • 输出：原文 + 摘要     │
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ 5. generate_skill       │ ← 生成/更新 SKILL.md
│   新建：完整 SKILL.md    │
│   追加：追加到现有文件    │
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ 6. git_push             │ ← 提交推送 GitHub
└──────────┬──────────────┘
           ▼
        完成！
```

## 输入格式

用户消息必须包含：
- `【】` 包裹的关键词（英文或中文均可）
- 一个有效的 URL

## URL 类型与处理方式

| URL 类型 | 处理方式 | 工具 |
|---------|---------|------|
| YouTube | MiniMax 音视频分析 | `videos_understand` |
| Bilibili | 网页提取字幕 + 音频分析 | `extract_content_from_websites` + `audios_understand` |
| 西瓜视频 | 音频分析 | `audios_understand` |
| 微信公众号 | 网页提取正文 | `extract_content_from_websites` |
| 小红书 | 音频分析 | `audios_understand` |
| 任意网页 | 提取正文 | `extract_content_from_websites` |

## 追加模式规则（已有 Skill 时）

追加内容到现有 SKILL.md 时：
1. **不要破坏现有结构**（frontmatter、章节结构保持不变）
2. 在正文末尾追加新内容，格式：

```markdown
---

## 【YYYY-MM-DD】新增：<来源标题>

<内容摘要>

来源：<URL>
```

3. 如果现有 Skill 已包含相同内容（重复检测），跳过不重复添加

## GitHub 仓库配置

默认仓库：`https://github.com/eeyan2025-art/skillhub.git`
默认分支：`main`
Skill 存放路径：`skills/<keyword>/SKILL.md`

## 环境变量

需要设置：
- `GITHUB_TOKEN`：GitHub Personal Access Token（拥有 repo push 权限）
- `MINIMAX_API_KEY`：MiniMax API Key（用于音视频分析）

## 错误处理

| 情况 | 处理 |
|------|------|
| GitHub 仓库无对应 Skill | 新建一个 |
| URL 无法访问 | 尝试降级方案或提示用户 |
| 内容提取失败 | 回复用户说明情况，附上可手动处理的方式 |
| Git push 失败 | 输出本地文件路径供手动处理 |

## 长期积累机制

每个关键词的 Skill 都是一个**持续生长的知识文件**，随时间越积越多。比如：

```
skills/
├── python/
│   └── SKILL.md   ← 不断追加，越来越大
├── 写作技巧/
│   └── SKILL.md
└── ai绘画/
    └── SKILL.md
```

用户无需每次指定"新建"，系统自动判断，自动迭代。
