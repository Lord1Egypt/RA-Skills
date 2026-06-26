## Description: <br>
Generates AI images with the Gitee AI API, saves them locally, and can optionally upload generated files to Tencent Cloud COS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weznai](https://clawhub.ai/user/weznai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate image assets from prompts with Gitee AI, save local PNG files, and optionally publish generated files to Tencent Cloud COS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and COS secrets may be exposed through chat, console output, or plaintext configuration files. <br>
Mitigation: Use limited-scope or disposable keys, avoid pasting real keys into chat, avoid commands that print secrets, and restrict permissions on local config files. <br>
Risk: Prompts and generated images are processed by Gitee AI and may also be uploaded to Tencent Cloud COS when upload is enabled. <br>
Mitigation: Avoid sensitive prompts or images unless that processing is acceptable, and keep COS upload disabled unless cloud storage is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/weznai/skill-image-gen) <br>
- [Gitee AI](https://ai.gitee.com/) <br>
- [Gitee AI documentation](https://ai.gitee.com/docs) <br>
- [Reference README](references/README.md) <br>
- [Gitee AI API key guide](references/GET_API_KEY.md) <br>
- [Configuration example](references/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [PNG image files with optional JSON status output and COS URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gitee AI API key; optional Tencent Cloud COS credentials enable upload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
