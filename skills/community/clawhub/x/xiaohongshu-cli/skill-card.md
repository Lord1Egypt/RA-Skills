## Description: <br>
Use xiaohongshu-cli for Xiaohongshu operations including search, reading, user browsing, likes, favorites, comments, follows, and posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackwener](https://clawhub.ai/user/jackwener) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to let an agent operate the xiaohongshu-cli command line tool for authenticated Xiaohongshu reading, discovery, social interaction, and creator workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse Xiaohongshu browser session cookies. <br>
Mitigation: Install only from a trusted publisher, prefer a disposable or low-risk account where possible, avoid exposing raw cookies, and run xhs logout when finished. <br>
Risk: The CLI can perform live account actions such as likes, follows, comments, posts, uploads, and deletes. <br>
Mitigation: Require explicit user confirmation before write actions and avoid delete -y in agent workflows. <br>
Risk: Aggressive automation may trigger captchas, rate limits, or account-risk controls. <br>
Mitigation: Do not parallelize requests; keep the built-in pacing behavior and pause or ask the user to complete browser verification when challenged. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackwener/xiaohongshu-cli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jackwener) <br>
- [README.md](artifact/README.md) <br>
- [Structured Output Schema](artifact/SCHEMA.md) <br>
- [PyPI project](https://pypi.org/project/xiaohongshu-cli/) <br>
- [Source repository](https://github.com/jackwener/xiaohongshu-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands can return YAML or JSON envelopes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Machine-readable command output uses an ok/schema_version/data/error envelope when --yaml or --json is selected.] <br>

## Skill Version(s): <br>
0.2.1 (source: ClawHub release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
