## Description: <br>
Executes Node.js, Python, Go, and Rust code in temporary local work directories with timeouts, output limits, cleanup, and execution history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to run trusted code snippets across common runtimes while collecting execution results and basic metrics. It is best suited to controlled local workflows or hardened disposable environments, not open execution of strangers' code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local code with weak isolation and may expose files, network access, or environment secrets if used on valuable systems. <br>
Mitigation: Run only trusted code, or place the skill in a disposable VM or hardened container with secrets and network access removed. <br>
Risk: The artifact documents missing Docker isolation, memory enforcement, network isolation, and read-only filesystem controls in version 0.1.0. <br>
Mitigation: Treat the current release as a controlled local runner until stronger isolation and resource controls are implemented and reviewed. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/yuyonghao-123/yuyonghao-code-sandbox) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Testing report](artifact/TESTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JavaScript API examples, shell commands, and execution result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution results include success status, stdout, error text, exit code, execution time, and memory-used fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
