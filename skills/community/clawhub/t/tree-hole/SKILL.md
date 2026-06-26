---
name: tree-hole
description: |
  Anonymous story/confession submission to the community "tree hole" (树洞) Feishu form. Use when: (1) user wants to submit a story, confession, or thought anonymously, (2) user wants to share recent chat conversations anonymously, (3) user says "tree hole", "树洞", "submit story", "匿名投稿", "share anonymously", or similar phrases.
---

# Tree Hole — Anonymous Story Submission

Submit stories or chat conversations anonymously to the community Feishu form.

**Form URL:** `https://ainewmedia.feishu.cn/share/base/form/shrcn1AeCLxzQdV15UaxAzu2L0e`

## Setup
you need install agent-browser skill
```
clawhub install agent-browser
```

## Workflow

### 1. Determine Content Source

- **Original story**: User types or pastes their own content
- **Chat conversation**: Fetch with `sessions_history`, format as dialogue, anonymize PII, confirm with user

### 2. Submit (2 steps)

**Step 1 — Fill the story_input:**

```bash
agent-browser open https://ainewmedia.feishu.cn/share/base/form/shrcn1AeCLxzQdV15UaxAzu2L0e
agent-browser wait --load networkidle
agent-browser fill ".bitable-text-editor [contenteditable='true']" "THE STORY TEXT"
```

**Step 2 — Click submit:**

```bash
agent-browser click "button:has-text('submit')"
agent-browser wait --load networkidle
```

**Verify (optional):**

```bash
agent-browser screenshot result.png
```

### 3. Confirm

After submission, confirm success to the user. If login popup appears, the form's identity collection setting needs to be disabled in Feishu backend.

## Content Guidelines

- **Anonymize** real names, phone numbers, addresses before submitting
- **Preserve emotion** — feelings matter more than grammar
- **No judgment** — accept all submissions without editorial commentary
