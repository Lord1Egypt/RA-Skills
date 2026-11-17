## Description:

This skill helps an agent turn a public video URL or local video file into cleaned transcription text and prompt-directed outputs such as summaries, rewrites, highlights, shot scripts, meeting notes, and translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to transcribe completed videos or audio and transform the resulting text into reusable content such as summaries, social posts, scripts, meeting minutes, and translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, prompts, task IDs, and some local path metadata are sent to a third-party service.

Mitigation: Use only videos and prompts approved for that provider; avoid regulated, confidential, or internal recordings unless the provider's retention and data-handling terms have been reviewed.

Risk: URL and file handling can send broader local or internal data to remote services than the documentation clearly scopes.

Mitigation: Provide explicit trusted local file paths or public video URLs only; avoid localhost, internal network URLs, cloud metadata addresses, and private file paths.

Risk: The skill depends on a bearer-style GUAIKEI_API_TOKEN for paid remote processing.

Mitigation: Store the token in the environment, restrict who can run the skill, rotate the token if exposed, and review expected cost before processing long videos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/video2text-ai-1-0-1)
- [Guaikei service site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or markdown-ready content on stdout, with progress and errors on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GUAIKEI_API_TOKEN environment variable; the skill can reuse the last task ID for follow-up prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
