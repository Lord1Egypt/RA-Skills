## Description: <br>
Uses vision and radar inputs to detect possible falls for elderly people living alone and trigger rapid safety alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, family members, and care-facility operators can use this skill to analyze monitoring images or videos for possible falls and to retrieve cloud-stored fall detection reports. Results should be treated as safety alerts that require human confirmation and emergency follow-up when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send sensitive home images, videos, and user identifiers to external cloud services and preserve account-linked report history. <br>
Mitigation: Use only with trusted services and explicit consent from monitored people; review privacy, retention, and account-linking implications before installation. <br>
Risk: Fall detection output can be incorrect or delayed and is not a substitute for human confirmation. <br>
Mitigation: Treat results as alerts, verify the situation directly, and follow established emergency response procedures for high-severity alarms. <br>
Risk: The security review marked the release suspicious because it may create or reuse accounts and store returned tokens locally without clear upfront disclosure. <br>
Mitigation: Inspect configuration and token storage behavior before use, limit credentials to the minimum required scope, and avoid deployment where local token persistence is unacceptable. <br>


## Reference(s): <br>
- [Elderly Fall Detection API documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-elderly-fall-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries or JSON analysis results, with command examples for invoking the packaged scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include detected fall status, confidence, alarm level, emergency suggestions, and links to cloud-hosted reports returned by the external service.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
