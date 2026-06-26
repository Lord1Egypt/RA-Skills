## Description: <br>
Download and archive Reddit posts including images, GIFs, and videos from specified users or subreddits with filtering and sorting options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terellison](https://clawhub.ai/user/terellison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and archive operators use this skill to collect Reddit media from a target user or subreddit, with options for sorting, date filtering, limits, and output location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader can ask yt-dlp to read local browser cookies by default for Reddit video downloads. <br>
Mitigation: Use REDDIT_COOKIES_BROWSER=none when archiving images or non-Reddit videos, or use a separate browser profile or Reddit account for downloads that require cookies. <br>
Risk: The skill installs or relies on Python packages and a video downloader that may change behavior over time. <br>
Mitigation: Pre-install and pin requests and yt-dlp versions before using the skill in repeatable or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terellison/reddit-archive) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands; execution downloads media files into Pictures and Videos directories.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses command-line options for Reddit target, sort order, date range, limit, output path, media type selection, existing-file handling, and worker count.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
