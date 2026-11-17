## Description:

Fetches and interprets Rankscale GEO (Generative Engine Optimization) analytics, including brand visibility score, citation rate, sentiment, and top AI search terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mathias-rs](https://clawhub.ai/user/mathias-rs)

### License/Terms of Use:


## Use Case:

External marketers, GEO practitioners, and developers use this skill to retrieve Rankscale brand analytics from the Rankscale API and turn visibility, citation, sentiment, engine, and content-gap data into actionable reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One error path can print the full Rankscale API key into logs.

Mitigation: Configure the API key through OpenClaw Gateway or a secret manager, avoid passing it with --api-key, review terminal and gateway logs after failures, and rotate the key if exposure is possible.

Risk: The skill connects a Rankscale account and exposes brand analytics to the Rankscale API.

Mitigation: Use the skill only with intended Rankscale brands, invoke it with explicit Rankscale wording, and keep credentials scoped and rotated according to account policy.

Risk: A committed or broadly readable .env file could expose Rankscale credentials.

Mitigation: Keep .env out of version control, restrict local file permissions, and prefer managed secret injection where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mathias-rs/skills/rs-geo-analytics)
- [Rankscale Homepage](https://rankscale.ai)
- [Rankscale Documentation](https://docs.rankscale.ai)
- [Command Reference](references/COMMANDS.md)
- [Feature Guide](references/FEATURES.md)
- [API Integration Reference](references/api-integration.md)
- [Troubleshooting Guide](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text reports with Markdown documentation and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Rankscale PRO account, REST API activation, and RANKSCALE_API_KEY; reports may link to the Rankscale dashboard for full details.]

## Skill Version(s):

1.0.11 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
