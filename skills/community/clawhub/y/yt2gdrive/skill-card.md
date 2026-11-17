## Description:

Sync latest audio or video (mp3/mp4) from YouTube channels to Google Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangoal2019](https://clawhub.ai/user/yangoal2019)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure an agent-assisted workflow that downloads recent YouTube channel media as MP3 or MP4 files and uploads the results to a configured Google Drive remote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says dry-run mode is misleading and can still download files and perform local cleanup.

Mitigation: Review the script before use, run it first with a disposable LOCAL_DIR, and use --keep-local when local cleanup is not desired.

Risk: The skill downloads YouTube media and uploads it to the configured Google Drive remote.

Mitigation: Use only with channels and Drive destinations you are authorized to access, and verify REMOTE_NAME, REMOTE_PATH, CHANNELS_FILE, and archive settings before execution.

Risk: The optional launchd installer creates a daily macOS scheduled task.

Mitigation: Install the LaunchAgent only after reviewing the generated schedule and script path, and unload it when automated syncing is no longer needed.

## Reference(s):

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [rclone](https://rclone.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to local shell scripts, environment variables, channel configuration files, rclone remotes, and optional macOS launchd scheduling.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
