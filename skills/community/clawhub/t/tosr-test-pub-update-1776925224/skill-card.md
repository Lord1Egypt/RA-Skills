## Description: <br>
Automated test skill validating creation, inspection, update, and deletion of skills via the ClawHub REST API lifecycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub lifecycle test operators use this ephemeral skill to validate publish, inspect, update, and delete behavior for a real skill release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes actions against the real ClawHub API, including update and delete operations. <br>
Mitigation: Use test credentials where possible, verify the target slug before update or delete actions, and confirm cleanup afterward. <br>
Risk: A failed lifecycle test may leave the ephemeral skill visible on ClawHub. <br>
Mitigation: Inspect the skill page after the run and remove the test skill if cleanup did not complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/tosr-test-pub-update-1776925224) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, markdown] <br>
**Output Format:** [Markdown guidance describing ClawHub REST API lifecycle operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ephemeral test skill intended to be deleted after lifecycle validation.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
