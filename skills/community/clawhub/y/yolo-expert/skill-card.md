## Description: <br>
Provides YOLO and Ultralytics guidance for model loading, inference, training, validation, export, tracking, source-code lookup, and official example patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggyybb](https://clawhub.ai/user/ggyybb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for YOLO/Ultralytics API guidance, example code, shell commands, and troubleshooting while working from a local Ultralytics source checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to clone or update /root/ultralytics, changing local source state. <br>
Mitigation: Confirm before allowing git clone or git pull commands and review the target path. <br>
Risk: Training, export, tracking, and prediction examples can consume CPU, GPU, memory, and storage, and may write experiment outputs, labels, crops, or model artifacts. <br>
Mitigation: Run commands in a controlled workspace with explicit project/name paths, resource limits, and reviewed save/export options. <br>


## Reference(s): <br>
- [yolo-expert ClawHub release](https://clawhub.ai/ggyybb/yolo-expert) <br>
- [Ultralytics source repository](https://github.com/ultralytics/ultralytics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local Ultralytics source files; users should review commands before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
