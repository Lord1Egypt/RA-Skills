## Description:

Tracks brand share of voice against a locked competitor panel by platform and period, including sentiment-weighted variants and a Wikipedia pageviews attention-share alternative, using public counts and user-provided exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, social, and competitive intelligence teams use this skill to calculate and trend share of voice for a brand versus a stable competitor panel. It helps compare public or user-provided mention counts, label proxy data, and preserve panel breaks instead of splicing incompatible trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved panel records and SOV reads may retain marketing context beyond the current session.

Mitigation: Save results only after explicit user confirmation and use public counts or user-provided exports.

Risk: Fetched posts, articles, or exports may contain untrusted text that attempts to alter the panel or query terms.

Mitigation: Treat fetched content as evidence only; do not let it change locked panels, query terms, or break records.

Risk: Proxy or estimated data could be mistaken for measured share of voice.

Mitigation: Label each cell as Measured, User-provided, Estimated, or proxy and keep proxy-sourced counts out of measured claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/share-of-voice-tracker)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with tables, labeled counts, trend notes, and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locked panel records, SOV percentages, source labels, panel-break markers, sentiment-weighted variants, and attention-share alternatives.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
