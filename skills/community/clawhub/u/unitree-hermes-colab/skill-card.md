## Description: <br>
Build or review a safety-gated Google Colab workflow that installs Hermes Agent and uses it for read-only Unitree Robotics repository analysis, simulation runbooks, log triage, and contribution planning; do not use for live robot control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to create or review a Google Colab workflow for read-only Unitree repository analysis, simulation planning, log triage, and contribution scouting. It is intended to keep robot-control actions outside Colab and make Hermes Agent execution opt-in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated notebooks or runbooks could include unsafe robot-control, DDS, ROS, SSH, SCP, tunneling, or robot-LAN actions if reviewed carelessly. <br>
Mitigation: Keep Colab outputs read-only, put risky local-host commands in quoted human-run runbooks, and run the provided artifact checker against unitree-hermes-review.json. <br>
Risk: Provider-backed Hermes execution may use optional API credentials. <br>
Mitigation: Provide OPENAI_API_KEY, OPENROUTER_API_KEY, or NOUS_API_KEY only when model-backed analysis is intended, and keep Hermes one-shot execution opt-in. <br>
Risk: The workflow may be mistaken for physical robot validation. <br>
Mitigation: Do not claim hardware validation unless the user provides external evidence, and frame live robot-control usefulness as low. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/unitree-hermes-colab) <br>
- [Project homepage](https://github.com/zack-dev-cm/unitree-g1-colab-ik) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON review gates, notebook or runner code, safety files, and validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated workflows should save unitree-hermes-report.md, unitree-hermes-review.json, AGENTS.md, and a flow visualization.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
