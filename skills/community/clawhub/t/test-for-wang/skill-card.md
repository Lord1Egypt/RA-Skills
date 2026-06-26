## Description: <br>
Create AI-narrated film and drama commentary videos through the narrator-ai-cli workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4myhime](https://clawhub.ai/user/4myhime) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, developers, and agent users use this skill to guide an AI agent through selecting source media, narration style, background music, voice, and task parameters for narrated video production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external CLI package and Narrator AI service that require an API key. <br>
Mitigation: Install only if you trust the narrator-ai-cli package and service, use a limited API key, and keep the key out of version control. <br>
Risk: The documented workflows can upload media, delete files, run batch jobs, consume account balance, and manage account keys. <br>
Mitigation: Confirm uploads, deletions, batch jobs, costs, and key-management actions with the user before executing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/4myhime/test-for-wang) <br>
- [narrator-ai-cli package archive](https://github.com/GridLtd-ProductDev/narrator-ai-cli/archive/refs/tags/v1.0.0.zip) <br>
- [Narrator AI API endpoint](https://openapi.jieshuo.cn) <br>
- [Narrator AI resources preview](https://ceex7z9m67.feishu.cn/wiki/WLPnwBysairenFkZDbicZOfKnbc) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires narrator-ai-cli and NARRATOR_APP_KEY; uses JSON CLI output for task creation, polling, file operations, and account checks.] <br>

## Skill Version(s): <br>
0.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
