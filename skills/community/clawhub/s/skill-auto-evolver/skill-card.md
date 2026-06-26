## Description: <br>
Skill Auto Evolver monitors OpenClaw Agent Skill usage, analyzes skill health and code quality, and generates improvement reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to monitor local OpenClaw skills, evaluate health across reliability, performance, code quality, and feedback, and generate recommendations and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local usage logs, feedback comments, user IDs, context, and error messages may contain secrets or personal data. <br>
Mitigation: Limit the skill directories it inspects, avoid recording secrets or personal data, and review exported reports before sharing them. <br>
Risk: Cleanup commands delete old local usage and feedback history. <br>
Mitigation: Confirm retention needs and export any needed reports before running cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skill-auto-evolver) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples and report exports in JSON, Markdown, or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local SQLite-backed monitoring data and generated reports.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
