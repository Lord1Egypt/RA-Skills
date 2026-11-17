## Description:

SRS evaluates security research tasks and maps accepted work to security research, operations, knowledge-management, and exploration roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caidongyun](https://clawhub.ai/user/caidongyun)

### License/Terms of Use:

MIT-0

## Use Case:

Security researchers, SecOps teams, and developers use SRS to triage AI and security research tasks, assign suitable roles, review local research notes, and coordinate delivery handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan broad local OpenClaw, workspace, and research directories.

Mitigation: Review scan roots before use and patch the skill to require explicit, narrowly scoped scan paths.

Risk: The skill can persist TODO, capability, role, handoff, feedback, and result files in local workspace locations.

Mitigation: Run it in a reviewed workspace and require confirmation before self-improvement or coordination writes.

Risk: Task IDs, role names, and Markdown-derived content can flow into filenames or generated TODO entries.

Mitigation: Validate task IDs and role names, and escape or sanitize Markdown-derived content before writing files.

## Reference(s):

- [ClawHub Srs skill page](https://clawhub.ai/caidongyun/skills/srs)
- [OpenClaw Security Guide: Data Governance and Incident Response](artifact/reports/OpenClaw-Security-Guide-Data-Incident.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with CLI examples, JSON evaluation/status records, and local task or coordination files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist TODO, capability, role, handoff, feedback, and result files when its commands run.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
