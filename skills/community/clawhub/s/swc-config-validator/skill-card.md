## Description:

Validate SWC config files (.swcrc, package.json#swc) for parser settings, transform conflicts, module type issues, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate .swcrc files and package.json#swc settings before relying on SWC, Next.js, or Turbopack build configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator reads local paths supplied by the user, so accidental use on the wrong file could expose unrelated local configuration content to the agent session.

Mitigation: Run it only against intended .swcrc files or package.json files that contain SWC configuration.

Risk: Static configuration findings and suggestions can be incomplete or inappropriate for a project's build constraints.

Mitigation: Review reported findings before changing build configuration, especially in strict mode or CI workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with optional text, JSON, and summary command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI-friendly exit codes; pure Python standard library validator]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
