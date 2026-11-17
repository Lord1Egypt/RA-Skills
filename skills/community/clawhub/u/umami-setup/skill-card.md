## Description:

Add Umami self-hosted analytics to a website by creating the site in Umami, configuring a same-domain proxy for common web stacks, and verifying tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superworldsavior](https://clawhub.ai/user/superworldsavior)

### License/Terms of Use:


## Use Case:

Developers and site operators use this skill to add self-hosted Umami analytics to websites they control, including API setup, proxy configuration, and tracking verification across common deployment stacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps configure analytics in a way that can bypass ad blockers.

Mitigation: Use only on sites where analytics tracking, privacy notices, and consent handling are already approved.

Risk: The setup examples include Umami admin credentials in an inline shell command.

Mitigation: Prefer a no-echo prompt, scoped token, or safer credential flow, and clear temporary tokens after setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superworldsavior/skills/umami-setup)
- [CASYS homepage](https://casys.ai)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for Umami API calls and proxy rewrites for Next.js, Astro/Vercel, Caddy, and Nginx.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
