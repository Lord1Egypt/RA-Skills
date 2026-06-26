## Description: <br>
Fetch, summarize, and manage X/Twitter bookmarks via bird CLI or X API v2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharbelayy](https://clawhub.ai/user/sharbelayy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and their AI agents use this skill to fetch private X/Twitter bookmarks, organize them into digests, identify patterns, propose follow-up actions, and optionally set up recurring bookmark reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to private X/Twitter bookmarks and sensitive authentication material. <br>
Mitigation: Use a read-only OAuth app where possible, protect .env.bird and ~/.config/x-bookmarks files, and revoke tokens when the skill is no longer needed. <br>
Risk: OAuth scopes include bookmark.write and the skill can support unbookmarking despite a primarily read-oriented workflow. <br>
Mitigation: Confirm write-capable access before authorization and use unbookmarking only after explicit user approval. <br>
Risk: Printing access tokens can expose credentials in terminal logs or shell history. <br>
Mitigation: Avoid --print-token in logged terminals and rotate credentials if a token is displayed or copied insecurely. <br>
Risk: The bird CLI path can read browser cookies from a logged-in X session. <br>
Mitigation: Verify the bird CLI installation before use and prefer OAuth if browser-cookie access is not acceptable. <br>
Risk: Scheduled digest workflows can repeatedly access private bookmarks. <br>
Mitigation: Enable cron digests only after confirming the schedule, stored state location, and how to disable the job. <br>


## Reference(s): <br>
- [X Bookmarks auth setup](references/auth-setup.md) <br>
- [X API v2](https://api.x.com/2) <br>
- [X Developer Console](https://developer.x.com/en/portal/petition/essential/basic-info) <br>
- [ClawHub listing](https://clawhub.ai/sharbelayy/x-bookmarks) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON bookmark data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local bookmark state and OAuth token/config files when the user enables those workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
