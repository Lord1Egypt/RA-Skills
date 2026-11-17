## Description:

Calls the Midu public opinion insights API to return dimension-specific public-opinion analysis for a specified subject.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitallin](https://clawhub.ai/user/bitallin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request focused public-opinion insights for an event, topic, or entity across named dimensions such as media coverage, sentiment intensity, propagation, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and user queries may be exposed because requests use unencrypted HTTP.

Mitigation: Avoid confidential subjects, secrets, and sensitive internal material unless the service is moved to HTTPS and the API key is provisioned through a secure channel or secret manager; rotate any key used over an untrusted network.

## Reference(s):

- [Analysis Dimension Reference](references/analysis_dimension.md)
- [Midu API Key Setup Guide](references/apikey-fetch.md)
- [ClawHub Skill Page](https://clawhub.ai/bitallin/skills/public-opinion-insights)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON response that usually contains Markdown text in the result field]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and MIDU_API_KEY; complex analysis can take several minutes.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
