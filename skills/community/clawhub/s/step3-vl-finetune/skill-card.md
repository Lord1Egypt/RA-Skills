## Description: <br>
Guides developers through Step3-VL-10B multimodal model LoRA or full finetuning on a GPU server, including configuration, training, inference, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunwenpinghao](https://clawhub.ai/user/hunwenpinghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to configure a Linux GPU environment, prepare training data, apply Step3-VL compatibility workarounds, and run finetuning and inference workflows for Step3-VL-10B. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Training and inference guidance includes environment variables, GPU paths, and commands that can consume GPU resources or write model adapter outputs. <br>
Mitigation: Review commands and paths before running them, execute in the intended Linux GPU environment, and validate outputs on test data before broader use. <br>
Risk: The guide includes model compatibility workarounds such as patched forward and adapter save behavior that may affect model correctness. <br>
Mitigation: Review the code changes, confirm they match the installed Step3-VL and PEFT versions, and test inference quality before relying on the resulting adapter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hunwenpinghao/step3-vl-finetune) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with code blocks, shell commands, configuration examples, and troubleshooting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Linux GPU environments with python3 and CUDA_VISIBLE_DEVICES configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
