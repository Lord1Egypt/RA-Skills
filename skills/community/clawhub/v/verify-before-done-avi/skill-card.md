## Description: <br>
Prevent premature completion claims, repeated same-pattern retries, and weak handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to improve execution discipline by verifying work before claiming completion, switching strategies after repeated ineffective attempts, and providing clearer handoffs when blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested verification steps could include tests, commands, or real integration checks that affect sensitive systems. <br>
Mitigation: Review proposed tests, commands, and external integration calls before they touch production, account, financial, or other sensitive data. <br>
Risk: The skill improves completion discipline but cannot independently prove that a task is complete. <br>
Mitigation: Use lightweight direct checks when possible and explicitly state what was checked, what could not be checked, and any remaining uncertainty. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance for agent behavior and response patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not include code, shell commands, persistence, or credential requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
