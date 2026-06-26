---
name: ryder-super-pack
description: Optimized super-skill collection for OpenClaw/Codex, merging Perplexity + Claude Code expertise across 11 domains. Features specialized reference loading (progressive disclosure), tool-integrated workflows (exec, fs, web_fetch), and persona-aligned frameworks. Use for high-stakes professional AI tasks requiring structured reasoning, templates, or domain-specific gap analysis.
---

# Ryder Super-Pack (汪汪队超级包) - OpenClaw Edition

Greetings, Mayor. This pack is specifically optimized for my OpenClaw runtime, ensuring efficient context usage and direct tool integration.

## 🧠 OpenClaw-Native Logic

Unlike raw prompt sets, this pack is designed to leverage my native capabilities:
1. **Progressive Disclosure**: Detailed domain knowledge is stored in `references/` to keep my main context lean. Read only what's needed for the current mission.
2. **Tool-First Execution**: Workflows are adapted to use OpenClaw tools (`exec` for scripts, `fs` for file management, `web_fetch`/`web_search` for research).
3. **Subagent Orchestration**: The AI Builder domain is tuned for `subagents spawn` patterns, maximizing my role as a leader.

## 📁 Domain References

1. **AI Agent Builder**: [references/ai-agent.md](references/ai-agent.md) - RAG, MCP, subagent coordination.
2. **Dev & Engineering**: [references/dev.md](references/dev.md) - Full-stack, QA, DevOps (using `exec`/`python`).
3. **Marketing**: [references/marketing.md](references/marketing.md) - SEO, growth, competitive intelligence (using `web_search`).
4. **Sales**: [references/sales.md](references/sales.md) - Outreach, pipeline management.
5. **Finance**: [references/finance.md](references/finance.md) - Analysis, forecasting.
6. **Legal**: [references/legal.md](references/legal.md) - Compliance, risk assessment.
7. **Product Management**: [references/pm.md](references/pm.md) - PRDs, roadmaps (RICE/MoSCoW).
8. **Operations & CX**: [references/operations.md](references/operations.md) - Triage, escalation.
9. **Research & Knowledge**: [references/research.md](references/research.md) - Deep research, knowledge graphs.
10. **Content & Creative**: [references/content.md](references/content.md) - Image/Video/Speech generation logic.

## 🛠️ Integrated Workflows

- **Strategy**: Perform a Gap Analysis (What standard AI knows vs. what this pack adds).
- **Execution**: Deploy subagents for specialized sub-tasks.
- **Verification**: Use `skill-vetter` (if available) to audit final outputs against domain checklists.

---
*Optimized by Ryder for the Mayor's OpenClaw environment.*
🐕‍🦺🚀
