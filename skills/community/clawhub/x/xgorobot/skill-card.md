## Description: <br>
Controls XGO Mini, Lite, Mini3W, and Rider robots with scripts and library APIs for motion, actions, vision, AI features, sensors, display, and audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingyangbj](https://clawhub.ai/user/mingyangbj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robot operators use this skill to control XGO robot hardware, run packaged robot-control scripts, and draft custom Python workflows against the included XGO libraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue physical robot motion and maintenance commands, including firmware, calibration, motor unload, and long-running motion workflows. <br>
Mitigation: Use it only with trusted operators, supervised hardware, and explicit approval for maintenance or motion commands. <br>
Risk: Camera, audio, and DashScope-backed AI features may capture local data or send data to a cloud service. <br>
Mitigation: Treat camera and audio workflows as privacy-sensitive, review prompts and inputs before execution, and configure DASHSCOPE_API_KEY only in approved environments. <br>
Risk: The security summary identifies unsafe command-execution paths and risky handling of filenames, URLs, prompts, or generated speech text. <br>
Mitigation: Review every generated command before execution and avoid untrusted filenames, URLs, prompts, and generated speech text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mingyangbj/xgorobot) <br>
- [Publisher profile](https://clawhub.ai/user/mingyangbj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include robot-control commands that require a Raspberry Pi runtime, XGO hardware, serial access, and DASHSCOPE_API_KEY for AI features.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
