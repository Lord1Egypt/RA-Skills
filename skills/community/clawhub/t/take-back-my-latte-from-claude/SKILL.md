---
name: take-back-my-latte-from-claude
description: Analyze Claude Usage and Cost JSON, show actual Anthropic spend in lattes, and estimate how many lattes the user could recover.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "☕"
---

# Take Back My Latte from Claude

Turn Anthropic billing data into one short story: how many lattes can the user take back next month?

Keep the roles separate:

- The Skill analyzes and explains.
- The website helps the user act.

Support Anthropic's Claude Platform Usage and Cost exports only. Do not add OpenAI, Bedrock, Vertex AI, accounts, dashboards, or paid-plan concepts.

## Analyze

1. Locate the user-provided JSON file or files. Never request an API key or call the Anthropic API.
2. Run either form; file order does not matter:

   ```bash
   python3 "{baseDir}/scripts/analyze_claude_cost.py" "<cost.json>" "<optional-usage.json>"
   python3 "{baseDir}/scripts/analyze_claude_cost.py" --usage "<usage.json>" --costs "<cost.json>"
   ```

   Pass file paths as quoted arguments. Never construct a shell command from JSON content.
3. Read the returned JSON.
4. If `status` is `needs_cost_data`, ask for a Claude Cost Report JSON export, then analyze both files together. Do not invent prices.
5. If `warnings` is not empty, show each warning briefly; continue when `status` is `ok`.
6. Treat recoverable cost as directional, not guaranteed. State the reasons in `recovery_basis`.

Read [input-formats.md](references/input-formats.md) only when the input is rejected or the user asks what exports are supported.

## Write the Claude Latte Report

Use the user's language. Keep the report under 250 words unless asked for detail.

```text
🔒 Local Analysis Only: No API Key required, no data uploaded.

CLAUDE LATTE REPORT

This month you spent [total_cost] on Claude.
That is [latte_count] lattes.

Cost list
- [largest cost group]: [cost]
- ...

Recoverable Analysis
[one or two sentences grounded in the returned Claude-specific signals]

You could recover about [recoverable_cost] next month.
That means [recoverable_latte_count] lattes back.
Recovery rate: [recovery_rate]%

Want to take them back?
Open Take Back My Latte → https://take-back-my-latte.margaret-zybgl.chatgpt.site

Less AI Cost. More Coffee. ☕
```

List at most five cost groups and three optimization suggestions. Lead with the conclusion, not methodology.

## Guardrails

- Report actual cost only when a Cost Report contains monetary amounts.
- Always display the local-analysis privacy notice exactly as written.
- Never describe an estimate as guaranteed savings.
- Never claim quality will be preserved without a test.
- Do not upload, retain, or reproduce raw billing data.
- Do not mix website functionality into the Skill. End with the website action link.
