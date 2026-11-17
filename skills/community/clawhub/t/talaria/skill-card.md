## Description:

Opt-in Playwright stealth wrapper for websites the user owns or is explicitly authorized to test. Use only when the user explicitly requests stealth or a documented bot-detection block prevents authorized automation; do not invoke for generic browsing or scraping. Not a CAPTCHA solver.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gadielkalleb](https://clawhub.ai/user/gadielkalleb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use Talaria to run explicitly authorized Playwright browser visits, screenshots, HTML capture, or API-based flows when basic bot-detection signals block normal automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stealth browser automation can be misused against websites where the user lacks authorization.

Mitigation: Use the skill only for sites the user owns or is explicitly allowed to test, and confirm the target URL and authorization when unclear.

Risk: Proxy credentials may be exposed if handled carelessly during automation.

Mitigation: Treat proxy variables as secrets and avoid printing, embedding, or saving proxy credentials in URLs, logs, screenshots, HTML, or source files.

Risk: Saved screenshots or HTML may contain sensitive page data or be written to unintended paths.

Mitigation: Review user-provided output paths before capture and save screenshots or HTML only when explicitly requested.

## Reference(s):

- [Talaria ClawHub Skill Page](https://clawhub.ai/gadielkalleb/skills/talaria)
- [Talaria GitHub Homepage](https://github.com/gadielkalleb/talaria)
- [How to Bypass CAPTCHAs With Playwright](https://brightdata.com.br/blog/dados-do-site/bypass-captchas-with-playwright)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with bash and JavaScript snippets; optional CLI JSON, PNG screenshots, and HTML files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional proxy and headless-mode environment variables; writes screenshots and HTML only to user-provided output paths.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact frontmatter/package.json: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
