## Description: <br>
wxb-assistant helps agents query Wangxiaobao recordings, reception records, customer data, customer profiles, and Panke analysis data after account authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[156554395](https://clawhub.ai/user/156554395) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales consultants and managers use this skill to retrieve Wangxiaobao customer records, visits, recordings, customer-profile predictions, Panke analysis, tenant/project information, and operational to-do data through an authorized account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive customer, recording, tenant, visit, and analytics data through the user's Wangxiaobao account. <br>
Mitigation: Install only when the publisher is trusted, use on a private machine, and avoid exposing terminal output, logs, or generated responses that contain sensitive account data. <br>
Risk: The skill persists the account auth token at ~/.wxb-auth-token. <br>
Mitigation: Clear ~/.wxb-auth-token when changing accounts, ending use, or working on a shared system. <br>
Risk: The skill includes write or control actions such as tenant switching, sharing, binding, commenting, submitting, updating, and recording or reception controls. <br>
Mitigation: Manually confirm any tenant switch, share, delete, bind, comment, submit, update, or recording/reception control action before execution. <br>


## Reference(s): <br>
- [ClawHub release: wxb-assistant](https://clawhub.ai/156554395/wxb-assistant) <br>
- [ClawHub publisher profile: 156554395](https://clawhub.ai/user/156554395) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Text, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Wangxiaobao account authorization and stores the auth token locally at ~/.wxb-auth-token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
