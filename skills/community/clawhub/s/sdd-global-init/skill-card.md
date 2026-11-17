## Description:

Initializes an SDD workspace by selecting a workspace directory, scanning projects, and generating global specification documents for project overview, architecture, constraints, features, and indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to bootstrap Chinese SDD documentation for a selected workspace, including global project overview, architecture, feature inventory, constraints, and supporting diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans the selected workspace and may encounter unrelated sensitive project files if the chosen directory is too broad.

Mitigation: Choose a constrained workspace that excludes unrelated sensitive files, and review the generated outline before confirming document generation.

Risk: Diagram prompts may include project architecture or metadata when the image-generation step is used.

Mitigation: Review diagram descriptions before generation and avoid including confidential implementation details in generated image prompts.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files, JSON workspace configuration, and concise Chinese status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates documentation under spec/global/ after user outline confirmation and may request image generation for diagrams.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
