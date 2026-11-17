## Description:

AI-powered automated QA for web apps. Smoke tests, accessibility, visual regression. Works with Cursor, Claude, ChatGPT, Copilot. Vibe-coding ready.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:

MIT

## Use Case:

Developers and QA engineers use this skill to run browser-based smoke tests, accessibility-oriented checks, visual regression workflows, and report generation for web applications before or after deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted URLs, YAML or JSON test steps, report paths, or company names could trigger local command execution through unsafe shell command construction.

Mitigation: Review before installing, run only trusted test suites against staging or test accounts, and fix shell command construction before broader use.

Risk: Screenshots, console logs, and generated reports may capture sensitive application data.

Mitigation: Use test accounts and non-production data, restrict artifact storage, and scrub or protect generated reports before sharing.

Risk: PDF output depends on ai-pdf-builder behavior that is not fully reviewed, declared, and pinned in the evidence.

Mitigation: Prefer Markdown or JSON reports and avoid PDF generation until ai-pdf-builder is reviewed, declared, and pinned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextfrontierbuilds/skills/web-qa-bot)
- [npm package](https://www.npmjs.com/package/web-qa-bot)
- [README](README.md)
- [Report template](templates/report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, YAML, JSON, and TypeScript examples; generated QA reports may be Markdown, JSON, or PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include test summaries, console findings, screenshots, and report files.]

## Skill Version(s):

0.1.3 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
