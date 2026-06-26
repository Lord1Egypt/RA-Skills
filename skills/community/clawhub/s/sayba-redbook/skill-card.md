## Description: <br>
Search, read, analyze, and automate Xiaohongshu (小红书) content via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saybanet](https://clawhub.ai/user/saybanet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to research Xiaohongshu topics, analyze creators and viral posts, manage comments and collections, and render markdown into Xiaohongshu-ready image cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package accesses Xiaohongshu browser session cookies and may expose or misuse an authenticated account if run in the wrong browser profile. <br>
Mitigation: Use a dedicated browser profile for Xiaohongshu, avoid manual cookie strings in chat or shell history, and run `redbook whoami` before account actions. <br>
Risk: Comment, reply, batch-reply, collect, uncollect, and post commands can perform real actions on the user's Xiaohongshu account. <br>
Mitigation: Preview batch operations with `--dry-run`, review generated content before execution, and keep account-changing commands under human approval. <br>
Risk: The npm install path modifies the local Claude skills directory automatically. <br>
Mitigation: Install only in an environment where this persistence is expected, and review the created Claude skill link after installation. <br>
Risk: Xiaohongshu automation may trigger anti-bot controls, captcha, or account safety checks. <br>
Mitigation: Use conservative request rates, respect dry-run and delay controls, and stop rather than retrying when captcha or verification appears. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/saybanet/sayba-redbook) <br>
- [Publisher profile](https://clawhub.ai/user/saybanet) <br>
- [Project homepage](https://github.com/lucasygu/redbook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI-oriented guidance with optional JSON-producing shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Xiaohongshu analysis tables, reply plans, content templates, and local PNG card-rendering instructions.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
