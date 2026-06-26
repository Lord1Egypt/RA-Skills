> ## Documentation Index
> Fetch the complete documentation index at: https://docs.tavily.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Best Practices for Research

> Learn how to write effective prompts, choose the right model, and configure output formats for better research results.

## Prompting

Define a **clear goal** with all **details** and **direction**.

* **Be specific when you can.** If you already know important details, include them.<br />
  (E.g. Target market or industry, key competitors, customer segments, geography, or constraints)
* **Only stay open-ended if you don't know details and want discovery.** If you're exploring broadly, make that explicit (e.g., "tell me about the most impactful AI innovations in healthcare in 2025").
* **Avoid contradictions.** Don't include conflicting information, constraints, or goals in your prompt.
* **Share what's already known.** Include prior assumptions, existing decisions, or baseline knowledge—so the research doesn't repeat what you already have.
* **Keep the prompt clean and directed.** Use a clear task statement + essential context + desired output format. Avoid messy background dumps.

### Example Queries

```text  theme={null}
"Research the company ____ and it's 2026 outlook. Provide a brief
overview of the company, its products, services, and market position."
```

```text  theme={null}
"Conduct a competitive analysis of ____ in 2026. Identify their main competitors,
compare market positioning, and analyze key differentiators."
```

```text  theme={null}
"We're evaluating Notion as a potential partner. We already know they primarily
serve SMB and mid-market teams, expanded their AI features significantly in 2025,
and most often compete with Confluence and ClickUp. Research Notion's 2026 outlook,
including market position, growth risks, and where a partnership could be most
valuable. Include citations."
```

## Model

| Model  | Best For                                                             |
| ------ | -------------------------------------------------------------------- |
| `pro`  | Comprehensive, multi-agent research for complex, multi-domain topics |
| `mini` | Targeted, efficient research for narrow or well-scoped questions     |
| `auto` | When you're unsure how complex research will be                      |

### Pro

Provides comprehensive, multi-agent research suited for complex topics that span multiple subtopics or domains. Use when you want deeper analysis, more thorough reports, or maximum accuracy.

```json  theme={null}
{
  "input": "Analyze the competitive landscape for ____ in the SMB market, including key competitors, positioning, pricing models, customer segments, recent product moves, and where ____ has defensible advantages or risks over the next 2–3 years.",
  "model": "pro"
}
```

### Mini

Optimized for targeted, efficient research. Works best for narrow or well-scoped questions where you still benefit from agentic searching and synthesis, but don't need extensive depth.

```json  theme={null}
{
  "input": "What are the top 5 competitors to ____ in the SMB market, and how do they differentiate?",
  "model": "mini"
}
```

## Structured Output vs. Report

* **Structured Output** - Best for data enrichment, pipelines, or powering UIs with specific fields.
* **Report** — Best for reading, sharing, or displaying verbatim (e.g., chat interfaces, briefs, newsletters).

### Formatting Your Schema

* **Write clear field descriptions.** In 1–3 sentences, say exactly what the field should contain and what to look for. This makes it easier for our models to interpret what you're looking for.
* **Match the structure you actually need.** Use the right types (arrays, objects, enums) instead of packing multiple values into one string (e.g., `competitors: string[]`, not `"A, B, C"`).
* **Avoid duplicate or overlapping fields.** Keep each field unique and specific - contradictions or redundancy can confuse our models.

## Streaming vs. Polling

<CardGroup cols={2}>
  <Card title="Streaming" icon="wave-pulse" href="https://github.com/tavily-ai/tavily-cookbook/blob/main/cookbooks/research/streaming.ipynb">
    Best for user interfaces where you want real-time updates.
  </Card>

  <Card title="Polling" icon="rotate" href="https://github.com/tavily-ai/tavily-cookbook/blob/main/cookbooks/research/polling.ipynb">
    Best for background processes where you check status periodically.
  </Card>
</CardGroup>

<Tip>
  See streaming in action with the [live demo](https://chat-research.tavily.com/).
</Tip>
