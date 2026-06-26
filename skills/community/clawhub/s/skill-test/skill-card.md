## Description: <br>
Test skills before using or publishing. Trial, compare, evaluate in isolation without affecting your environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill maintainers use this skill to test, compare, and evaluate agent skills in isolated sessions before installing or publishing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill testing can expose untrusted candidate instructions to an agent. <br>
Mitigation: Keep candidate skills in isolated sub-agent sessions and review untrusted skill text before running commands. <br>
Risk: Cleanup commands may delete the wrong path if temporary directories are changed. <br>
Mitigation: Verify temporary paths before cleanup. <br>
Risk: Comparison notes may capture sensitive task context or credentials. <br>
Mitigation: Avoid recording sensitive task context or real credentials unless the user explicitly wants that retained. <br>


## Reference(s): <br>
- [Sandbox Testing](artifact/sandbox.md) <br>
- [Comparing Skills](artifact/compare.md) <br>
- [Multi-Agent Evaluation](artifact/evaluate.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skill-test) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review prompts, comparison tables, and recommendations for skill testing workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
