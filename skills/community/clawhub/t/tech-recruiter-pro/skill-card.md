## Description:

Tech Recruiter Pro helps agents source and evaluate algorithm and R&D candidates across technical, academic, professional, and community platforms, generate personalized outreach, and manage a recruiting pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biancabian77](https://clawhub.ai/user/biancabian77)

### License/Terms of Use:

MIT

## Use Case:

Recruiters, hiring managers, and technical talent sourcers use this skill to find, compare, and contact algorithm and R&D candidates using public technical profiles, academic signals, and recruiting pipeline notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill profiles real people across multiple public platforms and may store candidate names, roles, contact links, academic metrics, and outreach history.

Mitigation: Use it only in approved recruiting workflows, minimize collected fields, define retention and deletion rules, and review applicable hiring-law and privacy obligations before storing or exporting candidate data.

Risk: Artifact behavior and server security guidance identify web scraping, CAPTCHA handling, proxy use, and platform terms-of-service concerns.

Mitigation: Prefer official APIs, respect rate limits and robots.txt, disable or remove CAPTCHA and proxy workarounds, and stop collection when a platform blocks or challenges access.

Risk: Automated matching scores and filters can create unfair or legally sensitive recruiting decisions, especially when age-related criteria or proxy variables are used.

Mitigation: Keep scores advisory, require human review before outreach or rejection, and avoid protected-class, age, or proxy criteria unless counsel and policy explicitly approve them.

Risk: Optional API tokens and Feishu integration can expose credentials or candidate data if stored insecurely.

Mitigation: Pin dependencies, keep tokens in a secret manager, avoid committing credentials, and restrict access to local exports and Feishu Bitable records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biancabian77/skills/tech-recruiter-pro)
- [README](artifact/README.md)
- [Quick Start Guide](artifact/QUICKSTART.md)
- [Platform Guide](artifact/docs/PLATFORM_GUIDE.md)
- [9 Platforms Overview](artifact/docs/9_PLATFORMS_OVERVIEW.md)
- [Security Fixes](artifact/SECURITY_FIXES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports, JSON-like candidate profiles, generated outreach email text, and Python or configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local candidate records, email templates, and recruiting reports; Feishu Bitable storage requires separate configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
