## Description:

Clusters repeated tool and request failures from the current session by tool, host, and error signature, identifies a dominant cause when present, and returns a compact failure trail with an action recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill after three or more repeated failures in a session to diagnose the dominant failure pattern before retrying. It helps decide whether to fix the dominant cause, vary one input, or report that no tool failures were found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the ClawPhylax plugin, which keeps a persistent local ledger of tool and request outcomes.

Mitigation: Review the ClawPhylax plugin before enabling it and treat local-runtime privacy claims as plugin behavior, not as installation behavior.

Risk: Failure diagnosis can be misleading when the local ledger is unavailable or incomplete.

Mitigation: Proceed without the plugin only after saying what could not be verified, and avoid over-interpreting sparse failure data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/why-do-i-keep-failing)
- [Publisher profile](https://clawhub.ai/user/aeneassoft)
- [Declared project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with an action label, clustered failures, and a compact failure trail]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports one dominant cause when present; uses ClawPhylax failure data when the plugin is available.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
