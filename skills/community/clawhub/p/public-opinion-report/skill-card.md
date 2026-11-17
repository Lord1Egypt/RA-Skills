## Description:

Calls the Midu Public Opinion Report service to generate public opinion analysis reports in Markdown for supported report types such as incident, topic, industry, event, brand, city, regional online information, and public policy reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitallin](https://clawhub.ai/user/bitallin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request public opinion analysis reports from the Midu service by passing a report requirement message. It can generate new Markdown reports and supports follow-up report refinement through the service workflow described by the artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials and sends report prompts to an internal plaintext HTTP service.

Mitigation: Install only in trusted environments, configure MIDU_API_KEY securely, avoid sending secrets or regulated content unless approved, and prefer a release that uses HTTPS and documents secret handling.

Risk: Generated public opinion reports may contain inaccurate or misleading analysis.

Mitigation: Review generated reports before relying on them or sharing them externally.

## Reference(s):

- [Midu API Key Setup Guide](artifact/references/apikey-fetch.md)
- [ClawHub skill page](https://clawhub.ai/bitallin/skills/public-opinion-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [JSON response containing a Markdown report result, with setup and usage guidance in Markdown and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and MIDU_API_KEY; report generation may take 5 to 20 minutes.]

## Skill Version(s):

0.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
