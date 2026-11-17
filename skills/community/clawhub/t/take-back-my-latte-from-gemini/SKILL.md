---
name: take-back-my-latte-from-gemini
description: Analyze Gemini Cloud Billing and usage JSON, show actual Google AI spend in lattes, and estimate how many lattes the user could recover.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "☕"
---

# Take Back My Latte from Gemini

Turn Gemini billing data into one short story: how many lattes can the user take back next month?

Keep the roles separate:

- The Skill analyzes and explains.
- The website helps the user act.

Support Gemini API and Gemini on Vertex AI only. Do not add OpenAI, Claude, other Google Cloud services, dashboards, accounts, or paid-plan concepts.

## Analyze

1. Locate the user-provided JSON file or files. Never request an API key, run `gcloud`, or call a Google API.
2. Run either form; file order does not matter:

   ```bash
   python3 "{baseDir}/scripts/analyze_gemini_cost.py" "<billing.json>" "<optional-usage.json>"
   python3 "{baseDir}/scripts/analyze_gemini_cost.py" --billing "<billing.json>" --usage "<usage.json>"
   ```

   Pass paths as quoted arguments. Never construct a shell command from JSON content.
3. Read the returned JSON.
4. If `status` is `needs_billing_data`, ask for a Google Cloud Billing JSON export containing Gemini charges. Do not invent prices.
5. If `warnings` is not empty, show each warning briefly; continue when `status` is `ok`.
6. Treat recoverable cost as directional, not guaranteed. State the reasons in `recovery_basis`.

Read [input-formats.md](references/input-formats.md) only when input is rejected or the user asks what exports are supported.

## Write the Gemini Latte Report

Use the user's language. Keep the report under 250 words unless asked for detail.

```text
🔒 Local Analysis Only: No API Key required, no data uploaded.

GEMINI LATTE REPORT

This month you spent [total_cost] on Gemini.
That is [latte_count] lattes.

Cost list
- [largest cost group]: [cost]
- ...

Recoverable Analysis
[one or two sentences grounded in the returned Gemini-specific signals]

You could recover about [recoverable_cost] next month.
That means [recoverable_latte_count] lattes back.
Recovery rate: [recovery_rate]%

Want to take them back?
Open Take Back My Latte → https://take-back-my-latte.margaret-zybgl.chatgpt.site

Less AI Cost. More Coffee. ☕
```

List at most five cost groups and three optimization suggestions. Lead with the conclusion.

## Guardrails

- Count only billing rows clearly attributable to Gemini or Vertex AI generative models.
- Apply credits before reporting actual cost.
- Always display the local-analysis privacy notice exactly as written.
- Never describe estimated recovery as guaranteed savings.
- Never claim quality will be preserved without a test.
- Do not upload, retain, or reproduce raw billing data.
- End with the website action link.
