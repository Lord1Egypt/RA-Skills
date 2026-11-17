## Description:

Python Crawler Architect helps developers design Python web crawler systems, including SQLAlchemy data models, async collection pipelines, proxy and retry components, and data-cleaning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strong-cyber](https://clawhub.ai/user/strong-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to plan and implement crawler architectures, database schemas, async request flows, state management, retry behavior, and deployment notes for public-data collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawler guidance could be applied to unauthorized or terms-violating collection from third-party sites.

Mitigation: Use the skill only for authorized, terms-compliant collection of public data, and review generated plans against robots.txt, rate limits, privacy rules, and site terms before use.

Risk: Generated proxy templates may expose proxy credentials through credential-bearing URLs or unredacted logging.

Mitigation: Store proxy credentials in secrets or environment variables, avoid embedding credentials in proxy URLs, and redact proxy values from logs.

Risk: Default proxy health checks may call a third-party service and disclose network metadata.

Mitigation: Replace third-party health-check URLs with an approved internal endpoint or a site-specific authorized test endpoint.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, shell command, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory crawler designs and implementation templates; generated code requires review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
