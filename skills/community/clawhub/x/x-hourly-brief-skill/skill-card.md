## Description: <br>
X Hourly Brief generates charge-first briefs from high-value X post URLs with Chinese, English, or automatic language output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangkefeng-ai](https://clawhub.ai/user/huangkefeng-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to summarize supplied X post URLs into per-post key points and a final digest after billing succeeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can charge a user balance before generating results. <br>
Mitigation: Use only with a trusted publisher and billing provider, and confirm the billing flow before running. <br>
Risk: Supplied URLs may be fetched through external services, which can expose private, internal, or unintended URLs. <br>
Mitigation: Use only public X post URLs and avoid private, internal, or non-X URLs. <br>
Risk: The security review marked the release suspicious because it combines charge-first behavior with external URL fetching. <br>
Mitigation: Review the skill and security guidance carefully before installing or running it in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangkefeng-ai/x-hourly-brief-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON object printed to stdout, with billing status or payment link errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports zh, en, and auto language modes; processes up to 20 supplied URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
