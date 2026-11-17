## Description:

Creates live dashboards, complete websites, and social-proof pages for Wesley-Agent with mobile-first HTML, CSS, JavaScript, live API data, media integration, and Cloudflare sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate and deploy live marketing dashboards, trading views, signal pages, and proof galleries for Wesley-Agent. It produces standalone web files and deployment guidance for VPS and Cloudflare tunnel workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment guidance can expose dashboard and API services publicly.

Mitigation: Do not expose the API until access controls are reviewed; restrict CORS to approved origins and use Cloudflare sharing intentionally.

Risk: Deployment commands can involve root SSH, container changes, open ports, and long-running services.

Mitigation: Replace hardcoded infrastructure details, avoid root SSH where possible, use a least-privilege deploy user, and confirm each administrator action before running it.

Risk: Telegram uploads require bot credentials and can introduce external data into generated galleries.

Mitigation: Store Telegram tokens as environment secrets and enable uploads only after explicit user approval and content handling review.

Risk: Unpinned dependencies and public CDN imports can change behavior over time.

Mitigation: Pin dependency versions and review third-party script and font imports before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/georges91560/skills/wesley-dashboard-builder)
- [Publisher Profile](https://clawhub.ai/user/georges91560)
- [Deployment Guide](artifact/DEPLOYMENT.md)
- [Design System](artifact/DESIGN_SYSTEM.md)
- [Telegram Bot API](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, configuration snippets, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce standalone inline web files, deployment steps, API integration guidance, and fallback data behavior.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
