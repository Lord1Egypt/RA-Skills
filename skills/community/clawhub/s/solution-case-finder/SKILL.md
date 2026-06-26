---
name: solution-case-finder
description: Help automotive, small-appliance, semiconductor, and mechanical-manufacturing R&D teams solve engineering bottlenecks by finding reference cases for similar technical problems. Compare how others handled tradeoffs, solution patterns, and patent-derived innovation cases.
version: 1.0.3
trigger: "solution case finder|reference case|similar engineering problem|technical tradeoff|how others solved|how did others solve|patent case|patent cases|R&D problem|engineering problem|engineering solution|similar solution|solution pattern|solution case|innovation case|cross-industry solution|technical problem|TRIZ|technical contradiction|inventive principle|scientific effect"
tools:
  - mcp
  - http
metadata:
  openclaw:
    primaryEnv: TRIZ_SOLUTION_SEARCH_MCP_ENDPOINT
    envVars:
      - name: TRIZ_SOLUTION_SEARCH_MCP_ENDPOINT
        required: false
        description: MCP gateway endpoint for triz-solution-search. Default: https://ai-fabric.patsnap.com/mcp/triz-solution-search?APP_ID=Patsnap.
      - name: TRIZ_SOLUTION_SEARCH_APP_ID
        required: false
        description: Optional APP_ID query value when the gateway endpoint is provided without query parameters.
      - name: SOLUTION_CASE_FINDER_LEAD_URL
        required: false
        description: Optional landing page or trial request URL shown only when the user asks for full exports, enterprise access, or follow-up.
---

# Solution Case Finder

## Public Positioning

Lead with the user's concrete problem: they are blocked by an engineering bottleneck and want practical reference cases before choosing a design direction.

Public listing copy should put the value first:

"Help automotive, small-appliance, semiconductor, and mechanical-manufacturing R&D teams solve engineering bottlenecks by finding reference cases for similar technical problems. Compare how others handled tradeoffs, solution patterns, and patent-derived innovation cases."

Do not position the skill as a TRIZ teaching tool. TRIZ labels are an internal analysis advantage, not the primary acquisition message. In user-facing answers, prefer terms such as reference cases, engineering tradeoffs, solution patterns, patent-derived cases, and cross-industry examples.

## Language Policy

This ClawHub skill is designed for English input and English output.

Always answer in English. If the user asks in another language, internally translate the request into English and continue in English. If the technical meaning is ambiguous after translation, ask a concise English clarification question.

Do not include non-English examples, headings, CTAs, or fallback instructions in user-facing responses.

If MCP case fields contain non-English source text, translate or summarize those fields into English before showing them to the user. Do not expose mixed-language raw source fragments in the default answer.

## When to Use

Use this skill when a researcher, engineer, product developer, patent analyst, or innovation lead directly enters a technical problem and asks for reference cases showing how similar problems have been solved before. The skill is mainly intended for R&D users in four industry domains: automotive, small appliances, semiconductors, and mechanical manufacturing.

The user can call the skill and input their own problem directly; do not require them to use a fixed prompt template.

The underlying case library is exposed through the MCP source `triz-solution-search` and contains structured patent-derived solution cases.

## Input Examples

Users can enter their own technical problem directly. They may use a plain question or a structured technical-contradiction statement.

Plain question examples:

- How can an EV battery pack reduce thermal runaway propagation between cells and modules without adding too much weight or cooling complexity?
- How can a semiconductor package improve heat dissipation while controlling warpage and keeping the package thin?

Technical-contradiction input example:

```text
If a conventional indoor fan is mounted inside the enclosure, then the structure is simple and easy to manufacture, but the conditioned air cannot be discharged over a long distance.
```

Typical user intents:

- Find historical solution cases for a technical tradeoff.
- Map a practical engineering problem to reusable solution patterns.
- Compare how different industries solved similar constraints.
- Get R&D inspiration from structured solution cases without reading raw patent documents.

This skill provides R&D inspiration and structured case retrieval. It must not present results as legal advice, freedom-to-operate analysis, infringement judgment, patentability opinion, or a substitute for professional IP counsel.

## Required Capability

Use the configured MCP server named `triz-solution-search`.

Default endpoint:

`https://ai-fabric.patsnap.com/mcp/triz-solution-search?APP_ID=Patsnap`

The source exposes one MCP tool:

- Tool name: `solution_search`
- Required argument: `user_question`
- Optional argument: `limit` with default `20` and maximum `100`
- Input shape: `{ "user_question": "<technical problem description>", "limit": 100 }`
- Return shape: JSON text containing `status`, `error_code`, `data.total`, and `data.cases[]`

Each case may include:

- `problem_summary`
- `effect_summary`
- `innovation_summary`
- `triz_technical_contradiction`
- `triz_svop`
- `triz_scientific_effects`
- `relevance_score`
- Internal traceability fields such as `case_id`, which should not be shown by default.

For connection details, read `references/mcp-integration.md`.

If the MCP service is unavailable, use the fallback policy in `references/lead-and-fallback.md`. Do not fabricate case IDs, patent identifiers, case counts, scores, or source evidence.

## Core Workflow

1. Understand the user's R&D problem.
   - Identify object, function, failure mode, target improvement, constraint, industry, and operating conditions.
   - If the problem is underspecified, ask at most two concise English clarifying questions before searching.
   - If enough information exists, proceed without delaying the user.

2. Convert the problem into a case search frame.
   - Extract the improving parameter and worsening parameter.
   - Identify the likely technical tradeoff or contradiction.
   - Identify candidate solution pattern labels.
   - Keep the search frame concise and in English.

3. Query `triz-solution-search.solution_search`.
   - Pass a compact English problem statement as `user_question`.
   - Pass `limit: 100` by default so the skill can retrieve the largest supported result set, unless the user explicitly asks for fewer cases.
   - Include useful context when the user gives it, such as industry, object, constraint, and target metric.
   - Sort returned cases by `relevance_score` in descending order before presenting them when scores are available.
   - If some scores are missing, keep unscored cases after scored cases while preserving returned order among unscored cases.
   - If all returned cases have `relevance_score` missing or null, do not fabricate scores and do not show per-case score lines. State once that MCP did not provide numeric scores, then present all returned cases in MCP order.
   - Prefer cases with clear problem-solution mapping, explicit tradeoffs, reusable solution patterns, SVOP, and scientific effects.

4. Select and synthesize results.
   - Group cases by solution pattern, not only by industry.
   - Highlight repeated inventive principles.
   - Explain why each case is relevant to the user's contradiction.
   - Extract transferable design ideas and experimental next steps.
   - Do not show internal `rank` values or `case_id` in the default user-facing answer. Use them only internally for traceability or when the user explicitly asks for source identifiers.
   - Present every case returned by the MCP service. Do not truncate to only the top cases by default.
   - If the returned case count is too large for a single response, continue in batches and clearly show total returned, cases shown in the current batch, and remaining cases.

5. Return a compact, source-grounded answer.
   - Use the structure in `references/output-format.md`.
   - Include the six important case fields when available: `problem_summary`, `effect_summary`, `innovation_summary`, `triz_technical_contradiction`, `triz_svop`, and `triz_scientific_effects`.
   - Include `relevance_score` only when the MCP provides a numeric value. Do not show `Relevance score: Not provided by MCP`.
   - Clearly label uncertainty when evidence is incomplete.
   - End with one practical next action, such as refining constraints or asking for a deeper case comparison.

## Query Rules

For detailed query expansion, ranking, and cross-industry analogy rules, read `references/triz-query-rules.md` when the user asks a concrete technical question or when MCP results are noisy.

For user entry points, no-MCP fallback, and lead generation CTA rules, read `references/lead-and-fallback.md`.

For expected answer structure, read `references/output-format.md`.

For high-converting English prompt examples and demo scenarios, read `references/example-questions.md` when preparing onboarding text, listing copy, demos, or test prompts.

## Response Style

Answer in clear, professional English. Keep the tone practical and useful for R&D teams.

Be specific:

- Say "The transferable idea is..." instead of giving generic inspiration.
- Say "The relevant tradeoff is..." before listing solution patterns.
- Say "This should be validated by..." for assumptions and experiments.

Do not overclaim:

- Do not say a solution is novel, non-infringing, or legally safe.
- Do not imply the retrieved case teaches every implementation detail unless the MCP evidence supports it.
- Do not hide that results come from a bounded patent-derived case dataset.

## Failure Handling

If no strong case is found:

1. Explain which search frame was attempted.
2. Provide the closest adjacent patterns.
3. Suggest how the user can reframe the problem with more constraints.

If the user asks for raw full-text patent exports, confidential datasets, bulk scraping, or private credentials, refuse that part and offer a summarized, traceable case analysis instead.

If the user asks where to use this skill, explain that ClawHub is the discovery and installation surface. The actual question is entered directly in the user's ClawHub-compatible Agent chat after installing this skill and configuring the `triz-solution-search` MCP endpoint.
