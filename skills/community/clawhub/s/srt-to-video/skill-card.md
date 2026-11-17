## Description:

Convert SRT subtitle files into Remotion typing-animation videos with character-by-character text reveal and cinematic animated backgrounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x00000003](https://clawhub.ai/user/0x00000003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to convert standard SRT subtitle files into a Remotion React project that renders timed typewriter-style subtitle videos with animated backgrounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The template installs Remotion packages with confirmed critical security advisories.

Mitigation: Update remotion, @remotion/cli, and related Remotion packages to 4.0.410 or newer, regenerate the lockfile, and run npm audit before installation or rendering.

Risk: Untrusted SRT files are used to generate and render a local video project.

Mitigation: Review SRT input before use and render in a contained project directory with only the files needed for the job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0x00000003/skills/srt-to-video)
- [Publisher profile](https://clawhub.ai/user/0x00000003)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript and JSON project files plus shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Remotion project scaffold for rendering an MP4 video from SRT subtitle timing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
