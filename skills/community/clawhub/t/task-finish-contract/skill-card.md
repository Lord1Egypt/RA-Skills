## Description:

Enforce task completion with explicit Goal/Progress/Next state. Prevent mid-task stalls and ensure evidence-based completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers, agent operators, and teams using multi-step agent workflows use this skill to require explicit task state, completion proof, and evidence before an agent considers work finished.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The privacy checklist includes a local scan command that can print secrets or sensitive matches into logs.

Mitigation: Configure scans to show only filenames or redacted matches, and avoid recording raw secret-scan output in task logs, memory files, or completion evidence.

Risk: A broad process skill can influence many agent workflows and may cause agents to over-collect evidence.

Mitigation: Keep completion evidence limited to relative paths, workspace artifacts, command summaries, and redacted verification results.

## Reference(s):

- [Privacy Checklist](references/privacy-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/dalomeve/skills/task-finish-contract)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with checklist, evidence, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill prompts agents to produce concise task-state updates, completion checklists, evidence summaries, and verification commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
