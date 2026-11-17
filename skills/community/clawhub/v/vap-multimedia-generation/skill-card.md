## Description:

VAP Media API skill for image, video, music, and media editing through VAP. Uses VAP product keys with current Media API endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elestirelbilinc-sketch](https://clawhub.ai/user/elestirelbilinc-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and external agent users use this skill to generate images, videos, and music or to edit and enhance existing media through VAP Media API endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media prompts, task metadata, and referenced media URLs are sent to VAP when the skill performs generation or editing tasks.

Mitigation: Avoid confidential prompts, private signed URLs, regulated data, or sensitive media unless VAP's terms and the user's data-handling requirements allow it.

Risk: The skill requires a VAP_API_KEY for authenticated calls to VAP Media API.

Mitigation: Keep the API key in an environment variable, do not paste it into shared chat logs or generated artifacts, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elestirelbilinc-sketch/skills/vap-multimedia-generation)
- [VAP Developer Hub](https://vapagent.com/developer/)
- [VAP Media API Keys](https://vapagent.com/developer/?key=media#keys)
- [VAP AI](https://vapagent.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples, setup guidance, status summaries, and final media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a VAP_API_KEY for authenticated Media API calls.]

## Skill Version(s):

1.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
