## Description:

Analyzes full-body pet images or video to estimate breed or body type and fur density, then returns a personalized drying temperature and duration curve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, groomers, and pet-care device operators use the skill to estimate a pet's breed or body type and fur density from full-body media, then review a suggested drying temperature and duration curve. The recommendations are for care guidance and are not medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags credential handling and persistent personal data, while noting that the evidence is partial and does not establish malicious intent.

Mitigation: Review credential handling, account creation, and report storage before installation; use only a trusted service configuration.

Risk: The skill sends local or network pet images and videos to remote analysis services, and the security review calls out remote media processing.

Mitigation: Submit only media you are authorized to share, and check the service's data handling and retention practices first.

Risk: The security scan was partial, and the analysis implementation was not fully available for verification.

Mitigation: Review the complete source and dependencies before using real media or credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-adaptive-pet-drying-temperature-analysis)
- [Publisher profile](https://clawhub.ai/user/18072937735)
- [API reference](references/api_doc.md)
- [Usage demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON, Markdown]

**Output Format:** [Structured JSON analysis report; historical report lists can be presented as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include breed or body-type estimate, fur-density estimate, drying temperature and duration recommendations, risk notes, and a report link.]

## Skill Version(s):

1.0.14 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
