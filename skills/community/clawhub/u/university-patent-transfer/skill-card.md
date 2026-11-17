## Description:

Finds active invention patents held by universities and research institutes, groups them by institution, and shortlists candidates for potential transfer or licensing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users with technology-transfer needs use the skill to find active university and research-institute invention patents and prepare an institution-grouped CSV shortlist for potential licensing or transfer discussions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to PatentMax, and API calls can spend account credit.

Mitigation: Use non-sensitive technical terms, explain expected costs, and set an explicit spending cap before searches.

Risk: Coding flaws could expose API keys or write files outside the intended cache.

Mitigation: Ask the publisher to restrict credential destinations and contain cache paths before installing; use a restricted key and do not share production keys through chat.

## Reference(s):

- [ClawHub release](https://clawhub.ai/ip930/skills/university-patent-transfer)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [PatentMax](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Files, Analysis, Text]

**Output Format:** [UTF-8 CSV with BOM and concise Markdown findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CSV is grouped by institution and includes the search strategy and query date; summaries and recommendations are based on patent database results, not legal conclusions.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
