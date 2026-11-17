## Description:

Manage autonomous AI research agents with SQLite-based state tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[julian1645](https://clawhub.ai/user/julian1645)

### License/Terms of Use:


## Use Case:

Developers and research operators use this skill to coordinate long-running autonomous research agents, track objectives and progress, manage handoffs, and monitor attention signals through a local SQLite-backed CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on installing an unpinned third-party CLI.

Mitigation: Install only from a trusted source, prefer a pinned release or reviewed commit, and verify provenance where possible.

Risk: Broad activation language may make the skill appear relevant to ordinary one-off research tasks.

Mitigation: Use it for deliberate long-running research-agent workflows that need project state, heartbeats, instruction queues, and oversight.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite state and append-only event logs for project tracking.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
