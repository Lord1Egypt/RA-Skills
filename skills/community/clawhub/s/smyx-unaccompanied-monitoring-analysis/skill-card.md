## Description:

Analyzes monitoring images or videos for prolonged periods without interaction or visitors and returns structured reports to support remote elder-care review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Families and elder-care providers can review monitoring images or videos and query prior reports as one input to remote check-ins for older adults living alone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious with high confidence and reports a possible mismatch between its elder-monitoring description and its video-analysis and reporting features.

Mitigation: Review the actual analysis and reporting behavior before use, and confirm that it matches the intended care workflow.

Risk: The security review raises privacy concerns about media and identity information sent to external services, possible account creation, and processing that may occur even when a no-analysis option is claimed.

Mitigation: Before sharing footage, clarify what media and identity data is transmitted and whether accounts or processing are triggered; use only with appropriate consent.

Risk: Automated monitoring results may be incomplete or misleading, and the security review says the external analysis behavior remains unverified because scan coverage was partial.

Mitigation: Treat reports as prompts for a human welfare check, verify alerts before acting, and do not use them as a substitute for direct contact or professional care.

## Reference(s):

- [API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-unaccompanied-monitoring-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis results and report links, presented as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include monitoring findings, recommendations, and links to report exports.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
