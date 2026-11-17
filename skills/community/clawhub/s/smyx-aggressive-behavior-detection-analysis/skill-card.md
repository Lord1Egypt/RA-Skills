## Description:

Detects aggressive interactions in livestock and poultry from continuous barn videos — including fighting, biting, chasing and butting — and outputs behavior type, intensity level and alert level. | 识别打斗、撕咬等攻击行为，及时预警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock and poultry farm operators use the skill to review barn images or video for fighting, biting, chasing, and butting, and receive behavior summaries with intensity and alert levels. It can also retrieve historical analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security review flags account and token handling, identity transmission, and remote transmission for review.

Mitigation: Before using real footage, review the reported identity and token handling and confirm what information is sent to remote services.

Risk: Export-only mode may still process footage, and the security guidance notes file-writing side effects.

Mitigation: Do not assume export-only mode skips media processing; start with non-sensitive test footage and review files the skill writes.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-aggressive-behavior-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured analysis reports and Markdown report lists with links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include behavior type, event segments, involved-animal locations, intensity, alert level, and report links.]

## Skill Version(s):

1.0.16 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
