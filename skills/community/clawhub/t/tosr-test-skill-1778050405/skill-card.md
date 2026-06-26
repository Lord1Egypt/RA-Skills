## Description: <br>
Automates end-to-end testing of ClawHub skill lifecycle operations, including publish, inspect, update, and delete. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to exercise temporary ClawHub skill lifecycle tests against a test skill slug. It is intended for controlled integration testing rather than general user workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lifecycle testing can create, update, or delete ClawHub skills if run with broad or production credentials. <br>
Mitigation: Run only with a test account or tightly scoped credentials, confirm the temporary slug before update or delete actions, and verify cleanup after the test. <br>


## Reference(s): <br>
- [TOSR Test Skill on ClawHub](https://clawhub.ai/yinwuzhe/tosr-test-skill-1778050405) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for a temporary lifecycle test skill.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
