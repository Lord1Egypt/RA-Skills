## Description: <br>
Automates WeChat Official Account draft creation from Markdown or HTML, including conversion, cover image upload, content image handling, and token-managed API publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onceyoungs](https://clawhub.ai/user/onceyoungs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to configure and run a Python helper that creates WeChat Official Account article drafts from Markdown or HTML and uploads related images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat account credentials and access tokens. <br>
Mitigation: Keep config.json and .tokens private, use credentials only for accounts intended for automation, and review access before installation. <br>
Risk: The helper can fetch remote image URLs and upload article content and images to WeChat. <br>
Mitigation: Avoid untrusted HTML, Markdown, and remote image URLs; confirm the content file, cover image, and draft action before running. <br>
Risk: Running the script can create drafts in a real WeChat Official Account. <br>
Mitigation: Confirm the selected account and inspect the resulting draft in WeChat before publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/onceyoungs/wx-mp-push) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Publishing script README](artifact/scripts/README.md) <br>
- [Configuration example](artifact/scripts/config.example.json) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON configuration, and Python script usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the helper may create a local token cache and WeChat article drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
