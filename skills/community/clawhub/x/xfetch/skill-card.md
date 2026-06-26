## Description: <br>
Use xfetch CLI to fetch X/Twitter data, including tweets, user profiles, search results, timelines, lists, DMs, notifications, and exports to CSV, JSON, or SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to retrieve and export X/Twitter content through the xfetch CLI when account-authenticated social data is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct agents to use browser cookies and an external CLI to access private X/Twitter account data. <br>
Mitigation: Install only when the external xfetch CLI is trusted, use a dedicated browser profile or account where possible, and confirm before private-data commands such as DMs, bookmarks, notifications, or home timeline. <br>
Risk: Authentication cookies or tokens could expose an X/Twitter session if pasted into chat or left saved after use. <br>
Mitigation: Avoid pasting tokens into chat and clear saved authentication when finished. <br>


## Reference(s): <br>
- [ClawHub xfetch listing](https://clawhub.ai/feiskyer/xfetch) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI output/export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI can export retrieved data as JSON, JSONL, CSV, or SQLite.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
