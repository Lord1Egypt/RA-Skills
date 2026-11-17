## Description:

新闻联播政策摘要 helps agents retrieve daily Xinwen Lianbo text and extract macroeconomic, financial-market, industrial, regional, and general policy signals into structured summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhutulang](https://clawhub.ai/user/zhutulang)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, investors, and policy-focused users can use this skill to turn a target day's 新闻联播 transcript into a concise policy brief, including financial-market-sensitive items and broader macro policy references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public transcript pages may be unavailable, incomplete, or not yet published for the requested date.

Mitigation: Prefer authoritative sources such as CCTV, Xinhua, and People's Daily, and state the latest available episode date when the requested transcript is not available.

Risk: Broad policy prompts could be routed through a specialized 新闻联播 workflow and produce irrelevant results.

Mitigation: Use explicit 新闻联播-related prompts and keep the request scoped to a target date or episode.

Risk: Fetched transcript text is written to a temporary local file before parsing.

Mitigation: Store only the fetched transcript needed for parsing and delete the temporary file after the report is generated.

Risk: Keyword-based classification can miss nuance or overstate the policy significance of a news item.

Mitigation: Treat tier labels as screening aids and review the matched item text before making financial or policy decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhutulang/skills/xwlb-policy-extract)
- [Macro policy keyword reference](artifact/references/macro_keywords.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown policy brief with optional JSON data output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Classifies transcript items into three policy-impact tiers and includes non-policy headlines for context.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
