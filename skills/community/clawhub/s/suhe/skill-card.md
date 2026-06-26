## Description: <br>
suhe initializes a persistent OpenClaw Agent workspace for a Suhe persona and optionally installs a selfie skill that edits a reference image with Tongyi Wanxiang and sends it through OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilozhao](https://clawhub.ai/user/lilozhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and agent developers use this skill to bootstrap a Suhe persona workspace with identity, memory, safety, metacognition, and optional AI-generated selfie messaging support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release installs a broader persistent OpenClaw persona workspace, not only a selfie generator. <br>
Mitigation: Review the workspace, docs, skill, and configuration files before installation and use a test OpenClaw profile first. <br>
Risk: The selfie workflow can send generated images or messages to external channels. <br>
Mitigation: Require explicit confirmation before sending any generated image or message outside the local environment. <br>
Risk: The skill depends on API keys and messaging gateway credentials. <br>
Mitigation: Keep credentials in environment or OpenClaw configuration, avoid pasting secrets into chats, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilozhao/suhe) <br>
- [DashScope console](https://dashscope.console.aliyun.com/) <br>
- [Tongyi Wanxiang image generation API](https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation) <br>
- [Carbon-Silicon Pact Manifesto](docs/carbon-silicon-pact.en.md) <br>
- [Group Chat Boundary Rules](docs/群聊边界规则.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JavaScript installer behavior, workspace files, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write OpenClaw workspace, docs, skill, and configuration files during installation.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
