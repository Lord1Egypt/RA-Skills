## Description:

Review YouTube upload metadata and publish-readiness notes before a human handles the final upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and channel operators use this skill to review YouTube titles, descriptions, thumbnail notes, tags, playlist choices, and upload-readiness checklists before a human performs the final upload or scheduling step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be asked to handle account access, credentials, cookies, recovery details, private analytics exports, or final publishing actions.

Mitigation: Keep the skill to planning and metadata QA, do not provide account secrets or private exports, and keep upload or scheduling actions under direct human control.

Risk: Viewer-facing metadata may include unsupported claims, policy-sensitive statements, copyrighted media references, or private personal information.

Mitigation: Verify claims against the video content or user-provided sources and review made-for-kids, medical, financial, legal, educational, copyright, and privacy-sensitive areas before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/youtube-openclaw-creator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown checklist and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cleaned metadata, recommendations, thumbnail notes, human-upload checklist, risks, and missing assets.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
