## Description:

Analyzes video of older adults living alone for behaviors such as prolonged stillness, sighing, and self-talk, then reports behavior summaries and an estimated emotional risk level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Families and community care workers can review video-based behavior summaries to decide when to offer supportive contact. The results are behavioral risk indicators, not a clinical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handling of sensitive home video, identity, and credentials is not clearly disclosed in the security summary.

Mitigation: Review handling before use, obtain the older adult's informed consent, and apply the documented video protection measures such as encryption and face masking.

Risk: The security review reports behavior that may not match the stated purpose, and scanner coverage is incomplete.

Mitigation: Treat this as review-needed, inspect the skill's behavior before installation, and do not assume the available scan assessed every behavior.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-loneliness-depression-analysis)
- [API interface and input guidance](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured behavior summaries and risk indicators; Markdown report listings and supportive follow-up suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include behavior counts and durations, baseline comparisons, risk level, suggested follow-up, and report links; it does not provide a clinical diagnosis.]

## Skill Version(s):

1.0.15 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
