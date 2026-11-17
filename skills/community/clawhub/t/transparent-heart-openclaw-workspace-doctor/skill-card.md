## Description:

Use when the user wants to inspect, repair, package, or troubleshoot an OpenClaw workspace doctor setup, especially for stale bootstrap state, missing daily memory notes, or codex-cli launch hazards in OpenClaw config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[transparent-heart](https://clawhub.ai/user/transparent-heart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose OpenClaw workspace startup drift, run workspace-local repairs, inspect missing daily memory notes, package the doctor tool, and handle known codex-cli launch hazards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable wrappers import Python code from a workspace package outside the released skill artifact.

Mitigation: Review and trust the external workspace_doctor package before running the wrappers.

Risk: The external OpenClaw config fixer can modify persistent configuration at ~/.openclaw/openclaw.json.

Mitigation: Run the check or stdout mode first, review the proposed output and backup behavior, and only allow the live write when appropriate.

Risk: Sandbox restrictions may prevent writes outside the workspace.

Mitigation: Report blocked writes clearly and do not claim the live OpenClaw configuration was fixed when the write did not occur.

## Reference(s):

- [Commands](references/commands.md)
- [Repo Layout](references/repo-layout.md)
- [ClawHub Skill Page](https://clawhub.ai/transparent-heart/skills/transparent-heart-openclaw-workspace-doctor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workspace-local fix recommendations, validation commands, and config patch guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
