## Description:

Downloads YouTube videos to ~/Downloads when the user wants to save a YouTube video to their machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bestisblessed](https://clawhub.ai/user/bestisblessed)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent download a user-provided YouTube URL to the local Downloads folder using yt-dlp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads media to the local Downloads folder and creates files named from video metadata.

Mitigation: Review the URL before execution and only run the skill when local media downloads are intended.

Risk: The skill depends on the locally installed yt-dlp command.

Mitigation: Install yt-dlp from a trusted package source such as Homebrew and keep it updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bestisblessed/skills/youtube-download)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Shell command execution with terminal text and a downloaded MP4 file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp and writes downloaded media to ~/Downloads using the video title as the filename.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
