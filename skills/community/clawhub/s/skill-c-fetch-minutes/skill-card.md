## Description:

Automates post-meeting minutes processing by scanning eligible meetings, coordinating transcript retrieval, supporting AI issue extraction, committing transcript, minutes, summary, and draft issue files to Gitea, and returning organizer notification payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill in an OpenClaw cron workflow to process completed Tencent Meeting sessions into reviewable meeting minutes and draft issue content. It is intended for controlled meeting automation workflows that can safely access the configured Gitea repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan and modify multiple Gitea repositories.

Mitigation: Run it only in the intended controlled AIFusion environment, use a repo-scoped bot token, and add an explicit repository allowlist before deployment.

Risk: The default Gitea endpoint uses plaintext HTTP, which can expose tokens and meeting data.

Mitigation: Change the configured Gitea endpoint to HTTPS before use and rotate any token previously used with the HTTP endpoint.

Risk: Generated meeting artifacts and status transitions are written back to remote repositories.

Mitigation: Constrain commit-content input files to a controlled temporary directory and enforce valid meeting state transitions before remote writes.

Risk: Runtime dependencies are installed from broad version ranges.

Mitigation: Run dependencies in a virtual environment with pinned versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/skill-c-fetch-minutes)
- [Publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Files, Shell commands, Configuration]

**Output Format:** [JSON command responses and Markdown meeting artifacts committed as files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scan groupings, status-transition results, email payloads, and committed transcript.md, ai_summary.md, minutes.md, and draft_issue.md files when inputs are available.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
