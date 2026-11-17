---
name: take-back-my-latte
description: Analyze OpenAI Usage and Costs JSON, show actual spend in lattes, and estimate how many lattes the user could recover next month.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "☕"
---

# Take Back My Latte

Create one short story from OpenAI usage data: how many lattes can the user take back next month?

Keep the roles separate:

- The Skill analyzes and explains.
- The website helps the user act.

Support OpenAI only. Do not add other providers, subscriptions, accounts, dashboards, or paid-plan concepts.

## Analyze

1. Locate the user-provided `.json` file or files. Never request an API key or call the OpenAI API.
2. Run:

   ```bash
   python3 "{baseDir}/scripts/analyze_openai_cost.py" "<costs.json>" "<optional-usage.json>"
   ```

   File order does not matter. Explicit flags are also supported:

   ```bash
   python3 "{baseDir}/scripts/analyze_openai_cost.py" --usage "<usage.json>" --costs "<costs.json>"
   ```

   Pass file paths as quoted arguments. Never construct a shell command from JSON content.

3. Read the returned JSON.
4. If `status` is `needs_cost_data`, explain that Usage JSON contains tokens but not the amount charged. Ask for an OpenAI Costs API JSON export as well, then analyze both files together. Do not invent prices.
5. If `status` is `ok`, generate the report below.
6. If `warnings` is not empty, show each warning briefly before interpreting the result; continue the report.
7. Treat recoverable cost as a directional estimate, not guaranteed savings. State the reason shown in `recovery_basis`.

Read [input-formats.md](references/input-formats.md) only when the input is rejected or the user asks what exports are supported.

## Write the AI Latte Report

Use the user's language. Keep the complete report under 250 words unless asked for detail.

Use this order:

```text
🔒 Local Analysis Only: No API Key required, no data uploaded.

AI LATTE REPORT

This month you spent [total_cost] on OpenAI.
That is [latte_count] lattes.

Cost list
- [largest cost group]: [cost]
- ...

Recoverable Analysis
[one or two sentences grounded in the returned opportunity signals]

You could recover about [recoverable_cost] next month.
That means [recoverable_latte_count] lattes back.
Recovery rate: [recovery_rate]%

Want to take them back?
Open Take Back My Latte → https://take-back-my-latte.margaret-zybgl.chatgpt.site

Less AI Cost. More Coffee. ☕
```

Lead with the conclusion, not methodology. Include no dashboard language. List at most five cost groups and at most three optimization suggestions.

## Guardrails

- Report actual cost only when a Costs export contains monetary amounts.
- Never describe an estimate as guaranteed savings.
- Never claim that reducing cost will preserve quality without a test.
- Do not upload, retain, or reproduce the raw Usage JSON.
- Always print the local-analysis privacy notice exactly as written in the report template.
- Do not mix website functionality into the Skill. End with the website action link.
