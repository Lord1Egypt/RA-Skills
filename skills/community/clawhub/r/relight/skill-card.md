## Description: <br>
Relight still images on RunComfy via the runcomfy CLI, routing dedicated lighting edits to Qwen Edit 2509 Relight LoRA and broader relighting requests to identity-preserving image edit endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to relight product, portrait, landscape, and reference-matched still images through RunComfy model endpoints. It provides model-routing guidance, prompting patterns, and CLI commands for lighting direction, color temperature, intensity, and mood changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and prompts are processed by RunComfy services. <br>
Mitigation: Do not submit sensitive images or prompts unless the user is comfortable with RunComfy processing them. <br>
Risk: The skill depends on an external CLI, account authentication, and possible RunComfy costs or quotas. <br>
Mitigation: Install the official RunComfy CLI source, authenticate intentionally, and confirm account limits before running relight jobs. <br>
Risk: Relighting commands require a RunComfy token or local RunComfy configuration. <br>
Mitigation: Use RUNCOMFY_TOKEN or the documented RunComfy login flow and keep authentication material out of shared prompts, logs, and artifacts. <br>


## Reference(s): <br>
- [ClawHub Relight Skill Page](https://clawhub.ai/kalvinrv/relight) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI Documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=relight) <br>
- [Qwen Edit 2509 Relight LoRA](https://www.runcomfy.com/models/qwen/qwen-edit-2509/lora/relight?utm_source=clawhub&utm_medium=skill&utm_campaign=relight) <br>
- [Qwen Image Collection](https://www.runcomfy.com/models/collections/qwen-image?utm_source=clawhub&utm_medium=skill&utm_campaign=relight) <br>
- [Best Image Editing Models Collection](https://www.runcomfy.com/models/collections/best-image-editing-models?utm_source=clawhub&utm_medium=skill&utm_campaign=relight) <br>
- [RunComfy Trainer](https://www.runcomfy.com/trainer?utm_source=clawhub&utm_medium=skill&utm_campaign=relight) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON CLI input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI, RunComfy authentication, and configuration at ~/.config/runcomfy or RUNCOMFY_TOKEN.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
