# 🔒 Privacy & Data Governance — Writing Triadic

> **Last updated:** 2026-06-18
> **Applies to:** v2.9.2+

---

## 1. What This Skill Stores

Writing Triadic stores the following data locally to improve writing quality over time:

| Data Category | What | Where | Why |
|---------------|------|-------|-----|
| Writing Preferences | Tone, structure, word-choice likes/dislikes | `MEMORY.md` | Avoid repeating corrections |
| Style Fingerprint | 8-dimension writing style profile | `MEMORY.md` → `🧬 克隆档案` | Make outputs sound like you |
| SEO Profile | Keyword history, title preferences, intent distribution | `MEMORY.md` → `🔎 SEO 档案` | Optimize future content |
| Session State | Current mode, template, phase progress, decisions | `session-state.md` | Resume interrupted sessions |
| Drafts & Reviews | Generated drafts, reader scores, improvement notes | `{writing_root}/当前写作/` | Reference for iterations |
| Calibration History | User corrections to style fingerprint | `MEMORY.md` → calibration log | Improve fingerprint accuracy |

**All data is stored locally on your machine.** Nothing is uploaded to cloud services unless you explicitly opt in to web research (see §3).

---

## 2. Data Retention

| Data | Default Retention | How to Delete |
|------|-------------------|---------------|
| MEMORY.md profiles | 90 days from last update | Say "清除我的写作数据" or delete `{writing_root}/MEMORY.md` |
| Session folders | 30 days from session end | Say "清理写作会话" or delete `{writing_root}/当前写作/` |
| Style fingerprints | Until explicitly removed | Say "忘记我的写作风格" or delete `🧬 克隆档案` section in MEMORY.md |
| SEO profiles | 90 days from last update | Say "清除 SEO 档案" or delete `🔎 SEO 档案` section in MEMORY.md |

**Automatic cleanup:** The Evolution Engine will prompt you to review and optionally purge data older than 90 days.

---

## 3. Web Research (Network Transmission)

**Writing Triadic NEVER transmits your data without asking first.**

Before performing any web research:
1. The Creator will **explicitly ask** for your consent
2. It will show you the exact search queries it plans to send
3. You can say **"no"** — the skill will proceed offline with local knowledge only

**What gets transmitted:** Only the search keywords derived from your topic (not your full document, not your personal data, not your MEMORY.md).

**Privacy Mode:** Use `local privacy mode` to run entirely offline with Ollama models. No data ever leaves your machine.

---

## 4. Your Control Commands

| Command | Effect |
|---------|--------|
| "不要搜索" / "no web search" | Skip web research for this session |
| "这次不用我的风格" | Skip style fingerprint injection for this session |
| "忘记我的写作风格" | Delete all style fingerprints |
| "清除我的写作数据" | Delete all writing preferences and profiles |
| "清理写作会话" | Delete current session drafts and reviews |
| "显示我的数据" | Show everything currently stored about you |
| "local privacy mode" | Use Ollama models, no external API calls |

---

## 5. Data Minimization

- **Sub-agents (Executor, Reader):** Only receive the minimum data needed for their task. They DO NOT receive your full MEMORY.md. They receive only the current task's: template, rules, must-include/forbidden items, and relevant style preferences.
- **Cross-session linkage:** Your data is stored per writing type (e.g., "技术博客" vs "朋友圈") and isolated between types.
- **No behavioral surveillance:** Style drift detection only triggers when you explicitly request style cloning. It does not silently monitor all your writing.

---

## 6. Compliance

This skill is designed to respect:
- **GDPR** (Right to access, right to erasure, data minimization)
- **CCPA** (Right to know, right to delete, right to opt-out)
- **Privacy by Design** principles (proactive not reactive, privacy as default)

If you have privacy concerns, open an issue at:
https://github.com/sallyface0/writing-triadic/issues

---

## 7. What This Skill NEVER Does

- ❌ Send your data to third-party servers without consent
- ❌ Upload MEMORY.md or writing profiles to cloud services
- ❌ Use your data to train external models
- ❌ Share your preferences with other users
- ❌ Exfiltrate credentials or environment variables
- ❌ Execute system commands beyond file read/write in the writing workspace
