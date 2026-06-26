## Description: <br>
Delay execution for a specified amount of time. Use for timing in scripts, waiting between operations, and scheduling delays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation authors use Sleep Tool to pause an agent workflow or script between operations, retries, and scheduled steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Duration suffixes such as minutes or hours are documented, but the bundled script accepts numeric seconds. <br>
Mitigation: Use numeric second values unless suffix parsing is implemented and tested. <br>
Risk: Large duration values can pause an agent workflow for longer than intended. <br>
Mitigation: Set bounded, intentional delays and review long waits before running the skill. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The delay duration is supplied as a single command argument; the bundled script accepts numeric seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
