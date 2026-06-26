# Report Generator EN

> A prompt-based skill powered by natural language that helps professionals quickly generate structured weekly reports. No coding, no dependencies, just Markdown + AI.

---

## ✨ Features

- 🎯 **Multi-role coverage**: frontend/backend/mobile/test engineers, operations, sales, HR, accounting, marketing, project management, and more
- 📋 **8+ professional templates**: role-specific formats ready to use out of the box
- 💡 **Insight first**: not just data listing - automatically highlights trends, anomalies, and action suggestions
- 📊 **Week-over-week analysis**: guides users to include last week's data for automatic comparison
- ⚡ **Zero learning curve**: pure natural-language input, professional report in about 2 minutes
- 🔧 **Flexible customization**: adjust tone (formal/concise), add data, and rewrite phrasing

---

## 🚀 Quick Start

### Step 1: Open an AI chat

Use any AI tool that supports custom prompts (for example: ChatGPT, Claude, Kimi, Qwen, etc.).

### Step 2: Load the skill

Copy and paste the full content of [SKILL.md](./SKILL.md) into your AI chat, or use it as a system prompt.

### Step 3: Describe your week

Describe your weekly work in natural language. The AI will generate a structured report automatically.

---

## OpenClaw-Ready Usage

This skill is optimized for OpenClaw-style prompt workflows:

- Use `SKILL.md` as a system prompt for consistent output
- Start with role + completed work + blockers + next week plan
- Use `/lang <code>` to request a different output language
- Use keywords like `compact` or `concise` for token-efficient output

### Recommended Input Schema

You can provide free text, or use this structured format:

```yaml
role: Backend Engineer
audience: Engineering Director
date_range: 2026-03-23 to 2026-03-27
tone: executive # executive | team-internal | concise
completed:
  - Refactored order service (70%)
  - Fixed 2 P1 production issues
in_progress:
  - Payment module architecture draft
blockers:
  - Waiting for API contract from platform team
next_week_plan:
  - Complete order service refactor
  - Begin payment module implementation
key_metrics:
  - API availability: 99.95%
  - Commits: 23
language: en
```

---

## 💬 Usage Examples

### Minimal mode (30 seconds)
```
I am a frontend engineer. This week I refactored the login page, fixed 3 bugs, and next week I will optimize homepage performance. Please generate my weekly report.
```

### Standard mode (1 minute)
```
I work in operations. This week I completed the 11.11 campaign plan, DAU increased 15% week over week, and I ran into vendor coordination issues. Next week I will push the campaign launch. Please generate my weekly report.
```

### Detailed mode (most complete)
```
Please generate my weekly report with the following information:
- Role: Backend Engineer
- Audience: Engineering Director
- Completed this week: User-center microservice split (80% done), API performance optimization (response time from 800ms to 200ms), fixed 2 production P1 bugs
- In progress: Order service refactor, expected to complete next week
- Issues encountered: Load testing failed due to DB connection pool configuration, now resolved
- Plan for next week: Complete order service refactor, start payment module development
- Key metrics: API availability 99.95%, 23 code commits
```

---

## 📁 File Structure

```
report-generator/
├── SKILL.md          # Core skill file (prompt + template library)
├── README.md         # Usage guide (this file)
└── LICENSE           # Open-source license
```

---

## 📋 Supported Report Types

| Template | Best For | Core Content |
|------|----------|----------|
| Generic Engineering Weekly Report | Frontend/Backend/Mobile/Test Engineers | Done, in progress, blockers, next-week plan |
| Executive/Management Weekly Report | Engineering Directors, Department Heads | TL;DR, key metrics, wins, risks |
| Team Weekly Report | Team Leads | Team capacity, task allocation, blockers, shout-outs |
| Sales Weekly Report | Sales, BD | Performance data, pipeline changes, customer follow-ups |
| Marketing Weekly Report | Marketing, Growth | Ad performance, content publishing, A/B tests |
| Project Status Report | Project Managers, PMO | Milestones, budget, risks, decision log |
| HR Weekly Report | HR, HRBP | Staffing changes, hiring progress, training/attendance |
| Operations Weekly Report | Ops, Product Ops | Core metrics, campaign outcomes, anomaly analysis |
| Finance Weekly Report | Accounting, Finance | Cash position, income/expense details, AR/AP |

---

## 🎨 Style Adjustments

After the report is generated, you can ask AI to refine it:

- `"Make the tone more formal"` - best for leadership reporting
- `"Make it shorter and keep only the most important points"` - best for quick syncs
- `"Add more detail to the data section"` - best for data-driven teams
- `"Generate an English version as well"` - best for international teams
- `"Convert this into email format"` - best for sending by email

---

## 💡 Best Practices

1. **Include last week's data**: comparison drives better insight
2. **Quantify outcomes**: "increased by 30%" is stronger than "improved"
3. **Explain blocker impact**: clarify what was affected and what support is needed
4. **Make plans specific**: include owner and timeline, not vague "continue next week"
5. **Use it regularly**: generate reports at a fixed weekly cadence to build trend history

---

## 🔧 Advanced Usage

### Use as a system prompt
Set `SKILL.md` as your AI system prompt. Then you can directly input weekly updates without reloading the prompt each time.

### Team-standard template
Team leads can customize templates in `SKILL.md` to standardize team reporting formats.

### Historical trend analysis
Save previous weekly reports as Markdown files. Attach historical data next time to let AI generate multi-week trend analysis.

### Versioning practice
When updating prompts/templates, keep a short changelog in your release notes so users know what changed (formatting, behavior, new templates, or quality rules).

---

## 📄 License

This project is released under the [MIT License](./LICENSE). You are free to use and modify it.

---

*Report Generator EN · Prompt-based Skill · No dependencies, natural-language driven*
