## Description: <br>
Seedance Video Creative Studio helps an agent analyze images, expand copy, choose camera language, validate prompt quality, and generate Seedance videos through the Volcengine Ark API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghaonan777](https://clawhub.ai/user/zhanghaonan777) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, marketers, and agent users use this skill to turn images, copy, or mixed media into Chinese Seedance video prompts and, when configured with an Ark API key, submit generation jobs. It is intended for prompt creation, media-aware creative direction, and command-line video generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts and selected local media to the Volcengine Ark API. <br>
Mitigation: Require user confirmation before API generation and only submit prompts or media the user has intentionally selected for the video task. <br>
Risk: The skill depends on an ARK_API_KEY credential for generation. <br>
Mitigation: Use a scoped API key, store it outside chats and logs, and rotate or revoke it if it is exposed. <br>
Risk: Local path arguments for images, videos, audio, or downloads could expose sensitive files or write outputs to unintended locations. <br>
Mitigation: Restrict media inputs and download directories to task-specific folders; do not pass credential stores, SSH keys, browser profiles, or private documents as media paths. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhanghaonan777/seedance2-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/zhanghaonan777) <br>
- [Seedance Cinematography and Prompt Reference](reference.md) <br>
- [Volcengine Ark API Key Console](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final video prompts are required by the skill to be written in Chinese; API runs may produce task metadata, status output, URLs, and downloaded video files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
