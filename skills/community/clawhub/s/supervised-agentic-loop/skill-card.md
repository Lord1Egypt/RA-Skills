## Description:

Supervised Agentic Loop runs autonomous Brainstorm, Plan, Implement, Review, Verify, and Evolve cycles for a target file, using metrics, git isolation, reputation scoring, and optional monitoring to keep improvements and discard regressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nefas11](https://clawhub.ai/user/nefas11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run supervised autonomous code-improvement experiments against a target file with a measurable command, while tracking results, reputation, learnings, and monitor alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous code-improvement runs can affect repository data beyond the target-file framing.

Mitigation: Run the skill only in a disposable, clean Git worktree or clone, use repository-relative target paths, and review diffs before merging any kept changes.

Risk: Target file content and command output may be provided to the configured agent or local review command.

Mitigation: Remove secrets and unrelated private files from the worktree before running the loop, and configure only trusted local agent commands.

Risk: Telegram alerts can send alert data outside the local environment when alert environment variables are set.

Mitigation: Leave Telegram variables unset unless external alerting is approved, and use an approved bot and chat destination when enabling alerts.

Risk: Git rollback and cleanup behavior can discard uncommitted or untracked files in the run worktree.

Mitigation: Start from a disposable clone or commit/back up wanted work before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nefas11/skills/supervised-agentic-loop)
- [Project source](https://github.com/Nefas11/supervised-agentic-loop)
- [governed-agents](https://github.com/Nefas11/governed-agents)
- [autoresearch](https://github.com/karpathy/autoresearch)
- [self-improving-agent](https://github.com/peterskoett/self-improving-agent)
- [openclaw-superpowers-workflow](https://github.com/Nefas11/openclaw-superpowers-workflow)
- [OpenAI agent monitoring article](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, CLI output, JSON task-result blocks, code changes, and repository state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes results.tsv and .state files; optional Telegram alerts require explicit environment variables.]

## Skill Version(s):

0.1.2 (source: server release metadata; pyproject.toml lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
