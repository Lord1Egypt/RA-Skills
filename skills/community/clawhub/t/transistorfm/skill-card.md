## Description:

Manage Transistor.fm podcasts through the Transistor.fm API, including show and episode listing, audio upload, episode publishing, analytics, and private subscriber management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christophrumpel](https://clawhub.ai/user/christophrumpel)

### License/Terms of Use:


## Use Case:

Podcast operators and content teams use this skill to manage Transistor.fm shows and episodes from an agent workflow, including uploading audio, creating drafts, publishing or scheduling episodes, checking analytics, and managing private podcast subscribers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that publish, delete, update, or otherwise change podcast content and subscribers.

Mitigation: Require confirmation of the exact show, episode, subscriber, and action before performing publishing, deletion, update, or subscriber-management requests.

Risk: Transistor.fm API keys could be exposed through logs, shell history, or process arguments.

Mitigation: Use environment variables or a secrets manager for TRANSISTOR_API_KEY and avoid command forms that print or embed the key in logs or process arguments.

Risk: Publishing an episode can make content publicly available before it has been reviewed.

Mitigation: Create episodes as drafts first and require explicit review before publishing immediately or scheduling a release.

## Reference(s):

- [Transistor.fm API base URL](https://api.transistor.fm/v1)
- [ClawHub skill page](https://clawhub.ai/christophrumpel/skills/transistorfm)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Transistor.fm API key and may produce API request commands for podcast-changing actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
