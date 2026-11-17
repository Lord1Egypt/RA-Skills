## Description:

Manage tasks and projects on a self-hosted Vikunja instance via the Vikunja REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickian](https://clawhub.ai/user/nickian)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to let an agent list, search, create, complete, and inspect tasks and projects on a self-hosted Vikunja instance. It also supports due-date checks, overdue task summaries, notifications, and scheduled reminder workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script has unsafe input handling that can run crafted local code.

Mitigation: Review and fix argument URL encoding before routine use, and avoid passing untrusted search, filter, project, or task values to the script.

Risk: The Vikunja API token may be exposed if the skill is configured with an HTTP endpoint.

Mitigation: Use only trusted HTTPS Vikunja URLs and reject non-HTTPS remote URLs before sending authenticated requests.

Risk: Write actions can create projects, create tasks, or mark tasks complete.

Mitigation: Require clear user confirmation before write actions and use a least-privilege Vikunja API token.

Risk: Due-date behavior assumes the America/Denver timezone.

Mitigation: Make the timezone configurable before relying on scheduled or due-date workflows in other locales.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickian/skills/vikunja-tasks)
- [Vikunja filter documentation](https://vikunja.io/docs/filters)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI text or JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIKUNJA_URL and VIKUNJA_TOKEN environment variables and a reachable Vikunja REST API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
