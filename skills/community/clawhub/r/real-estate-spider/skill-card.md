## Description:

Real Estate Spider helps agents collect Chinese real estate listing data from Anjuke, Soufun, Beike, and Lianjia using Python scraping and browser automation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h8296699](https://clawhub.ai/user/h8296699)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to configure real estate crawlers, run browser-assisted collection workflows, and export listing attributes such as price, area, location, house type, decoration, and build year. Users should apply it only where they have permission to collect data from the target sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes anti-bot and CAPTCHA-bypass workflows that may conflict with target site policies.

Mitigation: Use it only with permission from the target site or data owner, and review the target site's terms before running collection workflows.

Risk: Saved browser sessions, screenshots, PDFs, and scraped listing data may contain sensitive or account-linked information.

Mitigation: Avoid saving authenticated sessions unless necessary, store generated artifacts outside shared folders, and exclude them from source control.

Risk: The CAPTCHA-solving example sends an image to an external service and uses an API credential.

Mitigation: Do not use the example unless the image path, provider, and credential handling are fully controlled and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h8296699/skills/real-estate-spider)
- [Publisher profile](https://clawhub.ai/user/h8296699)
- [README](artifact/README.md)
- [CAPTCHA strategies](artifact/docs/captcha_strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell command, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate scraped data files, browser screenshots, and saved session state when the included scripts are executed.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
