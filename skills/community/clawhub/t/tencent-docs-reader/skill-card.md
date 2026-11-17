## Description:

Reads publicly shared Tencent Docs spreadsheets through agent-browser copy and paste and returns tab-separated text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cm-wenge](https://clawhub.ai/user/cm-wenge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read public Tencent Docs spreadsheet data, select a tab when needed, and return the content as tab-separated text for follow-on analysis or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can read document contents from the target Tencent Docs page.

Mitigation: Use the skill only with trusted document URLs, validate URLs manually, and avoid sensitive documents unless the browser environment is controlled.

Risk: The package includes a weekly-report workflow that can send employee names to a configured webhook.

Mitigation: Review or remove check_weekly_report.py before use and do not set WECOM_WEBHOOK_URL unless that notification behavior is intended.

Risk: The reader depends on Tencent Docs UI behavior and agent-browser copy-paste automation.

Mitigation: Test against representative spreadsheets before relying on the output, especially after Tencent Docs interface changes or for large sheets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cm-wenge/skills/tencent-docs-reader)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [Plain text with tab-separated rows; optionally saved to a text file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.x and agent-browser; output depends on the visible spreadsheet content and selected tab.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
