## Description:

Generates cooking inspiration from a refrigerator photo by using Wan/DashScope vision and generation models to identify ingredients, create a polished dish image or video, and produce a detailed recipe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laojun509](https://clawhub.ai/user/laojun509)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn fridge photos into meal ideas, generated food media, and Chinese recipe guidance across many cuisine styles, difficulty levels, and cooking-time targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads private refrigerator photos and prompts to cloud AI services.

Mitigation: Use only non-sensitive photos and avoid images that show medications, identifying labels, or other private household details.

Risk: API credentials and image data are sent to configurable cloud endpoints.

Mitigation: Use a dedicated DashScope API key with limited quota and do not set WAN_API_URL to an untrusted or unknown host.

Risk: The security review flags insufficient scoping and privacy disclosure.

Mitigation: Review the skill before installing, run it in a clean virtual environment, and confirm that its cloud-service behavior is acceptable for the intended users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laojun509/skills/pure-wan-fridge-gourmet)
- [Publisher profile](https://clawhub.ai/user/laojun509)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text and Markdown-style recipe output, with optional JSON result files and generated image or video URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include a media URL, task ID, cuisine, difficulty, cooking-time metadata, recipe source, ingredients, cooking steps, and tips.]

## Skill Version(s):

3.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
