## Description: <br>
Opinionated AI code reviewer for pull requests, local diffs, commits, and files, with six-layer review across logic, edge cases, performance, security, maintainability, and architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitHub pull requests, local diffs, commits, or individual files and receive prioritized, paste-ready review findings. It is intended for code quality, security, performance, maintainability, and architecture review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook mode can send repository diffs to Anthropic and post GitHub reviews using repository credentials. <br>
Mitigation: Deploy webhook mode only after review; use a dedicated least-privilege GitHub bot or GitHub App, restrict network exposure, and avoid repositories whose code cannot be shared with Anthropic. <br>
Risk: Automated webhook reviews can post APPROVE or REQUEST_CHANGES without human judgment. <br>
Mitigation: Consider comment-only behavior or require human approval before posting merge verdicts. <br>
Risk: Webhook requests are higher risk if the webhook signature secret is missing or misconfigured. <br>
Mitigation: Always configure GITHUB_WEBHOOK_SECRET and verify deployment settings before exposing the service. <br>


## Reference(s): <br>
- [Smart PR Review on ClawHub](https://clawhub.ai/fullstackcrew-alpha/smart-pr-review) <br>
- [README](README.md) <br>
- [Code Review Checklist](references/review-checklist.md) <br>
- [Anti-Patterns](references/anti-patterns.md) <br>
- [Review Examples](references/review-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown code review report with severity sections, replacement code examples, and merge verdict guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can output Chinese or English review text and may include shell commands for collecting PR, diff, commit, or file context.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
