## Description:

Detects delivery packages in a target surveillance area for inventory checks and unattended alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Teams managing community parcel stations, residential entrances, and office lobbies can use this skill to analyze surveillance images or videos, count detected packages, and review unattended-package reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks this release suspicious and reports account creation, credential storage, persistent local records, and external processing beyond the stated package-detection purpose. The assessment is partial because a referenced local path was missing.

Mitigation: Review the complete source and how identity, credentials, stored records, and external processing are handled before installation; avoid installing until you are comfortable with those behaviors.

## Reference(s):

- [Package detection API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-package-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Text analysis results and Markdown history-report tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include detected package counts, location markers, unattended-item alerts, recommendations, and report links.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
