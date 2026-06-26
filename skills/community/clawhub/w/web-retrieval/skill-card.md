## Description: <br>
Expert web fetching and crawling using Scrapling for static pages, JavaScript-rendered pages, anti-bot sites, bulk URL fetching, and site crawling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanford](https://clawhub.ai/user/seanford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve, extract, and crawl web content with static, browser-rendered, or stealth fetching modes when ordinary retrieval is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make direct network requests and crawl sites from the user's machine. <br>
Mitigation: Use it only for URLs and domains the user is allowed to access. <br>
Risk: Stealth and Cloudflare-bypass modes may be inappropriate for some sites or policies. <br>
Mitigation: Use stealth or challenge-solving modes only when explicitly appropriate for the target domain and task. <br>
Risk: Fetched content can be written to user-selected output paths and may contain sensitive data. <br>
Mitigation: Choose output paths carefully, avoid overwriting important files, and remove retained fetched content when it is no longer needed. <br>


## Reference(s): <br>
- [Web Retrieval Skill Page](https://clawhub.ai/seanford/web-retrieval) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, raw HTML, or JSON depending on command options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write fetched pages or crawl results to user-selected files and directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
