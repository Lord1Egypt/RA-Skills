## Description:

Analyzes videos of pets in carriers to estimate breathing rate, flag elevated rates, and provide a report without diagnosing disease.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and transport staff can submit a carrier video or video URL to check a pet's breathing rate and review alerts during travel. They can also request past cloud reports; results are informational, not a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet videos or video URLs are sent to a cloud analysis service.

Mitigation: Ask for consent before uploading and explain how the service handles and retains videos.

Risk: The skill silently creates or reuses an identity and stores authentication tokens locally.

Mitigation: Disclose account creation and token storage; provide a way to review and delete stored identity data.

Risk: Cloud report history can be retrieved without clear user-facing control.

Mitigation: Request confirmation before history lookups and explain access and deletion options.

## Reference(s):

- [Skill API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-pet-carrier-respiratory-rate-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Breathing-rate estimates, alerts, report links, and optional cloud report history.]

## Skill Version(s):

1.0.11 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
