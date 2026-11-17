## Description:

Systematic team status tracking via Slack DMs with confidential Obsidian-based internal tracking that gathers actionable project updates from team members.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parthpandya1729](https://clawhub.ai/user/parthpandya1729)

### License/Terms of Use:

MIT

## Use Case:

Managers and team leads use this skill to request project status updates by Slack DM, follow up on missing or vague responses, and maintain confidential Obsidian notes about progress, blockers, response quality, and support needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Slack access for direct messages and status monitoring.

Mitigation: Install it only after organizational approval, configure Slack scopes narrowly, and verify the gateway used for Slack access is trusted.

Risk: The skill stores named workplace behavior, response quality, and response-time records in Obsidian.

Mitigation: Store notes only in a protected location, define retention and deletion rules before use, and avoid subjective behavioral profiling unless explicitly authorized.

Risk: The workflow may expose sensitive commercial or personnel information if confidentiality settings are changed without approval.

Mitigation: Keep finance transparency disabled by default and share financial or personnel details only under approved policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parthpandya1729/skills/team-status-tracker)
- [README](README.md)
- [Status Request Templates](templates/status-request.md)
- [Obsidian Daily Status Tracking Template](templates/obsidian-tracking.md)
- [Configuration Template](config.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with message templates, configuration snippets, and example shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Slack and Obsidian skills; Slack access should be scoped narrowly and configured through an approved gateway.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
