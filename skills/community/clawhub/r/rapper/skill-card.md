## Description:

Create and debug SenseAudio rap, hip-hop, or vocal song generation workflows using the `/v1/song/lyrics/create`, `/v1/song/lyrics/pending/:task_id`, `/v1/song/music/create`, and `/v1/song/music/pending/:task_id` APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creators use this skill to generate rap or hip-hop lyrics, create vocal songs through SenseAudio, and debug asynchronous polling and response parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill requires a SenseAudio API key and can send prompts, lyrics, and creative briefs to SenseAudio.

Mitigation: Keep the API key in an environment variable and avoid submitting private lyrics, personal data, or confidential creative briefs unless the user trusts SenseAudio's handling of that content.

Risk: SenseAudio lyric and song generation jobs may be asynchronous, pending, failed, or missing expected response data before success.

Mitigation: Poll the documented pending endpoint, require `status == SUCCESS`, surface `FAILED` clearly, and guard every response field access.

## Reference(s):

- [SenseAudio Music Reference](references/music.md)
- [SenseAudio homepage](https://nightly.senseaudio.cn)
- [ClawHub Rapper skill page](https://clawhub.ai/scikkk/skills/rapper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, curl, Python, or JavaScript examples when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SenseAudio endpoint names, minimal request bodies, polling logic, response fields, and rap-specific prompt or style guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
