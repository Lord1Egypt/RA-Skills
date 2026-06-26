## Description: <br>
Enables an AI agent to search Xiaohongshu content, publish and delete notes, query users, manage comments, and read the home feed through a Python CLI. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[OSSKn4w7](https://clawhub.ai/user/OSSKn4w7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let an OpenClaw-style agent perform Xiaohongshu research, note publishing, deletion, user lookup, comment, and feed operations. The artifact documentation limits the intended use to learning, testing, and research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a full Xiaohongshu account session, including publishing, deleting, and commenting. <br>
Mitigation: Use a test account where possible and require manual approval before any publish, delete, or comment command. <br>
Risk: The Xiaohongshu cookie grants account access and may expose the account if stored or shared insecurely. <br>
Mitigation: Keep the cookie private, prefer environment-based storage, avoid plaintext cookie files, and rotate the cookie if exposure is suspected. <br>
Risk: Automated or frequent actions may trigger Xiaohongshu risk controls, account restrictions, or bans. <br>
Mitigation: Keep usage low volume, add delays between operations, and stop automation if the account receives warnings or verification challenges. <br>


## Reference(s): <br>
- [Xiaohongshu website](https://www.xiaohongshu.com) <br>
- [xhs-python-sdk](https://github.com/leeguooooo/xhs-python-sdk) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, pip, xhs, click, and a Xiaohongshu account cookie supplied through environment or local configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
