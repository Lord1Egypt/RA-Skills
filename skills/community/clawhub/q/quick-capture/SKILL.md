---
name: quick-capture
description: "帮用户把信息写入笔记系统：碎片化信息原样追加到当日 Journal（不改），待整理的笔记归纳成结构化知识写到 Inbox（要完善）。触发于：记笔记、记碎片、存一下、写到 inbox/journal 等。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "bins": ["python3"] },
        "install": [],
        "homepage": "https://github.com/daowuu/elysia"
      },
  }
---

# Quick Capture

把用户输入快速写入笔记系统的 `Inbox` 或 `Journal`。

## 什么时候用

当用户要你：

- 记一下 / 记录一下 / 收一下 / 存一下
- 放到 Inbox
- 写到 Journal / 今日日记
- 记录碎片化想法、观察、灵感、临时上下文

## 去哪里

- `Inbox`
  - 用于待处理记录、链接收藏、稍后整理的素材、还没分流的信息
  - 用户没明确说写到 Journal 时，默认写这里
- `Journal`
  - 用于当天碎片化信息、临时想法、现场观察、过程片段
  - 追加到今日日记，并按 `---` 分块

## 执行方式

优先使用脚本：

```bash
python3 $SKILLS_ROOT/quick-capture/scripts/capture_note.py inbox --title "标题" --content "内容"
python3 $SKILLS_ROOT/quick-capture/scripts/capture_note.py journal --title "分块标题" --content "内容"
```

可选参数：

```bash
--source-url "https://example.com"
--tags "AI, 推荐系统"
```

说明：

- `--tags` 只对 `Inbox` 生效
- `Journal` 如果不传标题，会自动用当前时间作为块标题
- `Inbox` 如果不传标题，会从正文第一条有效内容生成标题

## 工作规则

**两套处理逻辑，务必区分清楚：**

- **Journal（碎片化信息）**
  - 用户说"记碎片""今天""journal""日记"时写这里
  - 原样追加，不修改、不总结、不完善
  - 只保留原始内容，保持本来面目

- **Inbox（待整理的笔记）**
  - 用户说"记笔记""记一下""存到 inbox"时写这里
  - 主动理解内容，归纳整理成结构化知识笔记
  - 补充缺失背景、完善结构、给出定义/思路/应用场景
  - 不能机械堆砌原文，要当成在写自己的知识库
  - **公式一律用 LaTeX 编写**，用 `$\inline$` 或 `$$\block$$` 格式

- **默认行为**
  - 用户只说"记一下""存一下"时，默认写 `Inbox` 并完善
  - 只有明确说"碎片""journal""日记"时才写 Journal

- 不要先问一堆问题，优先直接落笔

## 输出要求

- `Inbox`：创建一篇结构完整的知识笔记
- `Journal`：追加原始分块，不加工
- 回答尽量简短：
  - `已写入 Inbox：Inbox/2026/2026-03/...`
  - `已追加到今日日记：Journal/2026/2026-03/2026-03-18.md`

## 输出要求

- `Inbox`：创建一篇新笔记
- `Journal`：追加到今日日记，形成一个新的 `---` 分块
- 回答尽量简短，例如：
  - `已写入 Inbox：Inbox/2026/2026-03/...`
  - `已追加到今日日记：Journal/2026/2026-03/2026-03-18.md`
