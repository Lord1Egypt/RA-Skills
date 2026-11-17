## Description:

Fetches latest-stable Alpine Linux minirootfs release metadata and aggregates the available architectures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lentiancn](https://clawhub.ai/user/lentiancn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to retrieve public Alpine Linux latest-stable release metadata and summarize which architectures are available for automation or environment setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs Bash helper scripts that make HTTPS requests to Alpine's public release CDN and depend on local command-line tools.

Mitigation: Review the scripts before execution, run them in the expected scripts directory, and ensure curl, yq, and jq are installed from trusted sources.

## Reference(s):

- [Alpine Linux latest-stable releases](https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases)

## Skill Output:

**Output Type(s):** [Shell commands, JSON data]

**Output Format:** [JSON emitted by Bash helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, yq, and jq; fetches public release metadata over HTTPS.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
