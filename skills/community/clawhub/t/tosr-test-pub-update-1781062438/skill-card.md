## Description: <br>
Automates testing of the ClawHub skill lifecycle by publishing, inspecting, updating, and deleting a skill through the ClawHub REST API. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to exercise ClawHub skill lifecycle API flows in controlled test accounts, including publish, inspect, update, and delete operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Following the skill may create, update, inspect, and delete skills through the real ClawHub API. <br>
Mitigation: Use it only in a controlled test account or workspace, and confirm the target account and slug before executing API mutations. <br>
Risk: The test skill is intended to be ephemeral and may remain published if cleanup fails. <br>
Mitigation: Inspect the ClawHub skill page after a test run and delete the test release if it remains visible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/tosr-test-pub-update-1781062438) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Markdown prose with REST API operation descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code is bundled; following the skill may mutate ClawHub skill records in a real account.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and artifact test identifier) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
