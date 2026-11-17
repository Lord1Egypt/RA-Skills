## Description:

Tracks per-turn input and output token usage, cumulative usage statistics, budget thresholds, local history, and estimated model costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhmqq616](https://clawhub.ai/user/xhmqq616)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record token consumption, review cumulative conversation statistics, estimate costs, and receive budget warnings during normal agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default local state file can be overwritten through a predictable path or symbolic links in an untrusted working directory.

Mitigation: Review before installing in shared or untrusted directories, avoid state-changing commands where .usage-tracker.json may be planted or replaced, and back up the state file before reset.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text with JavaScript examples and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local usage history to .usage-tracker.json by default and can export statistics as JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
