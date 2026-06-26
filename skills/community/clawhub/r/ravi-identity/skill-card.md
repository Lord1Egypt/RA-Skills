## Description: <br>
Get your agent identity (email, phone, owner name) and manage identities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to retrieve their Ravi-provided email address, phone number, owner information, and identity list, and to create or switch identities when explicitly requested by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal Ravi identity details such as email, phone, owner name, and identity list. <br>
Mitigation: Install only where agent access to those identity details is intended. <br>
Risk: The skill can create or switch identities through the ravi CLI. <br>
Mitigation: Confirm with the user before creating or switching identities, and use only a trusted ravi CLI. <br>


## Reference(s): <br>
- [Ravi Identities API schema](https://ravi.id/docs/schema/identities.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May expose or change agent identity details through the trusted ravi CLI.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
