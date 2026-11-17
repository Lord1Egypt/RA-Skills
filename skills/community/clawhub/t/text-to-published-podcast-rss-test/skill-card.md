## Description:

Helps an agent or app turn text into audio podcast episodes; one API call creates an episode using TTS and auto-publishes it to an RSS feed subscribable in podcast apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cast0](https://clawhub.ai/user/cast0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create podcast episodes from supplied text, poll generation status, list episodes, and publish completed audio through a public RSS feed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied text is sent to cast0.ai and auto-published as podcast audio through a public RSS feed.

Mitigation: Confirm the episode text is intended for public publication before creating an episode.

Risk: The skill uses CAST0_API_KEY credentials to create and manage episodes.

Mitigation: Store the API key securely and avoid committing it to source control.

## Reference(s):

- [cast0 API Documentation](https://api.cast0.ai/docs)
- [cast0 Dashboard](https://cast0.ai)
- [ClawHub Skill Page](https://clawhub.ai/cast0/skills/text-to-published-podcast-rss-test)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with API examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a cast0 API key tied to one podcast; episode generation is asynchronous.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
