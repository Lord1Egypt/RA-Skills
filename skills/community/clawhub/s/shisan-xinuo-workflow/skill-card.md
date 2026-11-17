## Description:

A workflow-governance skill that guides coding agents through tiered task routing, restatement, capability checks, gates, evidence capture, validation, and delivery discipline for hands-on engineering work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxc663](https://clawhub.ai/user/zxc663)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to make agent-assisted coding work auditable and disciplined across routine edits, multi-file implementation, debugging, reviews, and workflow-governed tasks. It is not intended for pure chat, read-only single-file lookup, or non-engineering conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct persistent project-level or optional global workflow-rule injection, memory files, hooks, and git setup with automatic writes.

Mitigation: Install first in on-demand or project mode, review the exact target paths and generated diffs, and require backups or rollback points before enabling hard or global injection.

Risk: Optional hooks and copied templates can affect future agent sessions if installed into platform configuration.

Mitigation: Enable hooks only after reviewing the copied script paths, platform event configuration, log location, and rollback plan; keep hooks disabled when platform support is uncertain.

Risk: The security scanner classified the release as needing review because of persistent workflow changes rather than malicious behavior.

Mitigation: Treat installation as a governance change: scan the release, prefer least-privilege placement, and confirm that the workflow's memory and rule files match local project policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zxc663/skills/shisan-xinuo-workflow)
- [Source Homepage](https://github.com/zxc663/shisan-xinuo-workflow)
- [Core Workflow Skill](SKILL.md)
- [Global Agent Workflow Core](references/injection-core.md)
- [Working Discipline Rules](references/rules.md)
- [Security and Rollback](references/security.md)
- [Platform Adaptation](references/platform-adaptation.md)
- [Skill Usage Module](references/skill-usage.md)
- [Hooks Template README](templates/hooks/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists, status lines, templates, command examples, configuration snippets, and optional file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create or maintain project memory, rule, documentation, hook, and git baseline files when the workflow is applied.]

## Skill Version(s):

1.0.20 (source: ClawHub release; artifact metadata version: 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
