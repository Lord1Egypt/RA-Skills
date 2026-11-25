## Description:

Diagnostic skill that prints a deterministic build marker together with the runtime hostname and numeric uid, used to record which environment an agent actually executes in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bucsaradu](https://clawhub.ai/user/bucsaradu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and assessment operators use the marker to identify the runtime environment in which a command executes. The shell version also prints visible environment variable names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell version prints visible environment variable names, which may reveal runtime configuration.

Mitigation: Review the names it prints before execution; remove the listing or make it opt-in, and avoid sharing output that exposes sensitive configuration.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bucsaradu/skills/skileval-canary-48897)
- [Publisher profile](https://clawhub.ai/user/bucsaradu)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A deterministic hostname and numeric uid marker; the shell version also lists visible environment variable names.]

## Skill Version(s):

0.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
