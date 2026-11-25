## Description:

Automates ZhanFu storefront workflows through its WebDriver client, using Playwright for browser tasks after a store is opened.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangzhang1997](https://clawhub.ai/user/zhangzhang1997)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use it to manage ZhanFu stores and automate pages in store browsers with Playwright.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rated the release suspicious with medium confidence, citing client and store management workflows that can terminate processes or delete caches without a required confirmation gate; analysis of much of the package was incomplete.

Mitigation: Review recovery and cache deletion safeguards before use, verify the bundled Playwright files and dependency lockfile, and confirm watcher and required environment, network, or shell access is acceptable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhangzhang1997/skills/zhanfu-playwright)
- [ZhanFu WebDriver API reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [Text, Browser actions, Guidance]

**Output Format:** [Concise status text and browser interactions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer; some store management actions are Windows only.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
