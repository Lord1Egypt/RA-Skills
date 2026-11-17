## Description:

Safety Programming Checklist is a guardrail skill for agents making system-level code changes, with rules, checklists, verification steps, and emergency rollback guidance learned from Hermes Desktop incidents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loodiu](https://clawhub.ai/user/loodiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a pre-flight and post-change checklist before modifying system-level desktop application code, packaging, services, registry settings, or related build artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing reference includes commands that install and invoke the ClawHub CLI.

Mitigation: Verify the CLI source, consider pinning a known version, and review the skill directory for secrets or unintended files before publishing.

Risk: System-level code changes can still cause application failures if checklist steps are skipped or applied out of order.

Mitigation: Modify source files rather than compiled output, keep a clean rollback path, use official build scripts, and verify each change batch before continuing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/loodiu/skills/safety-programming-checklist)
- [Hermes Desktop Architecture Reference](references/hermes-desktop-architecture.md)
- [ClawHub Publishing Workflow](references/clawhub-publish.md)
- [Hermes Desktop Tray Pull Request](https://github.com/NousResearch/hermes-agent/pull/63064)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown checklist guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checklist-driven safety review; the skill itself does not run hidden code or perform data exfiltration.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
