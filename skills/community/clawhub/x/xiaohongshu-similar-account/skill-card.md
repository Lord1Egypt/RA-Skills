## Description: <br>
Helps Xiaohongshu creators, brands, MCNs, and content operators find same-tier benchmark accounts and higher-tier reference accounts from an account ID or niche, follower count, and account level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content operations teams, MCNs, and brand marketers use this skill to identify Xiaohongshu benchmark accounts, compare follower and engagement signals, and produce a recommendation report for account growth or influencer selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive RedFox API key. <br>
Mitigation: Use a low-privilege, revocable key, store it only in the environment, and avoid exposing it in code, prompts, logs, or generated files. <br>
Risk: The provided security summary flags unresolved TLS safety questions. <br>
Mitigation: Review the network code before installing and avoid running the skill until TLS verification is fixed. <br>
Risk: Daily push or subscription behavior may create recurring data delivery. <br>
Mitigation: Confirm that subscription behavior can be explicitly enabled, disabled, and deleted before using recurring pushes. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/yuanyi-github/xiaohongshu-similar-account) <br>
- [README.en.md](README.en.md) <br>
- [Account report template](references/account_template.html) <br>
- [RedFox similar-account API endpoint](https://redfox.hk/story/api/xhsUser/querySimilarAccounts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and prose with shell command snippets, a JSON status marker, and a generated HTML report path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; may create temporary JSON and HTML report files; account data may differ from real-time Xiaohongshu data.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
