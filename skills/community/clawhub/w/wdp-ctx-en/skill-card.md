## Description:

Save, load, verify, export, or clear a project's stable profile and incremental work snapshots so coding agents can resume context across resets, compaction, and handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckystar513](https://clawhub.ai/user/luckystar513)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to maintain project context as Markdown profiles and timestamped snapshots, then reload or export that context when resuming work or handing off to another agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project notes may be exposed or mixed across unrelated projects when fallback storage or basename-only project separation is used.

Mitigation: Prefer project-local installation and project-local storage, and avoid using init in empty directories until cross-project fallback is removed.

Risk: Generated profile rules exported to AGENTS.md may contain project-specific directives that should not be adopted blindly.

Mitigation: Review generated profile rules before keeping them or exporting them to AGENTS.md.

Risk: The optional shell hook can emit session reminder messages if enabled in Claude settings.

Mitigation: Inspect the hook script before enabling it and keep hook installation project-local when possible.

## Reference(s):

- [Wdp Ctx En ClawHub skill page](https://clawhub.ai/luckystar513/skills/wdp-ctx-en)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project profiles, timestamped snapshots, latest-snapshot pointers, AGENTS.md exports, drift reports, delete-list confirmations, and optional hook reminder messages.]

## Skill Version(s):

1.1.2 (source: server release metadata and README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
