## Description: <br>
Automated integration test for the full ClawHub skill lifecycle: publish, inspect, update, and delete a skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test maintainers use this skill to exercise a ClawHub skill lifecycle flow, including publishing, inspecting, updating, and deleting a test skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete real ClawHub registry content if executed with credentials. <br>
Mitigation: Use a disposable test account or least-privilege token, verify the exact test slug, and require explicit approval before publish, update, or delete operations. <br>
Risk: A failed test run can leave ephemeral registry content published. <br>
Mitigation: Inspect the target skill after test runs and delete leftover test releases before reusing credentials or slugs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/tosr-test-pub-update-1776925038) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands] <br>
**Output Format:** [Markdown guidance with API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cause real ClawHub registry changes when executed with credentials.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
