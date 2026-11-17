## Description:

Audit any website across 8 quality signals to determine if it is outdated, broken, or neglected. Returns a structured audit dict used by the lead-scorer skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and automation teams use this skill to audit public websites for outdated, broken, or neglected signals and produce structured results for downstream lead scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs, including sensitive internal or confidential targets if deployed without scope controls.

Mitigation: Use outbound network controls, URL allowlisting, private-address blocking, and redirect validation before execution.

Risk: The skill can return full page contents through raw_html, which may expose sensitive page data in downstream workflows.

Mitigation: Apply response-size limits and clear handling controls for raw_html, especially before storing or sharing audit results.

Risk: Google PageSpeed checks submit target URLs to an external service.

Mitigation: Avoid using the skill on internal, customer-confidential, pre-release, or token-bearing URLs unless external submission is approved.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, code, configuration, guidance]

**Output Format:** [Structured audit dictionary with supporting Markdown and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAGESPEED_API_KEY for Google PageSpeed checks; returns raw_html when a site is live.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
