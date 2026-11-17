## Description:

Download and archive Reddit posts, including images, GIFs, and videos, from specified users or subreddits with filtering and sorting options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terellison](https://clawhub.ai/user/terellison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to archive public Reddit media from a chosen user or subreddit into local image and video folders. It supports sorting, date filtering, limits, and output-directory selection for targeted archive runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video downloads may cause yt-dlp to read cookies from a logged-in browser session.

Mitigation: Set REDDIT_COOKIES_BROWSER=none unless authenticated Reddit video downloads are required.

Risk: Automatic dependency installation can modify the user's Python environment.

Mitigation: Install pinned dependencies in an isolated environment before running the script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terellison/skills/reddit-archive)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [old.reddit.com](https://old.reddit.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Command-line status text and downloaded media files organized into local folders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Pictures and Videos subdirectories under the selected output directory.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
