## Description: <br>
Clips web pages into Youdao Note, including browser-extracted pages, supported Chinese content sites, and Twitter/X status URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lephix](https://clawhub.ai/user/lephix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to save web articles, rendered pages, and selected Twitter/X posts into Youdao Note with titles, source URLs, text, and images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read rendered browser page content and save it to Youdao Note, including sensitive pages if invoked there. <br>
Mitigation: Use it only on pages intended to be clipped, and avoid AI chat sessions, private dashboards, or pages containing secrets unless the captured content has been reviewed. <br>
Risk: Twitter/X clipping sends the target URL to Apify and uses APIFY_API_TOKEN, which is not declared in the manifest. <br>
Mitigation: Configure Apify access deliberately and avoid Twitter/X clipping when third-party processing of the URL is not acceptable; declare the token before managed deployment. <br>
Risk: Browser extraction injects local parsing code into target pages to read the page title, content, and image URLs. <br>
Mitigation: Run it in a browser profile appropriate for clipping and review the skill source before using it on authenticated or sensitive pages. <br>


## Reference(s): <br>
- [YoudaoNote Clip on ClawHub](https://clawhub.ai/lephix/youdaonote-clip) <br>
- [lephix publisher profile](https://clawhub.ai/user/lephix) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown status response with command-driven clipping and JSON metadata files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YOUDAONOTE_API_KEY; Twitter/X clipping also uses APIFY_API_TOKEN even though it is not declared in the manifest.] <br>

## Skill Version(s): <br>
1.21.8 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
