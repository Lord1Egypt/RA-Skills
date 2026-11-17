## Description:

Helps an agent or app turn text into audio podcast episodes, where one API call creates an episode using TTS and auto-publishes it to an RSS feed subscribable in podcast apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cast0](https://clawhub.ai/user/cast0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to convert finalized text into TTS podcast episodes, poll generation status, and publish the generated MP3 through a public RSS feed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Episode text is sent to cast0 and the generated audio is published through a public podcast RSS feed.

Mitigation: Use only text that is appropriate for public distribution, and avoid submitting secrets, private personal information, or confidential business material.

Risk: The skill requires a cast0 API key for authenticated episode creation and listing.

Mitigation: Keep the API key protected in the local environment and do not expose it in shared logs, prompts, repositories, or published content.

## Reference(s):

- [cast0 API documentation](https://api.cast0.ai/docs)
- [cast0 dashboard](https://cast0.ai)
- [ClawHub skill page](https://clawhub.ai/cast0/skills/text-to-published-podcast-rss)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash commands, curl examples, endpoint tables, and RSS URL patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a cast0 API key tied to one podcast; generated episodes are published through a public RSS feed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
