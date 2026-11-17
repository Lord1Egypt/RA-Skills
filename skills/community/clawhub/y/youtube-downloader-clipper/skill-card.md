## Description:

Clip and download specific time ranges or full YouTube videos in selected qualities, including audio-only MP3 extraction, using precise timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sandeepyadav1478](https://clawhub.ai/user/sandeepyadav1478)

### License/Terms of Use:

MIT

## Use Case:

Content creators, educators, musicians, researchers, and other external users use this skill to extract timestamped clips, audio segments, or full downloads from YouTube videos they are permitted to access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download media into the working directory.

Mitigation: Run it from a dedicated folder or sandbox and review output paths before execution.

Risk: The skill may modify the Python environment by installing dependencies.

Mitigation: Prefer preinstalling reviewed and pinned dependencies in an isolated environment.

Risk: The skill asks the agent to generate and run Python scripts from user-provided URLs, filenames, and timestamps.

Mitigation: Review generated scripts and avoid untrusted request text or filenames until the code-generation pattern is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sandeepyadav1478/skills/youtube-downloader-clipper)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash and Python code, plus generated video or audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads media into the current working directory and may modify the Python environment by installing media-processing dependencies.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
