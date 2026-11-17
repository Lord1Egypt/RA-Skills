## Description:

Analyzes images and videos for possible falls and returns structured results and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Household users and care providers can submit an image or video for on-demand fall analysis and retrieve structured results or prior reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private footage may be uploaded to a remote service, and retention, deletion, and account controls are unclear; stored credentials also lack clear user controls.

Mitigation: Before using private footage, obtain clear upload, retention, deletion, and account-control information from the publisher. Avoid shared workspace identities and do not rely on --export-env-only to prevent uploads.

Risk: The bundled workflow does not demonstrate continuous monitoring or emergency notifications despite the skill's monitoring and alarm claims.

Mitigation: Treat the skill as on-demand remote analysis until continuous monitoring and emergency notifications are demonstrated; verify suspected falls independently and contact emergency help as appropriate.

## Reference(s):

- [API Interface Notes](references/api_doc.md)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-elderly-fall-detection-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Report links]

**Output Format:** [Structured analysis text or JSON, with report links; history results may be returned as structured text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one image, video, or URL per analysis; can also list prior reports.]

## Skill Version(s):

1.0.18 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
