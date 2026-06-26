## Description: <br>
Analyzes configured OpenClaw subagents, recommends collaboration patterns, and generates multi-agent workflow designs with safety checks for complex task decomposition and orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanlinsec-sys](https://clawhub.ai/user/nanlinsec-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze available subagent roles, choose a collaboration pattern, generate runnable workflow files, and check generated workflows against subagent safety rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates runnable multi-agent workflow code from user-provided task text. <br>
Mitigation: Review generated JavaScript and workflow JSON before execution, especially agent count, sandbox, timeout, cleanup, and unintended code. <br>
Risk: Untrusted or secret-bearing task text may be propagated into generated workflow files. <br>
Mitigation: Avoid including secrets or sensitive operational details in task prompts passed to the workflow generator. <br>
Risk: Generated files may be written to unexpected locations if output paths are implicit. <br>
Mitigation: Use explicit output paths and inspect generated workflow and report files before using them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nanlinsec-sys/subagent-collaboration) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance, terminal output, JSON workflow files, JSON security reports, and generated JavaScript workflow code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated workflow code and reports should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
