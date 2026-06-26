## Description: <br>
Fetches public WeChat Official Account articles individually or in batches and saves content, images, and metadata as Markdown, HTML, JSON, or TXT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyfan01](https://clawhub.ai/user/jackyfan01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations users can use this skill to archive WeChat Official Account articles, optionally downloading images and processing URL lists in batches. It supports low-resource request-based fetching and a Playwright mode for pages that require browser handling or cookies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests and can save third-party article content and images locally. <br>
Mitigation: Use trusted WeChat URLs, choose a dedicated output directory, and review saved content before reuse or redistribution. <br>
Risk: The Playwright mode may retain logged-in browser session data in a persistent profile. <br>
Mitigation: Prefer no-login or ephemeral-session use where possible, and clear saved browser profiles or cookies after use. <br>
Risk: The browser mode uses weakened browser security settings. <br>
Mitigation: Run the browser mode only for trusted targets and prefer the Lite mode when browser-specific handling is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackyfan01/wechat-fetch) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, guidance] <br>
**Output Format:** [Markdown, HTML, JSON, or TXT files with article metadata and optional local image assets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write article files, image folders, and batch reports to the selected output directory.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
