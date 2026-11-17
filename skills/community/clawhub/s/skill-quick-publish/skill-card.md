## Description:

Automates publishing a skill by coordinating duplicate checks, optional Bear notes sync, GitHub push, and ClawHub publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this agent skill to publish new or updated skills to ClawHub and, when configured, push the skill files to a GitHub repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing workflow can push files to GitHub and publish a skill to ClawHub, which may expose unintended content if used against the wrong directory or repository.

Mitigation: Review the skill directory for private files, run with --dry-run first, and confirm the target GitHub repository, branch, version, and changelog before allowing external release steps.

Risk: A user may not intend to run every external publication step.

Mitigation: Use --skip-github when a GitHub push is not intended, and avoid running the final publish path when the release should remain local.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and option descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a command-oriented publishing workflow; dry-run mode can preview actions before external release steps run.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
