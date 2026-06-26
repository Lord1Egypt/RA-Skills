# Micro Routing Examples

Use these examples to keep discovery vs reuse behavior stable.

## 1. User asks for a new skill, but installed skill is already enough
### Installed
- `github`: GitHub issues, PRs, releases, runs, and API operations
- `clawhub`: publish and manage skills on ClawHub

### User
- "给我装一个处理 GitHub issue 的 skill"

### Expected routing
- Prefer reuse first
- Recommend `github` instead of jumping to discovery

### Good answer
- "你现在已经有能覆盖这个任务的 `github` skill，先不用装新的。只有现有流程明显不够时，再去找更专门的 skill。"

---

## 2. No strong installed browser skill
### Installed
- `github`
- `weather`

### User
- "帮我控制浏览器点一下这个按钮"

### Expected routing
- Do not fake a browser skill
- Route to discovery

### Good answer
- "我现在没看到已安装的强匹配浏览器控制 skill。先走 `find-skills` 找候选；如果来源陌生，再用 `skill-vetter` 过一遍。"

---

## 3. Unknown third-party candidate
### Installed
- `find-skills`
- `skill-vetter`

### User
- "有没有帮我备份 OpenClaw 的 skill？"

### Expected routing
- Discovery first
- Vet unfamiliar candidates before recommending installation

### Good answer
- "先用 `find-skills` 看有没有备份类 skill；如果候选来自陌生第三方，先过 `skill-vetter`，再决定装不装。"

---

## 4. User is already in the right workflow
### Installed
- `pinchtab-browser`

### User
- "用 PinchTab 帮我打开这个网页，然后点登录"

### Expected routing
- Stay quiet about routing
- Do not add extra router commentary

### Good answer
- no routing nudge; let the browser skill workflow continue naturally

---

## 5. Multiple installed skills could fit
### Installed
- `github`
- `gh-issues`

### User
- "这个 issue 要不要直接拉个修复 PR？"

### Expected routing
- Recommend the more specific skill if it materially changes the next step

### Good answer
- "这个更偏 issue 驱动修复流，优先用 `gh-issues`；如果只是普通仓库查看或 release 操作，再回到 `github`。"

---

## 6. Installed weak match is enough
### Installed
- `summarize`

### User
- "帮我总结这个网页"

### Expected routing
- Reuse installed skill
- Do not discovery-chase a more specific summarizer unless current skill is clearly insufficient

### Good answer
- "这类任务你已经有 `summarize` 可以覆盖，先直接用它，不必再找新的网页总结 skill。"

---

## Rule

When in doubt, prefer:
1. sufficient installed skill reuse
2. discovery only after clear insufficiency
3. vetting before unfamiliar installation
