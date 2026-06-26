## Description: <br>
Automated test skill for verifying ClawHub skill creation, inspection, update, and deletion workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub release testers and maintainers use this skill to exercise skill publish, inspect, update, and delete workflows for an ephemeral test release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes publish, update, and delete lifecycle operations that can affect real ClawHub accounts or releases if run with production credentials. <br>
Mitigation: Use a disposable test account and test slug, avoid normal production credentials, and require confirmation before publish, update, or delete actions. <br>
Risk: The skill is intended to be ephemeral and may remain listed if a test run fails to clean up. <br>
Mitigation: Inspect the test release after runs and delete it before reuse when cleanup fails. <br>


## Reference(s): <br>
- [Published skill page](https://clawhub.ai/yinwuzhe/tosr-test-skill-1778050437) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code files; behavior is described in a single markdown skill file.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
