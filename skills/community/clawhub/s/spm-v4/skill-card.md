## Description:

Super Project Manager v4 helps AI coding agents manage multi-step software projects with a WBS ledger, six-phase workflow, hash attestation, event audit logs, a YAML command security gate, and sub-agent prompt orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhbcher](https://clawhub.ai/user/zhbcher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use this skill to structure complex software work into tracked WBS tasks, preserve cross-session context, record verification evidence, and coordinate review or implementation subagents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local tracking files and may change project artifacts while managing work.

Mitigation: Run it in the intended working copy and review file changes before accepting them.

Risk: The implementer prompt may direct subagents to stage and commit broad changes.

Mitigation: Review or remove broad git add and commit steps, then inspect diffs before any commit.

Risk: The YAML command security gate should not be treated as a complete command sandbox.

Mitigation: Use external sandboxing or permission controls and manually review risky shell commands.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhbcher/skills/spm-v4)
- [Publisher profile](https://clawhub.ai/user/zhbcher)
- [README](artifact/README.md)
- [Architecture reference](artifact/ARCHITECTURE.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Tutorial](artifact/TUTORIAL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, templates, configuration snippets, and generated project tracking files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local WBS ledgers, attestation files, event logs, templates, and review artifacts.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
