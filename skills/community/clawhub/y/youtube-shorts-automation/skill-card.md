## Description: <br>
YouTube Shorts 자동 생성 및 업로드 파이프라인. Deevid AI Agent로 이미지→영상(BGM+음성 포함) 생성 후 YouTube에 업로드. 크론잡으로 매일 자동 실행 가능. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangjjang](https://clawhub.ai/user/kangjjang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate short-form vertical videos with Deevid AI Agent, download the rendered media, and upload it to YouTube Shorts. It also provides configuration guidance for repeatable channel-specific posting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The upload flow can publish videos publicly even when a non-public privacy option is selected. <br>
Mitigation: Review and fix the upload script's privacy handling before enabling automated uploads or cron jobs. <br>
Risk: OAuth credential files such as client_secret.json and token.json grant access to YouTube upload capabilities. <br>
Mitigation: Protect credential files, limit access to the execution environment, and rotate credentials if they are exposed. <br>
Risk: Automated uploads can affect a live YouTube channel without additional human review. <br>
Mitigation: Test with a dedicated YouTube channel and require manual review before connecting the workflow to production channels. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kangjjang/youtube-shorts-automation) <br>
- [Config Example](references/config_example.json) <br>
- [Deevid Agent Video Workflow](references/deevid-agent-workflow.md) <br>
- [YouTube Shorts Upload](references/youtube-upload.md) <br>
- [Deevid AI Agent](https://deevid.ai/ko/agent) <br>
- [YouTube Upload OAuth Scope](https://www.googleapis.com/auth/youtube.upload) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OAuth setup steps, Deevid workflow instructions, YouTube upload commands, and channel-specific configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
