## Description:

Scar memory, reflex arc, and decision traces for AI agents that records failures, checks proposed actions against past scars, and exports decision data without LLM calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aibenyclaude-coder](https://clawhub.ai/user/aibenyclaude-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use tetra-scar to persist failure lessons, run local reflex checks before actions, audit repositories for common agent failure patterns, and export decision traces for later training workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository scanning and CI audit behavior may operate on a broader path set than intended.

Mitigation: Use the skill only in a sandbox or trusted repository, restrict scan paths, and review configuration before running it in CI.

Risk: Untrusted GitHub Action inputs or attacker-controlled repository contents can affect what the audit scans.

Mitigation: Pin installer and action versions, avoid passing untrusted action inputs, and do not scan repositories containing attacker-controlled symlinks.

Risk: Persistent scar, narrative, decision trace, and training-data exports can contain sensitive operational history.

Mitigation: Treat memory and exported training data as sensitive, keep them access-controlled, and redact secrets or private incident details before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aibenyclaude-coder/skills/tetra-scar)
- [Publisher profile](https://clawhub.ai/user/aibenyclaude-coder)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text, Markdown reports, JSON/JSONL files, Python API guidance, shell commands, and GitHub Action configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSONL memory and optional training-data exports; the CI action emits score, grade, findings, and a step summary.]

## Skill Version(s):

0.4.0 (source: server release evidence; artifact frontmatter reports 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
