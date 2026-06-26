## Description: <br>
Web Fetcher routes URLs to article, Feishu document, or video handlers to save fetched content locally as Markdown and media files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexxxiong](https://clawhub.ai/user/alexxxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch webpages, platform articles, Feishu documents, and videos into local Markdown, image, MP4, or MP3 files for later reading, archiving, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches arbitrary webpages, images, and videos and writes downloaded content to disk. <br>
Mitigation: Use a dedicated output directory and fetch only URLs you trust or are authorized to access. <br>
Risk: Cookie-based modes such as browser cookies, Feishu authenticated fetching, and anti-bot browser fetching can access account-scoped content. <br>
Mitigation: Enable those modes only deliberately for accounts and content you are authorized to use. <br>


## Reference(s): <br>
- [Platform Strategies](references/platforms.md) <br>
- [Adding a New Platform](references/extending.md) <br>
- [ClawHub Release Page](https://clawhub.ai/alexxxiong/web-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands] <br>
**Output Format:** [Markdown files with localized images, plus MP4 video or MP3 audio files and terminal status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written to a user-selected local directory; optional modes can skip images, choose video quality, extract audio, or use browser cookies.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
