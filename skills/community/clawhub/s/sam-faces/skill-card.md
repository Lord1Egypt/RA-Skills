## Description:

Face recognition and identity memory for AI assistants that enrolls known people with reference photos, identifies faces in inbound images, and returns names, confidence scores, bounding boxes, and prompt-ready context using local inference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonacox-sam](https://clawhub.ai/user/jasonacox-sam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI assistant developers use this skill to add local face-identification memory to image workflows. It helps agents enroll known people, identify faces in intentionally shared images, and generate text context for downstream image descriptions or prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic face identification can identify people in shared images and create identity records without clear opt-in, retention, or cleanup controls.

Mitigation: Use in private workspaces, get consent before enrolling or identifying people, and periodically inspect and delete the faces database and unknown-crops directory.

Risk: The skill depends on a mutable PyPI package and local command execution through the sam-faces binary.

Mitigation: Review the package before installation, pin the version used for deployment, and reinstall only from trusted package sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonacox-sam/skills/sam-faces)
- [Publisher profile](https://clawhub.ai/user/jasonacox-sam)
- [Skill homepage](https://github.com/jasonacox-sam/sam-faces)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI identification responses are JSON and visualization commands produce image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include names, confidence scores, bounding boxes, an llm_context string, a local faces database, and unknown-face crop files.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
