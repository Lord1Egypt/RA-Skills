## Description: <br>
Provides cross-border paid ads optimization coaching across targeting, creatives, bidding, landing pages, and analytics for Meta, TikTok, Google, and multi-channel campaigns through Yufluent cloud execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce marketers, agencies, and operators use this skill to request paid advertising optimization guidance for audience targeting, creative testing, bidding, landing-page review, and analytics decisions. The skill is intended to return recommendations for human review before changes are made in advertising platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a Yufluent API key and campaign context to a configurable network destination. <br>
Mitigation: Use only approved Yufluent credentials, leave TOKENAPI_BASE_URL unset unless the destination is trusted, and avoid confidential campaign, customer, or account data unless your organization permits sending it to Yufluent cloud. <br>
Risk: Automatic fallback to a broader Yufluent agent endpoint can change the execution path. <br>
Mitigation: Review outputs before acting on them and verify endpoint behavior in the deployment environment. <br>
Risk: Advertising recommendations may be incomplete or conflict with platform policies or local market rules. <br>
Mitigation: Have a qualified operator review recommendations before applying changes in ad platforms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-ad-optimize) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown or plain text returned from Yufluent cloud skill execution; setup and examples use shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY and may send campaign context, metrics, and account-related inputs to Yufluent cloud.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
