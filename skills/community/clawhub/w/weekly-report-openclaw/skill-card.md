## Description:

Automates weekly report generation by logging into a report system, fetching team report entries, summarizing them with an LLM, and producing a formatted Word document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaillera999](https://clawhub.ai/user/kaillera999)

### License/Terms of Use:


## Use Case:

Employees, team leads, and operations staff use this skill to compile weekly team activity data into structured summaries and Word reports for the current, previous, or a specified week.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles report-system credentials and cached authentication tokens.

Mitigation: Use least-privilege test credentials first, keep secrets out of project `.env` files, and protect or delete `.token_cache` after use.

Risk: Team report content may be confidential and is summarized through the configured LLM provider.

Mitigation: Process confidential reports only after organizational approval and with an approved LLM endpoint and data-handling policy.

Risk: Security evidence flags weak transport safeguards for the report system.

Mitigation: Use an HTTPS report-system endpoint before handling real workplace data.

Risk: Setup guidance includes running a streamed remote installer.

Mitigation: Verify installer source and contents independently or install dependencies through approved package-management procedures.

Risk: The data cache can contain raw team report data.

Mitigation: Protect or delete `.data_cache` after use and avoid storing it in shared or versioned directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaillera999/skills/weekly-report-openclaw)
- [Configuration Guide](references/configuration.md)
- [Workflow Guide](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; runtime output is JSON status plus a .docx report file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires report-system credentials and an LLM API key; generated reports are saved as Word documents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
