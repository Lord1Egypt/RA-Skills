## Description: <br>
Validates documentation usability by spawning context-free agents to complete tasks using only the docs, identifying gaps for improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zscole](https://clawhub.ai/user/zscole) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to test whether setup guides, READMEs, tutorials, and other docs are sufficient for a fresh agent to complete a task without outside context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may spawn a separate tester agent session to evaluate documentation. <br>
Mitigation: Run it only on documentation intended for testing and review generated gap reports before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zscole/rtfm-testing) <br>
- [TESTER.md](artifact/TESTER.md) <br>
- [GAPS.md](artifact/GAPS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown gap reports and documentation quality summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports task attempted, provided documentation, execution log, gaps found, result, and summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
