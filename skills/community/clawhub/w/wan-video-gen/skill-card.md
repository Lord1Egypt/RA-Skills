## Description: <br>
Wan Video Gen helps agents submit, poll, and download videos from Alibaba Cloud DashScope Wan text-to-video APIs using prompt, model tier, resolution, duration, and task controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouweico](https://clawhub.ai/user/zhouweico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate videos with Wan text-to-video models, check existing task status, estimate cost before submission, and download completed MP4 outputs locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill can spend DashScope credits. <br>
Mitigation: Run a dry run and review the cost estimate before submitting generation jobs, especially before increasing resolution or duration. <br>
Risk: Generated videos are saved locally by default. <br>
Mitigation: Choose an appropriate output directory and manage generated MP4 files according to local data handling requirements. <br>
Risk: DashScope API keys can be exposed if stored in config files. <br>
Mitigation: Prefer the DASHSCOPE_API_KEY environment variable; if config.json is used, keep it out of source control and restrict file access. <br>


## Reference(s): <br>
- [Wan Video Generation API Notes](references/api.md) <br>
- [Alibaba Cloud Model Studio Text-to-Video API Reference](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference) <br>
- [Alibaba Cloud Model Studio Text-to-Video Guide](https://help.aliyun.com/zh/model-studio/text-to-video-guide) <br>
- [Alibaba Cloud Model Studio Video Generation Usage](https://help.aliyun.com/zh/model-studio/use-video-generation) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhouweico/wan-video-gen) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/zhouweico) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with CLI commands, configuration examples, task identifiers, status text, cost estimates, and downloaded MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated videos are saved locally by default; task result links are documented as expiring after 24 hours.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
