## Description: <br>
Fetches Xiaohongshu (RedNote/XHS) note details and comments by note ID, returning note metadata, author information, engagement counts, tags, and paginated comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Xiaohongshu note metadata and comments visible in a user's logged-in browser session for user-authorized inspection, export, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves data from an authenticated Xiaohongshu session, which may include account-scoped content or personal profile fields visible to the logged-in user. <br>
Mitigation: Use it only for content the user is authorized to access, and review extracted data before sharing, storing, or reusing it. <br>
Risk: Server security evidence flags authenticated scraping with scaling and rate-limit avoidance guidance. <br>
Mitigation: Keep use to manual-scale retrieval from the active session; avoid bulk collection, stealth browsing, rate-limit workarounds, and collection of content the user is not authorized to gather. <br>
Risk: Comment pagination and page state may be incomplete or filtered by Xiaohongshu, so extracted comment lists may not match displayed engagement counts. <br>
Mitigation: Treat comment output as page-visible extraction rather than a complete platform record, and verify important results against the browser page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/xiaohongshu-note-detail) <br>
- [Publisher profile](https://clawhub.ai/user/browseract-cli) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-shaped extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a browser session logged in to Xiaohongshu; output may include author and commenter profile fields visible on the page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
