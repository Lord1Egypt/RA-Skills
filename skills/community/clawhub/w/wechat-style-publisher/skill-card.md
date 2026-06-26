## Description: <br>
Supports publishing styled articles to one or more WeChat Official Accounts with per-account credentials, custom themes, and optional intro and outro templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[web3aivc](https://clawhub.ai/user/web3aivc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to prepare themed HTML articles, manage multi-account WeChat publishing configuration, import reusable templates from existing articles, and create WeChat draft articles with uploaded local media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WeChat account credentials and cache access tokens locally. <br>
Mitigation: Keep app secrets and the token cache out of shared folders and version control, and use least-privileged WeChat credentials. <br>
Risk: The publishing scripts can upload local images and create WeChat draft content for one or more configured accounts. <br>
Mitigation: Verify the selected accounts, article HTML, template content, and local image paths before running a publish command. <br>
Risk: Template import can fetch and process article HTML from a URL. <br>
Mitigation: Import templates only from trusted sources, or inspect imported HTML before reusing it in published articles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/web3aivc/wechat-style-publisher) <br>
- [WeChat API base endpoint](https://api.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, HTML, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and styled HTML article output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local configuration, token cache, template registry, styled HTML files, and WeChat draft or media records depending on the selected script.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
