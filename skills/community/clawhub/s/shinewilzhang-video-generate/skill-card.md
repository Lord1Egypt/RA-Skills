## Description:

Generates videos from text prompts with an optional URL or local image as the first frame.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinewilzhang](https://clawhub.ai/user/shinewilzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run a video-generation script that submits a prompt, optionally includes a first-frame image, prints the generated video URL, and saves the downloaded video file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local first-frame image can be uploaded to the remote video service.

Mitigation: Use only non-sensitive first-frame files and prefer URLs or a dedicated approved asset directory.

Risk: The generated video download can overwrite user-writable files.

Mitigation: Write outputs to a dedicated directory and avoid absolute or sensitive destination paths.

Risk: Untrusted prompts or agent invocations can trigger remote video-generation requests.

Mitigation: Install and invoke the skill only in trusted workflows with appropriate service credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinewilzhang/skills/shinewilzhang-video-generate)
- [Apache License 2.0 header reference](http://www.apache.org/licenses/LICENSE-2.0)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Console text and a downloaded video file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires video service credentials through environment variables; optional first-frame local files may be uploaded to the remote service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
