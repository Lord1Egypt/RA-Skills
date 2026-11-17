## Description:

Toon helps agents compress JSON command output into TOON format for lower token use while passing non-JSON output through unchanged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonk-moltbot](https://clawhub.ai/user/bonk-moltbot)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill when fetching API responses, reading JSON files, or handling structured command output that should be compressed before being added to context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references a scripts/toon executable that is not included in the release evidence.

Mitigation: Confirm the actual toon script or npm package source before installing it or piping sensitive data through the selected local CLI implementation.

## Reference(s):

- [TOON format specification](https://toonformat.dev)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and TOON-formatted text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and a local toon CLI implementation; non-JSON input is documented as passing through unchanged.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
