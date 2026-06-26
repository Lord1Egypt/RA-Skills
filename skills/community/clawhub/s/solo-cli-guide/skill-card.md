## Description: <br>
Interactive step-by-step tutor for Solo CLI that guides a human through environment setup, robot arm calibration, teleoperation, dataset recording, and policy training. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samarthshukla6](https://clawhub.ai/user/samarthshukla6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and robotics operators use this skill as a human-in-the-loop tutor for Solo CLI workflows, including setup, robot calibration, teleoperation, dataset collection, policy training, and inference. The skill presents commands from bundled domain files and waits for user-confirmed validation before proceeding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guided workflow includes teleoperation, replay, and inference commands that can move a physical robot arm. <br>
Mitigation: Before any motion step, clear the workspace, keep people away from the arm, confirm calibration and the intended follower, episode, or model, and know how to stop or power down the robot immediately. <br>
Risk: The setup flow may ask users to run remote installer, clone, or package installation commands. <br>
Mitigation: Review remote installer scripts and source-install commands before running them, and confirm upstream sources are trustworthy. <br>
Risk: Optional dataset, model, HuggingFace, and Weights & Biases workflows can expose user data or credentials if handled carelessly. <br>
Mitigation: Avoid sharing tokens in chat, enter credentials directly in the user's terminal, and inspect datasets or models before pushing them to HuggingFace or enabling W&B. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samarthshukla6/solo-cli-guide) <br>
- [Solo CLI Guide Homepage](https://github.com/SoloClaw/solo_cli_guide) <br>
- [Solo CLI Documentation](https://docs.getsolo.tech) <br>
- [Solo CLI Source Install Reference](https://github.com/GetSoloTech/solo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell commands and validation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are selected from bundled JSON action definitions and are intended for the user to run manually.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
