## Description:

Helps product managers turn early, ambiguous product ideas into review-ready PRD drafts by using Socratic, first-principles, and Occam-style questioning, with optional stages for agent scenario design, interaction design, learning loops, and phased planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mistyhuqwq-art](https://clawhub.ai/user/mistyhuqwq-art)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and product teams use this skill to sharpen unclear project requests, decide required PRD sections, drive multi-role review, and produce review-ready PRD v3.x artifacts; optional stages support agent product scenario, interaction, learning-loop, and phased planning work.

### Deployment Geography for Use:

China and international markets

## Known Risks and Mitigations:

Risk: Default Feishu document output may move confidential product requirements into an external document system.

Mitigation: Use local-only Markdown output for confidential projects or require explicit approval before creating Feishu documents.

Risk: Local PRD and log persistence may retain sensitive project context after the session.

Mitigation: Choose scoped output paths, review generated files, and remove local PRD or log files that should not persist.

Risk: Web research for competitor material can expose project intent or mix unverified public information into requirements.

Mitigation: Approve each web research step, provide allowed competitor sources, and review imported material before it enters the PRD.

Risk: Repository inspection for inherited product logic can copy more code or implementation detail than needed into requirements artifacts.

Mitigation: Provide narrow repository paths and review extracted summaries before they are included in PRDs or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mistyhuqwq-art/skills/requirement-sharpening-stone)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration, Text]

**Output Format:** [Markdown, structured prose, tables, Mermaid diagrams, and document-ready PRD content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes Feishu document output and falls back to local Markdown when document creation is unavailable.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
