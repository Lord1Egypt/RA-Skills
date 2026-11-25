## Description:

Search and analyze public Xiaohongshu notes, comments, and creator activity, returning structured JSON for topic research, competitor monitoring, and audience insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and analysts can search public Xiaohongshu notes, inspect a note or its comments, and review a creator’s posts and public engagement statistics. Use the results for topic research, competitor monitoring, creator screening, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and supplied links are sent to the external Guaikei API; the security review was benign with medium confidence and did not fully interpret some executable code.

Mitigation: Send only public-data queries, avoid including sensitive information in keywords or links, and review the skill before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/xhs-topic-hunter)
- [Guaikei API service](https://www.guaikei.com)
- [Output contract](artifact/references/contract.md)
- [Setup and data handling FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON results, with concise natural-language summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public note, comment, and creator data; API responses use a common success, empty, or error envelope.]

## Skill Version(s):

1.2.3 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
