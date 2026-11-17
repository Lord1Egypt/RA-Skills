## Description:

Run bounded synthetic audience research for draft posts and X-style feed experiments to compare content drafts, persona reactions, conversation quality, link friction, safety/spam risk, and feed-loop hypotheses without claiming live reach or ranking prediction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content research teams use this skill to compare draft posts against deterministic synthetic personas and produce bounded reports with objections, rewrite guidance, warnings, and a clear boundary statement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown and CSV files can contain user-supplied draft or persona text.

Mitigation: Treat generated reports as untrusted analysis, use a dedicated output directory, and avoid opening CSVs from untrusted inputs in formula-capable spreadsheets.

Risk: Synthetic persona scores can be mistaken for live reach, ranking, virality, or account-status predictions.

Mitigation: Keep the boundary statement with user-facing results and validate hypotheses through real posting experiments or user research.

## Reference(s):

- [Research Boundaries](references/research-boundaries.md)
- [Source Homepage](https://github.com/zack-dev-cm/open-feed-recsys-lab)
- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/tinytroupe-feed-research-lab)

## Skill Output:

**Output Type(s):** [text, markdown, json, csv, svg, guidance]

**Output Format:** [Markdown reports, JSON audit data, CSV persona reactions, SVG share card, and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local outputs depend on supplied drafts, audience, and optional persona files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
