## Description:

Full memory stack for OpenClaw on Windows. Includes LanceDB semantic memory, git-notes decision memory, and memory hygiene workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sea2049](https://clawhub.ai/user/sea2049)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this bundle to add local memory to OpenClaw on Windows, including semantic recall, git-notes decision history, and memory hygiene guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory may store and reuse sensitive user or project context without explicit user prompts.

Mitigation: Enable the bundle only when persistent local memory is intended; remove or override silent-operation rules and avoid storing secrets, credential locations, account inventories, or personal contacts.

Risk: Maintenance guidance includes destructive memory wipe commands and a monthly wipe cron example.

Mitigation: Review the exact LanceDB path before running wipe commands and do not install recurring wipe automation unless backup and reseed behavior has been approved.

Risk: Local memory quality and dependency behavior can drift over time.

Mitigation: Use a pinned virtual environment for dependencies and review Git notes and LanceDB contents regularly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sea2049/skills/vector-memory-windows)
- [Memory Hygiene Reference](https://github.com/xdylanbaker/memory-hygiene)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python code references, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory setup, retrieval, branch-aware persistence, and maintenance guidance for OpenClaw.]

## Skill Version(s):

1.0.1 (source: server release evidence, artifact/clawhub.json, and artifact release notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
