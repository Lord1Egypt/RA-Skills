## Description:

Helps agents crawl Chinese real estate listing sites, including Anjuke, Ke.com, Lianjia, and Soufun, with data extraction, export, browser automation, and anti-bot bypass guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h8296699](https://clawhub.ai/user/h8296699)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to collect and export real estate listing data for market research, property trend analysis, platform comparison, and related data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill teaches anti-bot and CAPTCHA bypass techniques for third-party real estate sites.

Mitigation: Use it only with explicit permission from target sites and confirm that collection complies with applicable terms, laws, and internal policy.

Risk: Saved browser sessions, cookies, and verified states can function as secrets.

Mitigation: Avoid real account sessions, store any session files securely, and rotate or delete them after use.

Risk: The CAPTCHA guidance discusses third-party solver APIs.

Mitigation: Do not upload CAPTCHA images or related site data to third-party solvers unless that use has been reviewed and approved.

Risk: The main entry point builds shell commands from CLI values.

Mitigation: Do not pass untrusted CLI values to main.py; prefer fixed, reviewed arguments or direct script invocation.

Risk: Runtime dependencies are installed from package managers.

Mitigation: Pin and review dependencies before installation in production or shared environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/h8296699/skills/real-estate-crawler)
- [README](artifact/README.md)
- [Anti-Crawler Guide](artifact/docs/anti_crawler_guide.md)
- [CAPTCHA Strategies](artifact/docs/captcha_strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell command, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports JSON, CSV, Excel, HTML report, and chart exports when its crawler scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
