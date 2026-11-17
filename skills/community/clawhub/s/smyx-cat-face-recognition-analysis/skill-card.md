## Description:

Identifies individual cats from face images or videos by comparing them with a pre-registered database and provides recognition reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Cat owners and pet-care operators use this skill to identify individual cats from photos or videos and retrieve previous recognition reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cat photos, videos, and submitted URLs are sent to lifeemergence.com services for analysis.

Mitigation: Obtain permission before sending media and avoid sensitive media or private/internal URLs.

Risk: Cloud report history may be queried automatically, and a service identity may be created or reused without an explicit prompt.

Mitigation: Review the cloud-history and account behavior before use and restrict use to intended accounts and reports.

Risk: Service tokens are stored locally in the workspace data directory.

Mitigation: Limit access to the workspace data directory and remove stored tokens when no longer needed.

## Reference(s):

- [Cat face recognition API documentation](artifact/references/api_doc.md)
- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-cat-face-recognition-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured recognition report and Markdown history table with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recognition depends on a pre-registered cat database and clear, well-lit images.]

## Skill Version(s):

1.0.12 (source: ClawHub server-resolved release; artifact frontmatter says 1.0.21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
