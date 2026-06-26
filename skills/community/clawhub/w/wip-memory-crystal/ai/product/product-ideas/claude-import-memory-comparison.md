# Product Idea: Claude's Import Memory vs Memory Crystal

**Date:** 2026-03-01
**Trigger:** Anthropic launched `claude.com/import-memory` on 2026-03-01

---

## What Anthropic Built

Anthropic launched a "Switch to Claude without starting over" feature. The flow:

1. Copy a prompt from `claude.com/import-memory`
2. Paste it into your current AI (ChatGPT, Gemini, etc.)
3. The prompt asks the AI to dump all stored memories: instructions, tone preferences, personal details, name, location, job, family, interests
4. Copy the output (a single code block)
5. Paste it into Claude's settings (Settings > Capabilities > Memory > Start import)
6. Claude extracts key info and stores it as individual memory entries
7. Wait up to 24 hours for it to take effect

Available on Pro, Max, Team, and Enterprise plans.

Source: https://claude.com/import-memory
Simon Willison coverage: https://simonwillison.net/2026/Mar/1/claude-import-memory/

---

## How This Differs from Memory Crystal

| Dimension | Anthropic Import Memory | Memory Crystal (Total Recall + Dream Weaver) |
|-----------|------------------------|----------------------------------------------|
| Method | Copy-paste prompt into old AI | API connection to provider accounts |
| Scope | Whatever the AI remembers about you | Full conversation history (every message) |
| Frequency | One-time migration | Continuous or on-demand |
| Processing | Claude extracts key facts from text dump | Dream Weaver Protocol: narrative consolidation, meaning extraction |
| Storage | Anthropic's servers (Claude memory) | Your local machine (sovereign) |
| Searchable | Only within Claude | Across all agents, all devices, all interfaces |
| Format | Unstructured text blob | Embedded vectors + FTS, hybrid search |
| Provider lock-in | Moves you from one lock-in to another | No lock-in. Your memory is yours. |
| Ongoing capture | No. One-time import. | Yes. Every conversation captured automatically. |

**The fundamental difference:** Anthropic's feature is a one-time paste to move your preferences from one walled garden to another. Memory Crystal is a persistent, sovereign memory layer that works across all your AIs simultaneously and stays on your hardware.

Anthropic asks: "Want to bring your memories to us?"
Memory Crystal asks: "Want all your AIs to share one memory that belongs to you?"

---

## Strategic Implications

1. **Validation.** Anthropic recognizes that memory portability matters. They're solving it with copy-paste. We're solving it with infrastructure. Different levels, same problem.

2. **Positioning opportunity.** "Don't move your memories from one company to another. Own them." This is the pitch.

3. **Integration opportunity.** Memory Crystal could offer an "export for Claude import" tool. One command that formats your Crystal memories as a text block compatible with Anthropic's import flow. Meet people where they are, then show them what sovereign memory looks like.

4. **Total Recall is the real differentiator.** Anthropic imports what the AI "remembers." Total Recall imports what actually happened. Full conversation history, not a summary. Dream Weaver then consolidates it into meaning. That's a category difference.

5. **They validated agent-first memory is a real market.** Every major AI company is now building memory features. The question is who owns the data. That's our lane.

---

## Action Items

- [ ] Reference this in Memory Crystal marketing/positioning
- [ ] Consider building a "crystal export --for-claude" command for users who also use Claude directly
- [ ] Track how Anthropic evolves this (will they add API-based import? Continuous sync?)
- [ ] Total Recall launch becomes more urgent. This is the moment to show the difference.
