## Description: <br>
Xhs Expert helps agents search Xiaohongshu notes, collect note and comment data, analyze content trends, and prepare or run account interactions such as likes, comments, saves, follows, and batch actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mieming1985](https://clawhub.ai/user/mieming1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to route Xiaohongshu search, data collection, account status, and interaction requests into the bundled xhs CLI. It supports content discovery, note detail retrieval, comment collection, local data statistics, and confirmed social actions through a logged-in account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Xiaohongshu account for likes, comments, saves, follows, and batch actions. <br>
Mitigation: Use a separate account or profile and manually confirm every comment, follow, and batch action before execution. <br>
Risk: The skill stores session cookies and account state locally under the Xiaohongshu configuration directory. <br>
Mitigation: Protect the local profile directory, limit machine access, and delete ~/.config/xiaohongshu when the account should no longer be available to the skill. <br>
Risk: Stealth browser automation or bulk engagement may violate platform rules or trigger account enforcement. <br>
Mitigation: Install only when this automation is intentional, keep action volume low, and review Xiaohongshu platform rules before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mieming1985/xhs-expert) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>
- [Xiaohongshu web API base](https://edith.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown guidance with inline CLI commands, terminal text, and optional JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on local login state, saved cookies, Xiaohongshu API responses, and user confirmation for sensitive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
