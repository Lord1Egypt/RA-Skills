## Description: <br>
Create and manage test payment links for one-time, recurring, payment plan, multi-product, custom plan, and pay-what-you-want scenarios in a sandbox environment. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[yaggit](https://clawhub.ai/user/yaggit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and testers use this skill to create and validate sandbox payment link flows before using a production payment system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production credentials, customer data, redirect URLs, metadata, or webhook payloads could be sent to a test payment helper. <br>
Mitigation: Use only local or sandbox payment services, avoid production payment credentials, and review payloads before execution. <br>
Risk: The skill description lists broader payment-link capabilities than the included script appears to implement. <br>
Mitigation: Expect only implemented sandbox behavior, and validate the requested payment link type before use. <br>
Risk: Sandbox payment responses may differ from live payment processor behavior. <br>
Mitigation: Treat outputs as test evidence only and revalidate payment flows with the intended production provider before launch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yaggit/skill-by-test) <br>
- [Skill homepage](https://test.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON API responses, concise error text, and command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves raw service responses when applicable and is intended for local or sandbox payment testing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
