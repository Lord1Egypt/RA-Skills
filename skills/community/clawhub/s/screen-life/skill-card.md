## Description:

screen-life monitors daily macOS computer activity and generates readable digital activity reports, with optional AI insights when LLM credentials are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vineindalvik](https://clawhub.ai/user/vineindalvik)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and productivity-minded developers use this skill to review daily or weekly macOS application usage, browser activity, notes activity, and AI-tool activity. It can produce local reports, optional LLM-generated insights, and optional Feishu notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill monitors potentially sensitive app, browser, notes, and AI-tool activity.

Mitigation: Install only after reviewing the disclosed data sources and confirming the monitored user has approved this local activity collection.

Risk: The installer creates a persistent macOS background agent.

Mitigation: Review the LaunchAgent target script before installation and use the documented stop or uninstall commands when background monitoring is no longer intended.

Risk: Reports may be sent to a configured LLM endpoint or Feishu webhook despite the local-only privacy statement.

Mitigation: Use --no-llm and avoid setting LLM or webhook environment variables unless external report sharing has been explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vineindalvik/skills/screen-life)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown or JSON activity reports, plus CLI status and installation command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; optional LLM analysis; optional Feishu push delivery.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
