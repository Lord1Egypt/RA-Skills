## Description: <br>
Automated integration test skill that verifies skill creation, update, inspection, and deletion via the ClawHub REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release automation maintainers use this skill to exercise the ClawHub skill lifecycle against the live REST API with an ephemeral test skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes live ClawHub lifecycle operations, including deleting a skill. <br>
Mitigation: Run it only for intentional lifecycle tests, confirm the exact slug before update or delete operations, and prefer a disposable test skill. <br>
Risk: Using production credentials could modify real ClawHub resources. <br>
Mitigation: Use a test account or scoped test credentials unless production use is deliberate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/tosr-test-skill-1778050421) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes live publish, inspect, update, and delete operations for an ephemeral ClawHub test skill.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact heading) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
