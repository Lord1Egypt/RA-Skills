## Description:

SEO-Awesome guides agents through first-party Google API-driven SEO automation, covering keyword research, pSEO page generation, staged publishing, monetization, site setup, and GA4-based review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsorgcn](https://clawhub.ai/user/adsorgcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and SEO automation teams use this skill to design and operate data-driven SEO workflows using Google APIs, LLM-assisted content assembly, staged publishing, and analytics feedback loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google API, GA4, and lead form integrations can expose credentials or sensitive analytics and user data if configured carelessly.

Mitigation: Use least-privilege credentials, store secrets in environment variables or a secret manager, avoid placing secrets in chat or source control, and retain only aggregate analytics needed for decisions.

Risk: Automated page generation, publishing Cron jobs, and analytics-driven changes can create incorrect or excessive live-site updates.

Mitigation: Start in staging or dry-run mode, require human review before production publishing, set daily publication and strategy-change limits, keep recent logs, and maintain a rollback path.

## Reference(s):

- [SEO-Awesome ClawHub listing](https://clawhub.ai/adsorgcn/skills/seo-awesome)
- [iLang homepage](https://ilang.ai)
- [Gefei SEO](https://seo.web.cafe/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured steps, code snippets, shell commands, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English guidance; recommends staging, human review, dry runs, least-privilege credentials, daily change limits, and rollback paths for live-site automation.]

## Skill Version(s):

1.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
