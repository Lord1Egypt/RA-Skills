## Description:

Detects cats, dogs, and birds in images and video for home pet monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External users can submit local images, videos, or media URLs to identify and count cats, dogs, and birds, then review analysis reports or query report history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious based on reported account and credential handling, broad report access, and privacy-sensitive behavior; its scan is partial.

Mitigation: Review identity and token handling, restrict report access to authorized users, and review the missing component before relying on the scan.

Risk: Images and videos sent for analysis may contain private home footage.

Mitigation: Submit only media approved for remote processing and avoid footage containing sensitive personal information.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-pet-detection-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API interface notes](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [Structured JSON or plain-text detection report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include detected pet categories, counts, confidence values, and report links.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata; bundled SKILL.md frontmatter says 1.0.25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
