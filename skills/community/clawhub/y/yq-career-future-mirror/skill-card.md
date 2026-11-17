## Description:

Yq Career Future Mirror helps users plan career transitions or development paths by collecting background details, producing three differentiated career-path reports, supporting future-self dialogue, and generating a future-letter HTML page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure career-planning conversations, compare three career paths, create HTML career reports, conduct future-self reflection, and generate a future-letter artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Career and resume-like details may be saved locally in generated conversation logs and reports.

Mitigation: Get user consent before logging, avoid storing raw sensitive text where possible, and delete output/data/conversation_log.json after use.

Risk: Generated HTML reports load unpinned third-party scripts from public CDNs.

Mitigation: Prefer self-contained or locally bundled report assets, or review the generated HTML before opening it with network access.

## Reference(s):

- [Career survey data schema](reference/career_survey_data.json)
- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/yq-career-future-mirror)
- [Tailwind CSS CDN](https://cdn.tailwindcss.com)
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js)
- [Alpine.js CDN](https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese conversational text plus generated HTML, JSON conversation logs, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local report files under output/reports and conversation data under output/data.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
