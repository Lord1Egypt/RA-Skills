## Description:

Fetch agent-ready cleaned Markdown from the Distiller API instead of relying on raw webpage fetches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardyen724-g](https://clawhub.ai/user/edwardyen724-g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add a hosted webpage-to-Markdown step to agent workflows, including setup guidance when a Distiller API key is not yet configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chosen webpage URLs are sent to Distiller's hosted service.

Mitigation: Avoid private intranet pages, authenticated pages, regulated data, or sensitive customer content unless the organization has approved that data flow.

Risk: CLI installation and API-key handling introduce normal third-party package and credential exposure risk.

Mitigation: Install the CLI in a virtual environment, pin a reviewed package version when possible, and use a revocable Distiller API key with limited exposure.

Risk: Endpoint availability and access level can change workflow behavior, especially for paid POST /distill access and unavailable POST /extract flows.

Mitigation: Default to POST /markdown, fall back to POST /markdown if POST /distill is denied, and avoid new workflows around POST /extract until it is re-enabled.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/edwardyen724-g/skills/web-distiller)
- [Distiller service](https://webdistiller.dev)
- [Distiller sign-in](https://webdistiller.dev/signin)
- [Distiller dashboard](https://webdistiller.dev/dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, environment configuration, and Distiller CLI/API output in markdown, text, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DISTILLER_API_BASE and DISTILLER_API_KEY; defaults to POST /markdown, reserves POST /distill for paid Starter access, and avoids POST /extract while unavailable.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
