## Description:

A pluggable pipe filter that strips verbose CLI output before it reaches the LLM, so an agent spends its context budget on signal instead of noise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workloftai](https://clawhub.ai/user/workloftai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use slim to filter large command outputs such as YAML or JSON dumps, lockfiles, long diffs, and verbose install logs before passing them into an LLM context. It is useful when summarized head-and-tail output is acceptable and exact complete output can be rerun without slim when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large outputs can be lossy because slim may hide the middle of command output.

Mitigation: Use pipe mode only when summarized output is acceptable, and rerun the original command without slim when exact complete output is required.

Risk: The exec wrapper form runs the requested command under the agent's normal privileges.

Mitigation: Review commands before using `slim -- some-command`; prefer pipe mode when command execution is already handled elsewhere.

Risk: bench.py executes local benchmark commands when run.

Mitigation: Run bench.py only when local benchmark execution is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workloftai/skills/slim)
- [Workloft Labs](https://workloft.ai/labs)
- [lowfat inspiration](https://github.com/zdk/lowfat)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Filtered stdout text with optional stderr savings summary and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May elide the middle of large outputs with an explicit marker; --report emits estimated character and token savings.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter and clawhub.json list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
