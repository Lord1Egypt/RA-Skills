## Description:

Run quick health checks on the workspace: skill loadability, evolver version/status, git state, and a summary of failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check whether workspace skills load, whether Evolver responds, and how many files Git reports as dirty before running workspace workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was limited: only 2 of 4 components were fully inspected, and tool-misuse analysis was degraded.

Mitigation: Review the skill details and install only if they match what you expect.

Risk: Checking skill loadability requires each discovered skills/<name>/index.js module, which can run that module's code.

Mitigation: Run the check only in a trusted workspace and review the modules it will load.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/147258xuan/skills/workspace-smoke-test)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON summary or human-readable terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports skill check counts and failures, Evolver status, Git dirty-file count, and a timestamp.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
