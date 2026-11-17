## Description:

故事接龙 helps users create and manage relay-style fiction with story starts, manual continuations, template-based continuations, style selection, and local story storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yansocool](https://clawhub.ai/user/yansocool)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writers use this skill to start, continue, list, view, complete, delete, and style relay-fiction projects. The artifact stores stories locally and uses built-in templates for continuation behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe local file handling may allow unintended story-file access or deletion when path-like story IDs are supplied.

Mitigation: Use only generated story IDs, run the skill in a contained non-sensitive workspace, and add story ID validation plus delete confirmation before broader deployment.

Risk: The release advertises AI continuation, image generation, and collaboration capabilities that are not fully implemented in the artifact.

Mitigation: Present current behavior as local story management with template-based continuation until real AI, image, and collaboration integrations are implemented and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yansocool/skills/story-relay)
- [ClawHub publisher profile](https://clawhub.ai/user/yansocool)
- [Project homepage from ClawHub metadata](https://github.com/openclaw/story-relay)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON files]

**Output Format:** [Console text with locally stored JSON story records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and modifies story and configuration files under its local story workspace.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
