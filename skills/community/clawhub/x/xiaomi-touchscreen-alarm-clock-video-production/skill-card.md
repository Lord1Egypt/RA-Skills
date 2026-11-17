## Description:

B站视频下载裁剪压缩工具。下载bilibili视频、裁剪去除边框、压缩到指定大小时使用。支持b23.tv短链和BV号。别名：闹钟视频下载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mimose101](https://clawhub.ai/user/mimose101)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through downloading Bilibili videos, resolving b23.tv short links, cropping video borders, trimming lead-in and end segments, and compressing output for a Xiaomi touchscreen alarm clock workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can modify the user's Python environment.

Mitigation: Install dependencies in a dedicated virtual environment and avoid --break-system-packages.

Risk: ffmpeg commands use overwrite mode and repeated runs for the same BV ID can replace previous outputs.

Mitigation: Choose output filenames and directories carefully, keep BV-based unique filenames, and check for existing files before rerunning processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mimose101/skills/xiaomi-touchscreen-alarm-clock-video-production)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, parameter tables, and bitrate formulas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include yt-dlp, bilix, ffmpeg, ffprobe, curl, and Python command examples for local media processing.]

## Skill Version(s):

1.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
