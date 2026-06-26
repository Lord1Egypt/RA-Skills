---
name: share2getnote
version: 1.0.0
description: >
  Parse ChatGPT or Gemini shared conversation links and save Q&A pairs as notes to GetNote (biji.com).
  Use when user provides a ChatGPT or Gemini share link and wants to import conversations as notes,
  or mentions saving AI chat history to GetNote/笔记.
description_zh: >
  解析 ChatGPT 或 Gemini 的分享对话链接，将问答对保存为 Get 笔记。
  当用户提供 ChatGPT/Gemini 分享链接并希望导入为笔记时使用，
  或用户提到将 AI 对话保存到 Get 笔记时使用。
---

# Share to GetNote

将 ChatGPT 或 Gemini 的公开分享对话导入为 Get 笔记。每轮问答生成一条独立笔记（问题为标题，回答为正文 MD 格式）。

## 触发条件

当用户提供的 URL 匹配以下模式时自动触发：

- `https://chatgpt.com/share/*`
- `https://chat.openai.com/share/*`
- `https://gemini.google.com/share/*`
- `https://g.co/gemini/share/*`

## 前置依赖

### 运行环境

需要 `uv` (Python 包管理器) 。脚本使用 PEP 723 内联依赖声明，`uv run` 会自动安装所需的 `playwright` 包。

检查 uv 是否可用：

```bash
uv --version
```

若未安装 uv，参考: https://docs.astral.sh/uv/getting-started/installation/

### GetNote Skill

需要 getnote skill 已安装并完成授权。检查方式：确认环境变量 `GETNOTE_API_KEY` 和 `GETNOTE_CLIENT_ID` 已设置，或 `~/.openclaw/openclaw.json` 配置文件存在。

若未配置，提示用户：
> 请先运行 `/note config` 完成 GetNote 授权配置。

getnote skill 安装地址: https://clawhub.ai/iswalle/getnote

## 核心工作流

### Step 1: 验证 URL

确认用户提供的 URL 匹配支持的分享链接格式。若不匹配，告知用户支持的格式。

### Step 2: 检查运行环境

确认 `uv` 可用。若不可用，告知用户安装方法。

### Step 3: 运行解析脚本

执行解析脚本提取对话内容（脚本首次运行时会自动安装 Playwright 和 Chromium）。

`SKILL_DIR` 为本 SKILL.md 文件所在的目录，请根据实际安装路径替换：

```bash
uv run SKILL_DIR/scripts/parse_share.py "<share_url>"
```

脚本输出 JSON 数组到 stdout：

```json
[
  {"title": "[1/3] 问题文本...", "content": "回答的 markdown 内容...\n\n---\n*来源: ...*"},
  {"title": "[2/3] 第二个问题...", "content": "第二个回答..."}
]
```

### Step 4: 展示结果并确认

解析 JSON 输出后，向用户展示：

```
成功提取 N 条笔记：
1. [标题1]
2. [标题2]
...

是否保存到 GetNote？
```

等待用户确认后继续。

### Step 5: 保存到 GetNote

逐条调用 getnote skill 的 `/note save` 命令保存笔记。对于每条笔记：

- 标题: JSON 中的 `title` 字段
- 正文: JSON 中的 `content` 字段（markdown 格式）

每保存成功一条，报告进度。

### Step 6: 汇报结果

保存完成后，向用户汇报：

```
已成功保存 N/M 条笔记到 GetNote。
[如有失败] 以下笔记保存失败：
- [标题]: [错误原因]
```

## 错误处理

| 脚本退出码 | 含义 | 处理方式 |
|-----------|------|---------|
| 1 | URL 不支持 | 告知用户支持的 URL 格式 |
| 2 | 页面加载失败/超时 | 提示链接可能已过期、已删除或需要登录 |
| 3 | 未找到对话数据 | 提示页面结构可能已变更，建议使用备用方案 |
| 4 | Playwright 未安装 | 引导用户安装 Playwright |

## 备用方案

当 Python 脚本失败时（如页面结构变更），使用以下备用流程：

1. 使用 browser-agent Task 工具打开分享链接
2. 等待页面加载完成后截取文本快照
3. 从快照文本中手动识别和提取 Q&A 对（用户消息和助手回复交替出现）
4. 按照相同格式组织为 `{title, content}` 结构
5. 继续 Step 4（确认）和 Step 5（保存）
