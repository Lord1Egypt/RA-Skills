## Description: <br>
Autonomous executor for Solo CLI that runs setup, calibration, teleoperation, dataset recording, policy training, and inference commands in the user's terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samarthshukla6](https://clawhub.ai/user/samarthshukla6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robot operators use this skill to have an agent execute Solo CLI workflows for local setup, robot calibration, teleoperation, dataset capture, policy training, replay, diagnostics, and inference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run shell commands and control attached robot hardware. <br>
Mitigation: Install only when the user intends agent-driven Solo CLI execution, stay physically present, keep the robot workspace clear, and review displayed commands before execution. <br>
Risk: Parameterized command values such as names, paths, and tasks may be unsafe if they contain shell-special characters. <br>
Mitigation: Use simple names and paths without shell metacharacters and review full commands before terminal execution. <br>
Risk: Dataset or model workflows can upload to external services when push or logging options are enabled. <br>
Mitigation: Prefer local-only workflows unless upload is intended, and use least-privilege HuggingFace and Weights & Biases credentials. <br>
Risk: Several high-impact robot actions depend on user observation rather than scanner-verifiable outcomes. <br>
Mitigation: Require physical confirmation that robot movement, calibration, replay, teleoperation, or inference completed correctly before treating the action as successful. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samarthshukla6/solo-impl) <br>
- [Solo CLI documentation](https://docs.getsolo.tech) <br>
- [Solo-claw project homepage](https://github.com/GetSoloTech/Solo-claw) <br>
- [solo-cli source repository](https://github.com/GetSoloTech/solo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown status updates with inline shell commands and terminal execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open terminal windows for interactive robot workflows and may use conditional HuggingFace or Weights & Biases credentials when the selected workflow requires them.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
