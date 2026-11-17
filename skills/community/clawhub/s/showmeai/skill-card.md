## Description:

Generate and edit images, create videos, convert images to 3D, synthesize speech or music, and process images through ShowMeAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hulebaji](https://clawhub.ai/user/hulebaji)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route creative-media requests through ShowMeAI, configure model defaults, run generation or processing commands, and recover long-running tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected local media are sent to the configured ShowMeAI endpoint.

Mitigation: Avoid sensitive media unless sharing it with the service is acceptable, and review the endpoint and account policy before use.

Risk: Credential-handling weaknesses could expose a ShowMeAI API key to unintended hosts.

Mitigation: Use the documented hidden-input or standard-input setup flow, avoid custom API base URLs, and rotate the key if exposure is suspected.

## Reference(s):

- [ShowMeAI API](https://api.showmeai.art)
- [ShowMeAI API Documentation](https://showmeai.apifox.cn)
- [Configuration and credentials](references/configuration.md)
- [Image models and parameters](references/image.md)
- [Video workflow](references/video.md)
- [3D workflow](references/three-d.md)
- [Speech and music](references/audio.md)
- [Polling and recovery](references/polling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON command results, and local media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful media outputs are downloaded locally and emitted as file paths; long-running tasks can be journaled and resumed.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
