## Description: <br>
Download images, GIFs, and media from URLs using browser-like headers, Referer handling, CDN-aware scraping, and media-specific tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bstokes0971](https://clawhub.ai/user/bstokes0971) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose safe, effective commands for saving remote images, GIFs, memes, thumbnails, and social media files while avoiding common CDN and header-related download failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to retrieve remote media, including from pages that may involve private accounts or session cookies. <br>
Mitigation: Use trusted URLs, save files into a safe folder, and do not permit logged-in browser sessions, cookies, or private account pages unless the site, account, and file are explicitly approved. <br>
Risk: A failed or blocked download can save an HTML error page or text response instead of the intended media file. <br>
Mitigation: Verify the downloaded file type before relying on it and treat HTML or text output as a failed media download. <br>


## Reference(s): <br>
- [Tool Reference](references/tools.md) <br>
- [ClawHub skill page](https://clawhub.ai/bstokes0971/save-image) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference curl, gifgrep, yt-dlp, file, jq, and GIPHY_API_KEY for optional Giphy access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
