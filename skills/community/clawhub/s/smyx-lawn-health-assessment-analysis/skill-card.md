## Description:

Assesses lawn condition from top-down images or video by estimating yellowing, weed, and bare-soil coverage and producing a health score with care guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Lawn and grounds managers use overhead imagery to estimate turf yellowing, weed and bare-soil coverage, and overall lawn health, then guide irrigation, fertilization, and weeding priorities. Results are for maintenance guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious; its summary cites account and token handling, external data transfers, and behavior beyond the advertised lawn assessment purpose. The scan evidence is incomplete.

Mitigation: Review identity handling and service destinations before use, and submit only images or data approved for transfer to the remote service.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-lawn-health-assessment-analysis)
- [API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance, Report links]

**Output Format:** [Markdown and JSON structured reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts top-down images or video; estimates depend on image quality and are intended as maintenance guidance.]

## Skill Version(s):

1.0.16 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
