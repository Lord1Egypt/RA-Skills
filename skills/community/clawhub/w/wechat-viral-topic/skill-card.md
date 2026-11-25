## Description:

A topic-selection assistant for WeChat public accounts, short-video creators, comic authors and H5 planners that turns a raw trend into a defensible topic card. It extracts verifiable signals from source material (figures, time windows, platform fit, hashtags, conflict lines, reader pain points), screens drafts against compliance red lines (medical claims, absolute wording, income promises, incentivised sharing, unsourced assertions), and grades headlines for length, formula type and red-line risk. Ships a zero-dependency, offline, standard-library toolchain (scan / riskcheck / titlecheck) plus an 11-case golden set with a re-executable runner and a demo that proves both the block path and the no-false-positive path. Progressive disclosure: frameworks and checklists live in references/. Triggers: topic selection, viral topic, hot take, headline, WeChat article, 100k+ read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

LicenseRef-AllRightsReserved

## Use Case:

External creators and editors use the skill to turn source material or a current trend into a topic plan, headline options, and a content outline, then screen the draft for common compliance red lines. It is intended for topic planning and editorial checks, not for guaranteeing reach or replacing professional review of sensitive claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation triggers may cause the skill to run for requests outside its topic-planning scope.

Mitigation: Use it for topic selection, headline checks, or content-risk screening, and describe that task clearly in the request.

Risk: The security assessment has medium confidence and is partial; binary content and some local path references were not assessed.

Mitigation: Review the package contents and local references before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/wechat-viral-topic)
- [Risk checklist](references/risk-checklist.md)
- [Scoring card](references/scoring-card.md)
- [Content formats](references/content-formats.md)
- [Title formulas](references/title-formulas.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Editorial guidance]

**Output Format:** [Topic cards, headline options, outlines, and risk-check guidance in Markdown or text; machine-readable signal and check results in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify missing evidence or flag risky wording; does not guarantee audience reach or content compliance.]

## Skill Version(s):

2.1.5 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
