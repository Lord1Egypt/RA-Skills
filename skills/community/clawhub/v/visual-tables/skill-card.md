## Description:

Visual Tables helps agents turn multi-option comparisons into escaped HTML tables where color tiers, bars, chips, and numeric formatting make tradeoffs readable at a glance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to present several options with several attributes each, such as search results, product comparisons, model benchmarks, server health, candidates, or quotes. It is intended for chat surfaces that render HTML, with plain text fallback needed elsewhere.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and write local paths when directed by the user.

Mitigation: Use it only with intended input data and output locations, and review generated files before sharing them.

Risk: HTML table output may render as raw tags on channels that do not support the expected HTML-render fence.

Mitigation: Confirm the target chat surface renders sandboxed HTML, or provide a plain-text comparison instead.

Risk: A visually polished table can still emphasize the wrong attributes if the column choices do not match the decision.

Mitigation: Define the decision and relevant columns before rendering, and visually inspect the final table for legibility and misleading omissions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/globalcaos/skills/visual-tables)
- [Designing a table someone can read at a glance](artifact/references/designing-a-table.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, guidance]

**Output Format:** [Markdown with fenced html-render blocks containing escaped HTML fragments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node for the bundled renderer and tests; generated HTML references no external resources.]

## Skill Version(s):

1.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
