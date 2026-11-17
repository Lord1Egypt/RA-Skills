## Description:

Production-oriented Vikunja task/project management skill with deterministic commands and strong validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kohlhammond](https://clawhub.ai/user/kohlhammond)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent manage Vikunja tasks, projects, comments, labels, assignees, views, buckets, webhooks, attachments, relations, filters, notifications, subscriptions, and API tokens through deterministic shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and API token commands can expose or alter Vikunja access.

Mitigation: Use a least-privileged token, protect VIKUNJA_TOKEN from shared logs, and review token create/delete commands before execution.

Risk: Delete, bulk-update, and webhook commands can remove data or change external integrations.

Mitigation: Review each delete, bulk-update, and webhook command before running it, especially against shared or production projects.

Risk: Attachment commands can upload sensitive files or download content to sensitive paths.

Mitigation: Avoid uploading sensitive local files and verify download destinations before executing attachment commands.

Risk: The smoke test creates and modifies live Vikunja projects and tasks.

Mitigation: Run the smoke test only against a test instance or disposable project, not production.

## Reference(s):

- [Vikunja project homepage](https://vikunja.io/)
- [ClawHub skill page](https://clawhub.ai/kohlhammond/skills/vikunja-complete)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and JSON API output where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, VIKUNJA_URL, and VIKUNJA_TOKEN.]

## Skill Version(s):

4.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
