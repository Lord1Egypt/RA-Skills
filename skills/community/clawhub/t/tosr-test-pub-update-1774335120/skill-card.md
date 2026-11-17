## Description:

Professional code review and Git commit workflow management for commit and push operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code changes, prepare Chinese conventional commit messages, run build checks, and coordinate Git pull and push workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports contradictory behavior: the skill says Git actions require user approval but also instructs the agent to automatically stage and commit existing changes.

Mitigation: Require explicit approval of exact files and commit message before staging or committing, or remove the automatic commit step before installation.

Risk: The skill can guide Git operations that affect repository history or publish local work.

Mitigation: Review proposed Git commands, changed files, build output, and remote target before allowing commit or push actions.

## Reference(s):

- [API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Git staging, commit, build, pull, and push commands for user approval.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
