## Description:

Analyzes cat-tree video files or URLs to summarize activity by area, dwell times, transitions, and a 2D activity heatmap without diagnosing disease.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and developers use cat-tree camera footage to review where a cat spends time, how often it moves between levels, and historical activity reports. Results are for observation, not medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cat-tree footage or video URLs may expose private areas of a home when sent to LifeEmergence cloud services.

Mitigation: Share only footage you are comfortable uploading, obtain consent where needed, and check the service's data retention terms before use.

Risk: The skill silently creates or reuses cloud identities and stores service tokens, while cloud reports remain associated with a locally persisted identity.

Mitigation: Review identity and token handling before installation; the publisher should require user-approved authentication and clearly document consent, token storage, and report-retention controls.

## Reference(s):

- [Skill release on ClawHub](https://clawhub.ai/18072937735/skills/smyx-pet-climbing-frame-heatmap-analysis)
- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Text or Markdown with structured analysis results and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical cloud report lists are available; analysis results can be saved to a file.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata; artifact SKILL.md lists 1.0.18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
