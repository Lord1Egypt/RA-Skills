## Description:

Analyzes local authentication, web, PowerShell, and Windows event logs for suspicious activity and produces evidence timelines and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Security analysts and system administrators use the skill to review authorized local logs during security triage, incident response, and audit work. It flags suspicious patterns for human verification and provides review suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may update multiple agent directories without the expected confirmation.

Mitigation: Choose one explicit --agent or --dir, review a --dry-run first, and avoid default or global installation until confirmation behavior is fixed. Back up existing skill files.

Risk: A report may overwrite a source log, and reports contain original log evidence.

Mitigation: Analyze read-only copies, specify individual files when practical, write reports to a new path outside the inputs, and protect reports as sensitive data.

## Reference(s):

- [Authentication log rules](references/auth-log-rules.md)
- [Web access log rules](references/web-log-rules.md)
- [PowerShell log rules](references/powershell-log-rules.md)
- [Windows event log rules](references/windows-event-rules.md)
- [Analysis specification](references/analysis-spec.md)
- [Project homepage](https://github.com/YottaMeta/yotta-logwatch)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-logwatch)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [Timeline and findings in text, JSON, or Markdown, with Chinese explanations and review suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are heuristic indicators of suspicious activity and require human review.]

## Skill Version(s):

0.3.3 (source: frontmatter, package.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
