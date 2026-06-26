## Description: <br>
X Platform API. Read posts, search tweets, post, upload media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to connect an agent to the X Platform API for reading posts, searching recent tweets, managing bookmarks, posting tweets, deleting tweets, and uploading media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate a real X account, including posting, deleting, bookmarking, and uploading media. <br>
Mitigation: Use read-only bearer credentials unless write access is required, keep OAuth tokens least-privileged, and require human approval before post, delete, bookmark, or upload actions. <br>
Risk: The media upload path can upload local files supplied to the agent. <br>
Mitigation: Only pass media file paths that have been explicitly reviewed and approved for upload. <br>


## Reference(s): <br>
- [X API v2](https://docs.x.com/x-api) <br>
- [X API authentication](https://docs.x.com/resources/authentication) <br>
- [X API base URL](https://api.x.com/2) <br>
- [@xdevplatform/xdk SDK](https://github.com/xdevplatform/xdk) <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-x) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, shell commands, configuration snippets, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read X account data and perform account-changing X actions when OAuth credentials are available.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, package.json, CHANGELOG released 2026-02-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
