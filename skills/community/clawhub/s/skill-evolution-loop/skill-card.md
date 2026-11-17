## Description:

Skill Evolution Loop scans recent agent session history for repeated tool-backed tasks, proposes or distills reusable skills, scores and improves them, and can generate workflow files and cleanup reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgx281227231](https://clawhub.ai/user/lgx281227231)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to identify repeated tool-backed work, draft reusable skills from observed patterns, improve skill documentation quality, orchestrate workflow files, and review stale auto-generated skills for cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans private local session history to identify automation candidates.

Mitigation: Run it only in environments where the operator has approved local session-history scanning and understands what data may be reviewed.

Risk: The skill can create persistent skills from chat-derived task patterns.

Mitigation: Treat generated skills as drafts and inspect their instructions, commands, and boundaries before activation or publication.

Risk: The cleanup command can delete auto-generated skill directories when run outside dry-run mode.

Mitigation: Use dry-run cleanup first and require explicit confirmation or quarantine before deletion.

Risk: The documented protected cron-job safeguard may not be fully enforced.

Mitigation: Do not rely on protected-job documentation alone; verify enforcement before allowing automated cron-job changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lgx281227231/skills/skill-evolution-loop)
- [Whitelist Domain Configuration](references/whitelist-domains.md)
- [Protected Cron Jobs](references/protected-cron-jobs.md)
- [ClawHub Workflow Competitive Analysis](references/clawhub-competitive-intel.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, generated SKILL.md files, workflow YAML, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local skill files, workflow configuration, state files, logs, candidate reports, and cleanup reports when its commands are run.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
