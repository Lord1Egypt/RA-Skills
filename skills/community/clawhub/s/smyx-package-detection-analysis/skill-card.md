## Description:

Detects delivery packages in a surveillance area for inventory checks and unattended-item alerts at parcel stations, residential entrances, and office lobbies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External operators at parcel stations, residential entrances, and office lobbies use the skill to detect and count visible packages, identify unattended items, and retrieve prior reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious for credential and identity handling, remote requests, and behavior beyond package detection.

Mitigation: Before use, verify the service destinations, the identity and video data sent, and how credentials and user records are stored.

Risk: Scanning was partial because one local path-like reference was missing.

Mitigation: Locate and inspect the missing referenced item before relying on the security assessment.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured package-detection results and Markdown report lists with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes local images or videos and network URLs; historical reports are retrieved from the service.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata; artifact frontmatter reports 1.0.25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
