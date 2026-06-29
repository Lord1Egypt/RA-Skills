## Description: <br>
Automated integration test skill to verify publishing, updating, and deleting skills via the ClawHub REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release automation maintainers use this skill to verify ClawHub skill lifecycle operations, including publish, inspect, update, and delete flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes live API operations that can publish, update, or delete real ClawHub skill resources. <br>
Mitigation: Verify the target account, project, slug, and resource ID before state-changing calls, and use dry-run or confirmation steps where available. <br>
Risk: A failed lifecycle test can leave an ephemeral test skill visible on ClawHub. <br>
Mitigation: Check cleanup results after test runs and delete stale test releases when cleanup does not complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/tosr-test-pub-update-1781598090) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with REST API operation descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing API operations should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
