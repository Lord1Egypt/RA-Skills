## Description:

Helps agents discover, track, sync, and query news, RSS, social, financial, and other external sources through agent-data-cli and configured source workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[severinzhong](https://clawhub.ai/user/severinzhong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to translate data-source tasks into agent-data-cli command flows for discovery, subscription, sync, local querying, and explicit remote interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users toward installing mutable third-party code.

Mitigation: Install only from trusted sources, pin a known commit or version, and review dependency setup before use.

Risk: Scheduler examples can create recurring background syncs.

Mitigation: Use cron, launchd, or systemd only when recurring sync is intended and the disable path is understood.

Risk: Install and uninstall interactions through data_hub can cause remote or local side effects.

Mitigation: Confirm the source, verb, and explicit refs before allowing install, uninstall, or other content interaction commands.

## Reference(s):

- [using-data-cli ClawHub release](https://clawhub.ai/severinzhong/skills/using-data-cli)
- [Command Semantics](references/command-semantics.md)
- [Task Patterns](references/task-patterns.md)
- [Result Reporting](references/result-reporting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise execution reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSONL-oriented command examples for downstream filtering.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
