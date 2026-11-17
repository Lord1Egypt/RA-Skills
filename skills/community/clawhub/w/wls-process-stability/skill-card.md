## Description:

WLS runtime engineer skill for worker lifecycle, reload versus restart decisions, process cleanup, and runtime stability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose WLS lifecycle issues, choose reload or restart behavior, preserve worker stability, and validate runtime process changes with dedicated local test instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to start local WLS test instances, which can leave processes running or conflict with the default WLS port if handled carelessly.

Mitigation: Use a unique dedicated test instance on port 9502 or higher, avoid default port 9501 for AI testing, and confirm the test instance is stopped after validation.

Risk: Runtime-sensitive worker changes can reduce responsiveness if blocking calls or blind process cleanup are introduced.

Mitigation: Keep cleanup lifecycle-aware, avoid sleep, die, and exit in runtime-sensitive code, and validate worker behavior after reload or restart.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime stability guidance should include lifecycle impact, validation steps, and cleanup confirmation.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
