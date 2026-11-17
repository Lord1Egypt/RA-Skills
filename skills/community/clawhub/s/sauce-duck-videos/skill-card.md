## Description:

Generates multilingual humorous sauce-duck meme videos by creating and monitoring a RunningHub workflow task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emwstudio](https://clawhub.ai/user/emwstudio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to request sauce-duck meme videos in a selected language. The agent gathers RunningHub host and API-key configuration, starts the video-generation task, monitors status, and returns the generated MP4 link when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RunningHub API key may be exposed through command logs, transcripts, local configuration, or process arguments.

Mitigation: Use a low-privilege RunningHub API key, keep local configuration access restricted, and rotate the key if it may have been exposed.

Risk: A misconfigured or unsafe host could receive the user's API key.

Mitigation: Confirm the host is exactly www.runninghub.cn or www.runninghub.ai before running task creation or polling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emwstudio/skills/sauce-duck-videos)
- [Publisher profile](https://clawhub.ai/user/emwstudio)
- [RunningHub China host](https://www.runninghub.cn)
- [RunningHub international host](https://www.runninghub.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Text or Markdown status messages with JSON command results and an MP4 URL when generation succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and a user-provided RunningHub API key; task completion depends on the external RunningHub service.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
