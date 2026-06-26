# Report Anti-Patterns

Load this file before `--generate`. It is the report-specific anti-pattern layer on top of `references/design-quality.md` and `references/review-checklist.md`.

These rules are intentionally blunt. If a draft triggers one of these patterns, rewrite it before writing HTML.

## Contract Shape

Each anti-pattern entry should answer the same four questions.

## Symptom

What the bad output usually looks like in IR, prose, or HTML.

## Why It Hurts

Why the pattern makes async reading slower, noisier, or less trustworthy.

## Preferred Replacement

Which component or prose pattern should replace the bad pattern.

## Rewrite Rule

One direct instruction that the generator or reviewer can apply without debate.

## `fake-kpi`

- Symptom: KPI cards are filled with placeholders, status words, long explanatory sentences, or qualitative claims that are not actually metrics.
- Why It Hurts: It creates a fake visual anchor and tells the reader that the report has hard numbers when it does not.
- Preferred Replacement: `callout`, prose, or `table`.
- Rewrite Rule: If the source does not provide a short real numeric metric, do not emit `:::kpi`; downgrade to `callout`, `timeline`, or `table`.

## `decorative-chart`

- Symptom: A chart appears mainly to decorate a section, restate obvious text, or visualize placeholder-only values.
- Why It Hurts: It adds scanning cost without increasing understanding and can imply false analytical rigor.
- Preferred Replacement: prose, `table`, or a short `callout`.
- Rewrite Rule: If the reader learns nothing new from the chart shape, remove the chart and state the takeaway directly.

## `pseudo-timeline`

- Symptom: A timeline is used for parallel principles, capability buckets, or unordered stages that are not truly chronological.
- Why It Hurts: The component communicates sequence and causality that the content does not actually have.
- Preferred Replacement: `list`, prose, or `callout`.
- Rewrite Rule: If items can be reordered without changing meaning, do not use `:::timeline`.

## `template-heading`

- Symptom: Section headings read like empty labels such as "Overview", "Summary", "核心能力", or "Next Steps".
- Why It Hurts: Headings stop carrying argument structure, so the document becomes harder to skim and harder to remember.
- Preferred Replacement: information-bearing headings that state a claim, implication, or contrast.
- Rewrite Rule: Rewrite noun-label headings into content-specific statements before render.

## `badge-quota-thinking`

- Symptom: Badges are inserted just to hit a count or to make the page feel "busy enough".
- Why It Hurts: Optional scan anchors turn into noise, and the reader can no longer tell which chips actually matter.
- Preferred Replacement: no badge at all, or one status/category/entity badge only where it clarifies the content.
- Rewrite Rule: Add a badge only when it disambiguates status, category, or entity identity; never fill a quota.

## `color-flood`

- Symptom: Accent colors spread across headings, KPI values, badges, charts, dividers, and callouts at the same time.
- Why It Hurts: The page loses hierarchy because everything is trying to be the focal point.
- Preferred Replacement: neutral text with one restrained structural accent.
- Rewrite Rule: Keep the main reading surface neutral and reserve accent color for one clear job at a time.

## `summary-without-judgment`

- Symptom: The opening summary repeats background or facts but never states what matters or why the reader should care.
- Why It Hurts: Async readers do not know the report's conclusion, decision frame, or next action within the first screen.
- Preferred Replacement: BLUF-style opening prose.
- Rewrite Rule: Open with purpose plus judgment, not background plus scene-setting.

## `action-without-decision-context`

- Symptom: The report ends with recommendations or next steps that are detached from any stated decision, tradeoff, or threshold.
- Why It Hurts: The actions feel generic because the reader cannot tell what decision they are supposed to support.
- Preferred Replacement: action block tied to a named decision, condition, or trigger.
- Rewrite Rule: Every action section must state what decision it supports, what signal triggers it, or what risk it addresses.
