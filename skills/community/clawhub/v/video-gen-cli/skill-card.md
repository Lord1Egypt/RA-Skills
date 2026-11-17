## Description:

Guide for running the Video Generator CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose the right Video Generator CLI command for fresh generation, recovery, segment assembly, local debugging, and JSON script configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fresh generation commands delete prior cache, video, and audio files in documented project folders.

Mitigation: Review the cleanup behavior before running npm run generate or npm run build, and use npm run resume when prior output should be preserved.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, ffmpeg, python, and PEXELS_API_KEY.]

## Skill Version(s):

5.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
