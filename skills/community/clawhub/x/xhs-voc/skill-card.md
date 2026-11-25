## Description:

Retrieves public Xiaohongshu notes, comments, and creator data and returns structured JSON without logging in or making changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, brand teams, and analysts use the skill to research public Xiaohongshu content for topic selection, competitor monitoring, creator screening, and comment sentiment. It supports personal or internal team analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied links are sent to the third-party GuaiKei service.

Mitigation: Avoid sensitive query terms or links and review the service's data-handling terms before use.

Risk: The security review has partial coverage, and the token's environment scope remains unresolved.

Mitigation: Review the executable package and provide the token only in the runtime environment needed for approved queries.

## Reference(s):

- [XHS VOC on ClawHub](https://clawhub.ai/guaikei/skills/xhs-voc)
- [Publisher profile](https://clawhub.ai/user/guaikei)
- [GuaiKei API information](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON containing public Xiaohongshu search results, note details, comments, and creator data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; requires a GuaiKei API token.]

## Skill Version(s):

1.2.3 (source: ClawHub release evidence, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
