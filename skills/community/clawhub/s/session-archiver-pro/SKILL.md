---
name: "session-archiver-pro"
description: "Extract decisions, todos, knowledge, preferences, and risks from AI chat sessions into structured memory. Outputs Markdown, JSON, or Obsidian notes."
---

# Session Archiver Pro

Extract structured memory from AI chat sessions. Transform raw conversation logs into organized knowledge: **decisions**, **todos**, **knowledge points**, **user preferences**, and **risks**.

## Why Session Archiver Pro?

- **Persist what matters**: No more scrolling through endless chat logs to find that one decision.
- **Cross-session awareness**: Link related information across different conversations.
- **Knowledge management ready**: Export to Markdown, JSON, or Obsidian — plug into your note-taking workflow.
- **Agent memory injection**: Outputs are formatted for direct injection into long-term agent memory.

## Workflow (9 Steps)

```
Input: One or more session logs (plain text / .log / .json / clipboard)
↓
[1] Parse dialogue structure: user messages, assistant replies, tool calls, decision points
[2] Segment by conversation arc: problem definition → exploration → decision → action
[3] Extract 5 structured categories:
    📌 Key Decisions — explicit choices/conclusions
    ✅ Action Items — who needs to do what by when
    📚 Knowledge Points — reusable facts or insights
    ⭐ User Preferences — expressed likes/dislikes, style, standards
    ⚠️ Risks & Issues — potential problems identified
[4] Deduplicate & merge: consolidate identical or related items across sessions
[5] Generate topic tags: auto-classify each session with hierarchical tags
[6] Build cross-session graph: link related items ("this decision relates to last week's todo")
[7] Export in chosen format: Markdown report / JSON / Obsidian-compatible notes
[8] Optional: format for agent long-term memory injection
[9] Produce executive summary: 5-sentence overview for quick recall
↓
Output: Structured memory report + tag index + cross-session links + summary
```

## When to Use

- After a long planning session with an AI assistant
- Before starting a new conversation on a related topic
- During weekly review of AI-assisted work
- When onboarding a new team member to an existing project
- Before an AI agent's context window resets

## Sample Prompts

### Sample 1: Daily session summary
> "Summarize today's 3 chat sessions about the SaaS pricing model. Extract decisions, action items, and open questions."

### Sample 2: Cross-session knowledge mining
> "I have 12 sessions from the past week on our product launch. Find all decision points and create a timeline."

### Sample 3: Preference extraction
> "From all my conversations with the code assistant, extract my coding style preferences (linting, testing, naming conventions)."

### Sample 4: Risk identification
> "Scan these 5 design review sessions and flag any risk signals or tensions I should revisit before finalizing."

### Sample 5: Agent memory prep
> "Archive this session about database migration planning. Output in agent-memory-injection format for my AI assistant's long-term memory."

## First-Success Path

```
1. Run: python3 scripts/archiver.py --file sample_session.log
2. Review the structured output in stdout (Markdown by default)
3. Use --format json for programmatic consumption
4. Use --format obsidian for note-taking integration
5. Use --dir ./sessions/ for batch processing multiple sessions
```

## Output Examples

### Markdown Report (Decision-Centric)

```markdown
# Session Memory Report — SaaS Pricing (3 sessions)

## 📌 Key Decisions (4)
| # | Decision | Session | Impact |
|---|----------|---------|--------|
| 1 | Usage-based pricing model | Session-1 | Revenue model shift |
| 2 | Target audience: SMB (10-50 seats) | Session-1 | Product positioning |
| 3 | Free tier limit: 1K MAU | Session-2 | User acquisition funnel |
| 4 | No annual-only billing | Session-3 | Cash flow consideration |

## ✅ Action Items (6)
- [ ] Validate competitive pricing (John, by Fri)
- [ ] Conduct 5 customer interviews (Team, next week)
- [ ] Design pricing page mockup (Design, Mon)

## 📚 Knowledge Points (8)
- Industry conversion rate: 3-5% free→paid
- AWS pricing uses consumption + reservation hybrid
- Competitors all offer annual discount (15-20%)

## ⭐ User Preferences (3)
- Prefers clean, simple pricing (no feature tiers overload)
- Dislikes hidden fees or "starting at" bait-and-switch
- Wants transparent cost calculation upfront

## ⚠️ Risks (2)
- Free tier compute costs may exceed budget at scale
- Minimum commit could scare SMB segment
```

### JSON Output Snippet
```json
{
  "sessions": ["session-1", "session-2", "session-3"],
  "decisions": [{"text": "Usage-based pricing model","session": "session-1","tags": ["pricing","revenue-model"]}],
  "knowledge_points": [{"text": "Industry conversion rate: 3-5% free→paid","source": "session-2"}]
}
```

## CLI Usage

```
python3 scripts/archiver.py --help
  --file PATH         Single session log file
  --dir PATH          Directory of session logs
  --format FORMAT     Output format: markdown (default), json, obsidian, memory-inject
  --tags              Enable auto-tagging (default: on)
  --graph             Enable cross-session linking (default: on)
```

## Tags

`session-archiver-pro`, `memory`, `session`, `archive`, `extract`, `knowledge-management`, `obsidian`, `chat-summary`
