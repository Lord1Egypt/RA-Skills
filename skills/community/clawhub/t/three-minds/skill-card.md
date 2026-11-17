## Description:

Three Minds runs three Claude Code agents with different personas in a shared workspace so they can review, edit, test, and iterate on code or documents until they reach consensus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enderfga](https://clawhub.ai/user/enderfga)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to coordinate multi-perspective agent work for code review, refactoring, feature development, bug fixing, documentation improvement, research brainstorming, and paper-writing review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches coding agents with broad unattended write and command-execution authority in the selected workspace.

Mitigation: Review before installing and run it only in a disposable branch or sandboxed environment.

Risk: Child agent processes may be exposed to secrets available in the runtime environment.

Mitigation: Do not run it with cloud credentials, package tokens, SSH agent sockets, or other secrets in the environment.

Risk: The skill can leave transcripts and result files in the working directory.

Mitigation: Use non-sensitive repositories and review generated transcript or output files before sharing or committing them.

## Reference(s):

- [Three Minds ClawHub page](https://clawhub.ai/enderfga/skills/three-minds)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown transcript, optional JSON session file, and workspace file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a configurable number of collaboration rounds; the default configuration uses 15 rounds and saves a timestamped transcript in the working directory.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
