## Description:

Check the status of a ScienceClaw agent - journal stats, recent investigations, knowledge graph size, and activity summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwang108](https://clawhub.ai/user/fwang108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ScienceClaw users use this skill to inspect a local ScienceClaw agent's journal statistics, recent investigations, knowledge graph activity, and installation health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status output may reveal private research activity, including recent journal topics and active investigations.

Mitigation: Request aggregate statistics when detailed history is not needed, and review any generated summary before sharing it outside the workspace.

Risk: Running the status commands against the wrong ScienceClaw directory or agent profile may expose or summarize unintended local memory records.

Mitigation: Confirm the resolved agent name and SCIENCECLAW_DIR before running detailed journal, investigation, or graph searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fwang108/skills/scienceclaw-status)
- [Publisher profile](https://clawhub.ai/user/fwang108)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local ScienceClaw agent status, including journal counts, recent topics, active investigations, and health-check results when available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
