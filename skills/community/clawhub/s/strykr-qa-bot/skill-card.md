## Description:

AI-powered QA for the Strykr trading platform with pre-built tests for crypto signals, stock signals, news, economic events, AI chat, PRISM API health checks, and known issue tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:

MIT

## Use Case:

Developers and QA engineers use this skill to run regression, smoke, and health checks for the Strykr finance dashboard after deployments or feature changes. It helps validate page loading, navigation, filters, signal cards, AI chat responses, PRISM endpoints, known issues, screenshots, console errors, timing, and markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned external npm tool through npx, which may change between runs.

Mitigation: Pin web-qa-bot to an exact reviewed version, commit a lockfile, and run the local locked binary in CI.

Risk: Browser tests, API checks, screenshots, console logs, and reports may expose financial application data or account context.

Mitigation: Use test accounts, avoid production sessions and secrets, restrict network access to intended Strykr hosts, and handle generated artifacts as sensitive.

Risk: Some helper methods contain placeholder browser-context logic and may not independently prove page behavior without the underlying web-qa-bot runner.

Mitigation: Review generated reports and screenshots, and verify critical assertions against the actual browser runner before relying on results for release decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nextfrontierbuilds/skills/strykr-qa-bot)
- [Strykr application](https://app.strykr.ai)
- [web-qa-bot dependency](https://github.com/NextFrontierBuilds/web-qa-bot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, terminal status output, YAML configuration, TypeScript helper APIs, screenshots, console error captures, and timing metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can mark pass, fail, skip, and known-issue statuses; screenshots and console logs may contain sensitive application or account data.]

## Skill Version(s):

0.1.2 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
