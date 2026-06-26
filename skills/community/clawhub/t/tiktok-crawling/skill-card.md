## Description: <br>
Use for TikTok crawling, content retrieval, and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RomneyDa](https://clawhub.ai/user/RomneyDa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve TikTok videos and metadata with yt-dlp, organize profile or hashtag crawls, and export results for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to use logged-in browser cookies for TikTok, which may expose account access or session data if used broadly. <br>
Mitigation: Prefer unauthenticated runs when possible; when authentication is needed, use a separate low-privilege browser profile and delete exported cookie files afterward. <br>
Risk: Downloaded TikTok media or metadata may include sensitive content that should not be retained longer than needed. <br>
Mitigation: Store crawled content in a scoped project directory, review retention needs before sharing outputs, and delete sensitive downloads after analysis. <br>


## Reference(s): <br>
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>
- [yt-dlp output template reference](https://github.com/yt-dlp/yt-dlp#output-template) <br>
- [ClawHub skill page](https://clawhub.ai/RomneyDa/tiktok-crawling) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands for downloading media, exporting metadata as JSON or CSV, scheduling recurring crawls, and troubleshooting yt-dlp runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
