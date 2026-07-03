# Mode A: First-time Setup (Guided Onboarding)

Run when user wants to set up token saving for the first time, or hasn't done it before.

---

## Step 1 — Scan

Run the scanner:
```bash
python3 <skill-install-path>/scripts/scan_workspace.py --workspace .
```

Present findings in plain language. Highlight estimated token savings. Ask user if they want to proceed with the suggested cleanups.

---

## Step 2 — Create memoryres/ (if missing)

```bash
mkdir -p memoryres  # in your workspace root
```

Explain: this is the "cold storage" tier — content that doesn't need to load every session but should still be findable.

---

## Step 3 — Move heavy sections, one at a time

For each HIGH/MEDIUM finding from the scan:

1. Show the user the section content (brief preview — heading + first 3 lines)
2. Confirm: "Move this to `memoryres/[suggested-name].md`?"
3. If yes:
   - **First, ask the user if they want a backup**: "需要我帮你备份这个文件吗？"
   - If user confirms: create a timestamped backup dir under `.backup/token-slim-undo-<ts>/` and copy the source file there; tell the user the backup path
   - Create the file in `memoryres/`
   - Replace the section in the source file with a one-line pointer: `→ 详见 memoryres/[filename]`
4. If no: skip and move to next

Do not move sections that are operational/behavioral rules (cron configs, safety rules, behavioral guidelines, etc.). These must stay always-on.

---

## Step 4 — Heartbeat file trim (if flagged)

If the heartbeat file exceeds 50 lines:
- Show the user any completed tasks or explanatory prose
- Suggest removing completed items and moving any long "why" explanations to the agent config file or memoryres/
- Ask before removing anything

---

## Step 5 — Deep scan (mandatory, do not skip)

After the first round of cleanup, always run a second pass manually — the scanner catches line counts but misses semantic issues:

- **Cross-file duplicates**: same table or rule appearing in two workspace files (e.g. persona config and memory index both have a dispatch table)
- **Template residue**: default English boilerplate left in files primarily written in another language (e.g. tool notes file "What Goes Here / Examples / Why Separate")
- **Stale pending items**: `⏳ 待确认` entries that haven't been resolved — move to `memoryres/pending-tasks.md`
- **Bootstrap files**: BOOTSTRAP.md is a one-time setup guide — if it still exists after setup, delete it immediately
- **Compressible prose**: long "why" explanations in group chat rules, expression-reaction guides, etc. — compress to 1–2 lines

After this pass, explicitly ask: "I found X more issues. Want me to clean those up too?" — do not wait for the user to ask.

---

## Step 6 — Session discipline (persist to workspace config, not just say it)

Do not just explain verbally — write it permanently into the workspace agent config file so it's enforced every session.

Check if the agent config file already contains a session discipline section using the anchor comment:
`<!-- token-slim:session-discipline-start -->`. If not, append:

```markdown
<!-- token-slim:session-discipline-start -->
## 话题切换提醒（节省 Token）

- 一个话题明显告一段落时，提示：「这个聊完了，要开新会话继续下一个话题吗？」
- 对话超过 20 轮 或 明显切换到新主题时，主动提示
- 完成大任务后，先把关键决策写一句到 `memory/YYYY-MM-DD.md`，再切换会话
<!-- token-slim:session-discipline-end -->
```

If the anchor `<!-- token-slim:session-discipline-start -->` already exists, skip (do not duplicate).

**Must do**: After writing (or confirming it already exists), explicitly tell the user: "✅ 「话题切换提醒」已写入工作区配置，每次会话将生效。"

---

## Step 7 — Completion checklist (mandatory)

Before declaring done, verify every step was completed. Do not skip this.

```
- [ ] Step 1: Scanner run, findings reviewed
- [ ] Step 2: memoryres/ directory exists
- [ ] Step 3: Heavy sections moved with pointers left behind
- [ ] Step 4: Heartbeat file trimmed if needed
- [ ] Step 5: Deep scan done, semantic issues addressed
- [ ] Step 6: Session discipline written to workspace agent config
- [ ] Step 7: Token habits written to workspace agent config
- [ ] Step 8: Completion checklist verified
- [ ] Step 9: Summary report delivered
```

---

## Step 8 — Inject token habits into workspace agent config

Check if the agent config file already contains the token habits section using the anchor:
`<!-- token-slim:token-habits-start -->`. If not, append:

```markdown
<!-- token-slim:token-habits-start -->
## 💡 Token 节省好习惯

每次对话，系统提示 + 历史消息 + 工作区文件全部重新注入。会话越长、任务越杂，消耗越高。

### 会话隔离（最高收益）
- **不相关的任务主动建议开新会话**，或用 `sessions_spawn` 开 subagent 后台处理
- 代码生成、数据查询、文档撰写等独立任务 → 天然适合 subagent，完成后通知结果
- 主会话只做调度和决策，保持上下文干净

### 提问方式
- 问题具体，一次问一件事；模糊大问题会产生长回答，长回答下轮全部携带
- 需要代码时提供明确约束（语言、范围、格式），减少来回迭代
- 要结论不要过程：「直接给我答案」比「帮我分析一下」省 token

### 工具使用
- 能用工具直接查的，不要靠 AI 凭记忆回答（减少 hallucination + 减少确认轮次）
- 大文件/长文本只贴相关片段，不要整段粘贴（每次都重新计费）

### 🔥 狂暴模式（最大化输出效率）<!-- 狂暴模式：已开启 -->
**核心思想：只要结论，不要过程。**
- 默认省略分析过程、推理链条、背景铺垫
- 直接给答案、给代码、给结论
- 除非用户明确说「解释一下」「为什么」，否则不展开
- 对话越短越好：一句话能说清的，绝不写段落
- 用「开启/关闭狂暴模式」随时切换
<!-- token-slim:token-habits-end -->
```

If the anchor `<!-- token-slim:token-habits-start -->` already exists, **replace the entire block** (from start to end anchor) with the latest template.

**Must do**: After writing (or confirming it already exists), explicitly tell the user:
- "✅ 「Token 节省好习惯」已写入工作区配置，每次会话将生效。"
- "✅ 「狂暴模式」已写入工作区配置，以后默认只给结论不给过程。"

---

## Step 9 — Summary

Report:
- Files modified and line counts before/after
- Total tokens saved per session
- Estimated daily savings = tokens saved × 100 sessions/day（基准：每天 100 个会话）
- Estimated monthly savings = daily × 22 working days（基准：每月 22 个工作日）
- Where the moved content now lives (so user can find it)

---

## Undo Mechanism

Before any file modification, always create a timestamped backup:

```bash
BACKUP_DIR=./.token-slim/undo-$(date +%Y%m%d-%H%M%S)
mkdir -p "$BACKUP_DIR"
# Copy the specific file(s) about to be modified, e.g.:
# cp <file-to-modify> "$BACKUP_DIR/"
```

To restore: copy files back from the latest backup directory.
Tell the user the backup path after every write operation so they can undo if needed.
