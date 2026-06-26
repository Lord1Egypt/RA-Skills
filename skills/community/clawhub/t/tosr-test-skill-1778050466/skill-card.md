## Description: <br>
Automated integration test skill that verifies ClawHub skill lifecycle operations, including publishing, inspection, updates, and deletion through the REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill as a ClawHub lifecycle test reference for publishing, inspecting, updating, and deleting a disposable skill through the REST API. It should be used only when those create, update, and delete actions are intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lifecycle testing can create, update, or delete real ClawHub skills if used with production credentials or non-disposable skill slugs. <br>
Mitigation: Use disposable test credentials and skill slugs, and run lifecycle tests only when those create, update, and delete actions are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/tosr-test-skill-1778050466) <br>
- [Source skill file](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes REST API lifecycle operations; no executable code is included.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
