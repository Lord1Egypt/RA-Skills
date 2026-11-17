## Description:

Converts Figma designs into frontend component code by using the `sloth d2c` CLI to fetch design data, split it into chunks, and generate final project files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cherokeeli](https://clawhub.ai/user/cherokeeli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn specified Figma file and node IDs into frontend component code. It is suited for design-to-code workflows that may target React, Vue, iOS, Taro, UniApp, Hippy, or related frontend outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can install or depend on a global npm CLI and use generated markdown to drive project file edits.

Mitigation: Install the sloth CLI from a reviewed, pinned source and run the workflow in a restricted or disposable workspace.

Risk: Figma access tokens may be required for private designs.

Mitigation: Provide tokens only when needed, scope them carefully, and avoid exposing them in logs or committed configuration.

Risk: Generated code may be incorrect, incomplete, or unsafe for the target project.

Mitigation: Review all generated diffs, run normal project checks, and build or test before committing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets, plus generated code written to project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Figma fileKey and nodeId inputs; generated diffs should be reviewed before build or commit.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
