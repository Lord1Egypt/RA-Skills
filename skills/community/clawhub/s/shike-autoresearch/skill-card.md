## Description:

CPU-based autonomous optimization loop for skill quality improvement that runs experiments, evaluates results, and keeps improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjj2026](https://clawhub.ai/user/sjj2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to run a local, checkpointed optimization loop over experiments for skill packages, strategy backtests, or content-creation tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through local experiments, proposed file edits, result logging, commits, and reverts in the working directory.

Mitigation: Install it only in repositories where that workflow is acceptable, and review diffs at the documented checkpoints before allowing experiment runs, commits, or reverts.

## Reference(s):

- [Karpathy autoresearch](https://github.com/karpathy/autoresearch)
- [OpenClaw Skills](https://github.com/openclaw/skills)
- [ClawHub skill page](https://clawhub.ai/sjj2026/skills/shike-autoresearch)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file edits, experiment runs, result logging, commits, or reverts behind user-confirmable checkpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
