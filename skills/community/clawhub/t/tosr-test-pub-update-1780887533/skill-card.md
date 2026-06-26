## Description: <br>
Automated test skill for verifying skill creation, inspection, update, and deletion through the ClawHub REST API. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release-test agents use this skill to exercise the ClawHub skill lifecycle for a disposable test slug, including creation, inspection, version update, and cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using this skill can perform live ClawHub publish, inspect, update, and delete lifecycle actions. <br>
Mitigation: Use it only for an intended lifecycle test with test credentials and a disposable test slug. <br>
Risk: An interrupted test run can leave the ephemeral test skill visible on ClawHub. <br>
Mitigation: Confirm cleanup after the test and delete the test skill if cleanup did not complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/tosr-test-pub-update-1780887533) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls] <br>
**Output Format:** [Markdown or text instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live ClawHub publish, inspect, update, and delete lifecycle actions when used for testing.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
