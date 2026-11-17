## Description:

Interactive step-by-step tutor for Solo CLI that guides a human through environment setup, robot arm calibration, teleoperation, dataset recording, and policy training.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samarthshukla6](https://clawhub.ai/user/samarthshukla6)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, robot operators, and robotics teams use this skill as a human-in-the-loop tutor for Solo CLI setup, calibration, teleoperation, dataset collection, policy training, and inference checks. It presents commands from bundled domain definitions and waits for user-confirmed validation instead of executing commands autonomously.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guided setup includes remote installer, clone, and package installation commands.

Mitigation: Review remote installer scripts and package sources before running them, avoid elevated shells unless required, and pin versions where practical.

Risk: The guided workflows involve physical robot motion during calibration, teleoperation, replay, and inference.

Mitigation: Clear the workspace, keep hands and bystanders away from the robot, and have an immediate stop or power cutoff ready before motion steps.

Risk: Optional dataset or model pushes may expose images, robot states, environment details, or credentials used in the user's own terminal.

Mitigation: Review datasets and models before publishing to HuggingFace, and enter any HuggingFace or Weights & Biases credentials directly in the user's terminal rather than sharing them with the agent.

## Reference(s):

- [Solo CLI Guide on ClawHub](https://clawhub.ai/samarthshukla6/skills/solo-cli-guide)
- [Solo CLI Documentation](https://docs.getsolo.tech)
- [Solo CLI Source Repository](https://github.com/GetSoloTech/solo-cli)
- [Solo CLI Guide Homepage](https://github.com/SoloClaw/solo_cli_guide)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and validation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are drawn from static bundled JSON domain files and presented for user execution and confirmation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
