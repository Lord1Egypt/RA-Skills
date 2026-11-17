## Description:

AI-powered collaborator for scientific research works. Helps draft notes, organize citations, and check the local research environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ray-778](https://clawhub.ai/user/ray-778)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and technical teams use this skill to draft structured research notes, organize citation placeholders, and confirm the local Python runtime is ready before beginning research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick-start environment check stores hostname, username, platform, and skill name in a local marker file.

Mitigation: Run the check only when local metadata capture is acceptable, review or remove ~/scientify_skill_marker.json after use, and document the stored fields for users.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local JSON marker output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional quick-start check writes a local environment marker at ~/scientify_skill_marker.json.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
