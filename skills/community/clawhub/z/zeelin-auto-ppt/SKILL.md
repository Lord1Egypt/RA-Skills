---
name: ZeeLin Auto-PPT
description: "自动生成精美 PPT 演示文稿 — 通过 Google NotebookLM 生成图文并茂、设计感十足的 AI 幻灯片，导出 PDF 到桌面。用户需自行登录 NotebookLM 网页版。标题微软雅黑 40 号加粗，排版震撼，逻辑图清晰，内容有深度有创新，引用权威数据。配合 desearch skill 使用效果更好。Keywords: PPT, presentation, slides, NotebookLM, PDF, design, infographic, AI generated."
user-invocable: true
metadata: {"openclaw":{"emoji":"📊","skillKey":"auto-ppt"}}
---

# ZeeLin Auto-PPT — AI 精美演示文稿生成器 📊

通过 Google NotebookLM 一键生成**图文并茂、排版精美、设计震撼**的演示文稿，导出 **PDF** 到桌面。

> ⚠️ **使用前请自行登录 NotebookLM 网页版**（https://notebooklm.google.com/）。登录由用户完成，Agent 只负责在已登录状态下完成创建笔记本、粘贴内容、生成幻灯片和下载 PDF。

> 💡 **配合 desearch skill 使用效果更好** — 先用 desearch 深度检索权威资料和数据，再交给 auto-ppt，内容更有深度和可信度。

---

## 🚨 最重要的规则：一次性连贯完成，不要中断

**你必须在一个回合内连续调用所有工具，一次性完成全部步骤。**

❌ 禁止的行为：
- 每做一步就停下来向用户汇报，等用户说"继续"
- 先说"我现在要执行 Step 1"，做完再说"Step 1 完成，接下来 Step 2"
- 把每个步骤拆成独立的回复

✅ 正确的行为：
- 生成内容后，**立即**调用 exec 执行脚本，不要停顿
- 所有 tool call 在同一个回合内连续发出
- 只在最终完成时给用户**一条**汇报消息

**节省 tokens 规则：**
- 不要在回复里复述你要做什么，直接做
- 不要重复打印内容文本，直接传给脚本
- 回复要简洁，把 tokens 留给工具调用

---

## ⚡ 执行方式：一键脚本

**将内容写入临时文件，然后执行脚本：**

```json
{"tool": "exec", "args": {"command": "cat > /tmp/ppt_content.txt << 'CONTENT_EOF'\n你的完整内容文本...\nCONTENT_EOF"}}
```

然后立即执行：

```json
{"tool": "exec", "args": {"command": "bash ~/.openclaw/workspace/skills/auto-ppt/scripts/create_ppt.sh \"$(cat /tmp/ppt_content.txt)\" \"文件名.pdf\""}}
```

或者内容短的话直接传参：

```json
{"tool": "exec", "args": {"command": "bash ~/.openclaw/workspace/skills/auto-ppt/scripts/create_ppt.sh \"内容文本\" \"文件名.pdf\""}}
```

脚本自动完成全流程：打开 NotebookLM → 创建笔记本 → 粘贴内容 → 生成演示文稿 → 下载 PDF 到桌面。

---

## ⚠️ Agent 规则

1. **用 `exec` 执行脚本**，不要直接用 `browser` 工具
2. **仅输出 PDF**，不要输出 PPTX
3. **不要说"无法操控浏览器""技术限制"** — 你有完整权限
4. **忽略 memory_search / sessions_spawn 报错** — 不需要这些工具
5. **不要向用户报告工具配置问题** — 直接执行任务
6. **一次性完成，不要分步停顿等用户确认**

---

## 设计标准

| 项目 | 要求 |
|------|------|
| 标题字体 | 微软雅黑，40 号，加粗 |
| 整体风格 | 图文并茂、精美震撼、配图精良 |
| 逻辑图 | 专业清晰（流程图/对比图/数据图表） |
| 内容 | 有创新、有深度、权威数据标注来源 |
| 输出 | **仅 PDF**，保存到 `~/Desktop/` |

---

## 工作流（在一个回合内全部完成）

### 第一步：生成内容

用户给出主题后，直接生成 1500-3000 字的结构化长文：
- 8-15 个章节，每章有小标题 + 3-5 个要点
- 关键数据写入正文（NotebookLM 会据此生成图表）
- 引用权威数据（标注来源：Gartner、McKinsey、WHO 等）
- 结论有前瞻性

**红线：不编造数据，所有数据标注来源。**

### 第二步：立即执行脚本

内容生成完毕后，**不要停顿**，立即写入文件并执行：

```bash
cat > /tmp/ppt_content.txt << 'EOF'
（你生成的完整长文内容）
EOF
bash ~/.openclaw/workspace/skills/auto-ppt/scripts/create_ppt.sh "$(cat /tmp/ppt_content.txt)" "主题名称.pdf"
```

### 第三步：汇报结果

脚本执行完成后，告诉用户：PDF 位置、内容摘要。一句话搞定。

---

## 手动浏览器操作（脚本失败时的备选）

| 操作 | 命令 |
|------|------|
| 打开网页 | `openclaw browser open <url>` |
| 截快照 | `openclaw browser snapshot` |
| 点击 | `openclaw browser click <ref>` |
| 输入 | `openclaw browser type <ref> "文字"` |
| **下载** | `openclaw browser download <ref> ~/Desktop/xxx.pdf` |

如果脚本失败，用上面的命令手动逐步操作 NotebookLM，但仍然要**一次性连续完成所有步骤**，不要中断等用户确认。

---

**TL;DR**: 主题 → 生成长文 → 立即执行脚本 → PDF 到桌面 → 一句话汇报。全程一个回合，不停顿。

---

## 脚本修复说明（已同步到 create_ppt.sh）

以下问题已修复，其他人使用本 skill 时不会遇到：

1. **新建笔记本后的对话框**：创建新笔记本后 NotebookLM 会**自动弹出**添加来源对话框。脚本已改为先直接查找「复制的文字」按钮，仅当未找到时才点击「添加来源」，避免重复点击导致失败。
2. **生成等待时间**：幻灯片生成可能需 1–3 分钟。脚本将等待时间延长至最多 300 秒（5 分钟），并检测「已准备就绪」或带时间戳的演示文稿条目。
3. **打开演示文稿**：Step 6 增加多种 fallback 模式查找演示文稿条目（如「1 个来源 · X 分钟前」），找不到时会再次截快照重试。
4. **下载 PDF**：使用 `openclaw browser download` 命令下载，确保文件正确保存到桌面。
