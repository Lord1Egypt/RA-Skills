## Description: <br>
Generates a high-end black-and-gold vertical recruitment poster for private circles, paid communities, or clubs, with optional Feishu image delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyken](https://clawhub.ai/user/jackyken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, community operators, and agents use this skill to produce customizable recruitment posters for private clubs, paid communities, and membership offerings, then optionally send the generated image through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials may be exposed when optional delivery is used. <br>
Mitigation: Avoid placing secrets directly in shell history, use a least-privileged Feishu app, and provide credentials only when Feishu delivery is intended. <br>
Risk: The generated poster may be sent to the wrong Feishu recipient. <br>
Mitigation: Confirm the recipient ID and receive ID type before sending the image. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackyken/social-recruit-page) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, API Calls] <br>
**Output Format:** [PNG image file generated from configurable HTML, with optional Feishu image message delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional JSON configuration controls brand, founder, pricing, quota, services, target audience, footer copy, and year.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
