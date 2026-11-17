## Description:

Collect Xiaohongshu posts and comments, refresh single URLs, manage cookie updates, and support browser plugin integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengluday](https://clawhub.ai/user/pengluday)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain local, user-driven Xiaohongshu post and comment collection workflows, including full comment pagination, single-URL refreshes, saved-cookie handling, and browser-plugin backend integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A saved Xiaohongshu session cookie could expose authenticated account access if it is disclosed or stored carelessly.

Mitigation: Keep the cookie file private, never echo cookie values in user-facing output, and rotate or remove the cookie when it is no longer needed.

Risk: Collection and refresh operations may use authenticated access and should reflect the user's explicit intent.

Mitigation: Prefer explicit confirmation before running collection or refresh operations that use a saved or newly provided cookie.

Risk: Centralized mass collection from a shared server could increase platform and compliance risk.

Mitigation: Keep the workflow local-first and user-driven, and avoid proposing or implementing shared-server mass scraping.

## Reference(s):

- [Xiaohongshu Collector Workflow](references/collector-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code or configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation notes for CSV and JSON collection artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
