## Description:

Checks whether an AI agent skill is safe before installation or use by querying the PYX Scanner API for trust status, risk score, and safety recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fysoul17](https://clawhub.ai/user/fysoul17)

### License/Terms of Use:


## Use Case:

Developers and agent users use Pyx Scan to check an owner/name agent skill before installing or using it and to receive a concise safety report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-triggering and the curl fallback can make unintended network or shell calls more likely.

Mitigation: Limit use to explicit PYX scan requests, restrict owner/name to safe characters, and prefer a structured HTTP call over the Bash fallback.

Risk: Network, rate-limit, or unavailable scanner responses can leave a skill unverified.

Mitigation: Treat ERROR or UNSCANNED results as unverified and require manual source review before installing or using the target skill.

## Reference(s):

- [PYX Scanner](https://scanner.pyxmate.com)
- [ClawHub skill page](https://clawhub.ai/fysoul17/skills/pyx-scan)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Structured Markdown safety report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Omits null or empty scan data and asks for confirmation before proceeding on caution verdicts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
