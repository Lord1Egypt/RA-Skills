## Description: <br>
Use the rasptorch CLI to create tensors, inspect Vulkan (GPU) availability, build models, and run training. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joshua-ludolf](https://clawhub.ai/user/joshua-ludolf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate rasptorch from an OpenClaw agent, preferring JSON CLI output while creating tensors, checking Vulkan availability, managing models, and running approved training workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The rasptorch binary or Python package runs outside the skill artifact. <br>
Mitigation: Install or invoke rasptorch only from a trusted local binary or package before using the skill. <br>
Risk: Training, model save/load operations, and Streamlit UI mode can consume resources, write files, or run for a long time. <br>
Mitigation: Require explicit user approval before starting training, saving or loading model files, or launching long-running UI/chat modes. <br>
Risk: Large tensor shapes or forced GPU execution can create avoidable compute pressure or fail when Vulkan is unavailable. <br>
Mitigation: Use small tensor shapes by default and prefer --device auto unless the user explicitly requests CPU or GPU behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joshua-ludolf/rasptorch-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should prefer --json and explicit --device selection; file writes, training, Streamlit UI, and interactive chat require user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
