## Description:

Stop guessing what your AI costs. Tinker shows every token, every dollar, every context byte, in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install or assess a local OpenClaw dashboard for monitoring token usage, context size, response cost, and budget status during agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation relies on an unpinned third-party GitHub fork whose code was not included in the reviewed artifact.

Mitigation: Use a pinned reviewed commit, verified checksum or signed release, and audit package scripts and the lockfile before installation.

Risk: The dashboard connects to local OpenClaw sessions and may expose conversation or context data to the installed fork code.

Mitigation: Run it only in an isolated environment and avoid connecting it to sensitive sessions or credentials unless the fork has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/tinker-command-center)
- [TinkerClaw repository referenced by the artifact](https://github.com/globalcaos/tinkerclaw)
- [ClawHub publisher profile](https://clawhub.ai/user/globalcaos)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents toward a local dashboard setup that requires node and pnpm.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
