---
name: web-llm-chat
description: Chat with web-based LLMs through the Chrome Relay extension. Provides free access to powerful web search and RAG capabilities without API costs. Currently supports Qwen AI (chat.qwen.ai). Use for web search, deep research, multi-turn investigations, getting a second opinion, comparing AI responses, or delegating complex reasoning tasks. Requires Chrome extension relay connected with an LLM chat tab open. Triggers on phrases like "ask Qwen", "search with Qwen", "Qwen search", "deep research with Qwen", "Qwen research", "web LLM search", "browser AI chat", "free AI search", "Qwen怎么说", "去问Qwen", "Qwen 搜索", "Qwen 研究", "用 Qwen 深度研究".
---

# Web LLM Chat Skill

Interact with web-based LLMs through the Chrome Relay extension. This skill enables automated conversations with AI models, supporting both simple queries and multi-turn research workflows.

**Currently supported:** Qwen AI (chat.qwen.ai) — more models coming soon.

## Why This Skill?

### The Problem

- **Web search APIs are expensive**: Services like Brave Search API and Tavily require API keys and paid subscriptions, creating ongoing costs.
- **Limited research capabilities**: Traditional search APIs return raw results, lacking the reasoning and synthesis capabilities of modern LLMs.
- **Quality vs. cost tradeoff**: Getting high-quality, well-reasoned research often requires expensive API calls or manual effort.

### The Opportunity

Modern web-based LLMs (like Qwen) offer:

- **Powerful built-in search**: Native web search with real-time information retrieval
- **RAG capabilities**: Automatic retrieval-augmented generation for grounded responses
- **Deep research features**: Multi-source synthesis and citation
- **Commercial-grade quality**: As products backed by major companies, they're continuously improved

### The Solution

This skill leverages OpenClaw's Chrome Relay to:

- **Access web LLMs for free**: Use the web interface without API costs
- **Automate research workflows**: Let agents conduct multi-turn investigations
- **Get higher quality results**: Benefit from commercial LLM capabilities at lower cost
- **Enable comparison**: Cross-reference with other AI responses

**Bottom line**: Use OpenClaw to orchestrate powerful web-based LLMs at a fraction of the API cost, with better research quality than raw search APIs.

## Features

- **Send messages** to web-based LLMs and receive responses
- **Multiple output formats**: plain text, Markdown (preserves code blocks, tables, lists), or raw HTML
- **Send-ready detection**: waits until the page is ready for the next question
- **Smart extraction**: uses anchor-based extraction to get only the latest response
- **Research mode**: agent-orchestrated multi-turn conversations

## Supported Models

| Model | Status | Notes |
|-------|--------|-------|
| Qwen AI (chat.qwen.ai) | ✅ Supported | Full support for search, RAG, and multi-turn conversations |
| More models | 🚧 Coming soon | Open an issue to request support for other web-based LLMs |

## Prerequisites

- Chrome Relay extension attached to a Qwen Chat tab (`chat.qwen.ai/*`)
- Gateway running on `127.0.0.1:18789` (default)
- Node.js with `ws` package installed

## Installation

Install the `ws` package using your preferred package manager:

```bash
# npm
npm install ws

# yarn
yarn add ws

# pnpm
pnpm add ws
```

## Quick Start

### Check Connection Status

```bash
node scripts/qwen_chat.js status
```

### Send a Message

```bash
# Plain text (default)
node scripts/qwen_chat.js send "What is machine learning?"

# With custom wait time (for long responses)
node scripts/qwen_chat.js send "Explain RAG in detail" --wait 120

# Get response in Markdown format (preserves formatting)
node scripts/qwen_chat.js send "Write a Python function" --format markdown

# Get raw HTML
node scripts/qwen_chat.js send "Create a table" --format html
```

### Read Current Page Content

```bash
node scripts/qwen_chat.js read
```

## Command Reference

### `status`

Check if Chrome Relay is connected and Qwen tab is active.

```bash
node scripts/qwen_chat.js status
```

Output:
```
Extension: ✅ Connected
Qwen tab: ✅ Qwen Chat
  URL: https://chat.qwen.ai/c/...
```

### `send`

Send a message to Qwen and receive the response.

```bash
node scripts/qwen_chat.js send "your message" [options]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--wait N` | Maximum wait time in seconds | 45 |
| `--format text\|markdown\|html` | Output format | text |
| `--debug-extract` | Show extraction debugging info | off |

**Output Formats:**

- `text` — Plain text output
- `markdown` — Preserves code blocks, tables, lists, headers, and formatting
- `html` — Raw HTML from the page

### `read`

Read the current page content (useful for debugging or reviewing conversation history).

```bash
node scripts/qwen_chat.js read
```

### `research`

Run multi-round research on a topic (fixed stages, consider using agent-orchestrated mode instead).

```bash
node scripts/qwen_chat.js research "AI safety" --rounds 10 --wait 120
```

## How It Works

### Response Extraction

The script uses a robust extraction strategy:

1. **Send-ready detection**: Waits until the page is ready for the next question (input field editable, send button enabled)
2. **Anchor-based extraction**: Uses the user's message as an anchor to find and extract only the latest response
3. **Content stabilization**: Waits for content to stabilize before extraction

### Why Not Use Thinking Indicators?

- Thinking indicators can get stuck visually while the response is complete
- Send-ready detection is more reliable: if you can send the next question, the previous response is done
- Works regardless of UI changes to thinking indicators

### Why Not Use Delta by Body Length?

- Qwen page may reflow and change `bodyLen` unpredictably
- Anchor-based extraction is more robust to page reflows
- Only extracts the actual response content, not noise

## Research Mode (Agent-Orchestrated)

For multi-turn research, use agent-orchestrated mode instead of the fixed `research` command. This allows the agent to dynamically control the conversation based on Qwen's responses.

### Workflow

```
1. Determine research topic
2. Ask first question (open-ended, let Qwen expand)
3. Read Qwen's response
4. Analyze the response:
   - Which point deserves deeper exploration?
   - Which claim needs cross-validation?
   - Any contradictions or gaps?
5. Ask follow-up question based on analysis
6. Repeat steps 3-5 for 5-10 rounds
7. Final round: Ask Qwen to summarize, agent also compiles its own summary
```

### Example Per-Round Operation

```bash
# Agent sends question and waits for response
node scripts/qwen_chat.js send "What are the key challenges in RLHF?" --wait 120

# Agent can read full page if needed
node scripts/qwen_chat.js read
```

### Follow-up Strategy

Good follow-ups come from Qwen's response:

| Response Pattern | Follow-up Direction |
|-----------------|---------------------|
| Mentions data/statistics | "What's the original source? Sample size?" |
| Gives opinion without evidence | "Any research supporting this claim?" |
| Mentions controversy | "What are the counter-arguments?" |
| Uses "possibly/maybe" | "Under what conditions does this hold?" |
| Lists multiple factors | "Which one is most critical? Why?" |
| Mentions case study | "Has this case been challenged by other researchers?" |
| Goes off-topic | "Back to the core question, specifically..." |

### Best Practices

- **Don't pre-plan all questions**: Generate questions dynamically based on responses
- **Allow tangents**: If Qwen mentions something unexpected but interesting, pursue it
- **Challenge occasionally**: Don't always agree with Qwen; present counter-arguments
- **Maintain continuity**: Briefly reference previous points when asking follow-ups
- **Control rounds**: 5-10 rounds is optimal; too few lacks depth, too many has diminishing returns
- **Handle timeouts honestly**: If the script times out, report it to the user rather than making up content
- **Adjust wait time**: Use `--wait 180` for search-heavy questions, `--wait 60` for simple ones

## Debugging

### Enable Extraction Debugging

```bash
node scripts/qwen_chat.js send "test message" --wait 90 --debug-extract
```

This shows:
- Baseline and latest body length
- Number of leaf elements detected
- Extraction path used
- Raw and final content lengths

### Common Issues

| Issue | Solution |
|-------|----------|
| Extension disconnected | Check Chrome extension badge shows `ON` |
| No Qwen tab found | Open `chat.qwen.ai` and attach extension |
| Response not captured | Increase `--wait` time, use `--debug-extract` to diagnose |
| Markdown formatting broken | Code blocks use Monaco Editor; extraction handles this automatically |

## Configuration

### Auth Token

The script auto-derives the relay token from the OpenClaw config. Config priority:

1. `E:\.openclaw\.openclaw\openclaw.json` (Windows)
2. `~/.openclaw/.openclaw/openclaw.json` (Unix)

### Gateway Ports

- Gateway: `18789`
- Relay: `18792` (Gateway + 3)

## Limitations

- Requires Qwen to be logged in the browser
- One tab at a time (controls the first attached Qwen tab)
- No streaming — waits for full response before returning
- `research` command uses fixed stages — use agent-orchestrated mode instead

## File Structure

```
qwen-chat/
├── SKILL.md                    # This file
├── scripts/
│   ├── qwen_chat.js           # Main script
│   ├── _diagnose_selectors.js # Diagnostic tools
│   └── _analyze_format.js     # Format analysis
└── references/
    └── chrome-relay.md        # Chrome Relay setup guide
```

## See Also

- [Chrome Relay Setup](references/chrome-relay.md) — detailed relay configuration

## License

See [LICENSE](LICENSE) file for details.