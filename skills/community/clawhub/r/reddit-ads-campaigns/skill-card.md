## Description: <br>
Inspect Reddit Ads campaigns, ad groups, creatives, and reporting data via the Reddit Ads API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External advertisers and marketing operators use this skill to inspect Reddit Ads campaign structure, creative status, and reporting data, and to manage live campaign resources after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected Reddit Ads tools can make live campaign changes that affect advertising spend. <br>
Mitigation: Review previews carefully and approve write actions only when the account, resource, and spend impact match the intended change. <br>
Risk: The skill requires connecting a Reddit Ads account through ClawLink and uses sensitive OAuth credentials. <br>
Mitigation: Install only when comfortable with that connection model and keep access scoped to the intended Reddit Ads account. <br>


## Reference(s): <br>
- [Reddit Ads API Documentation](https://ads-api.reddit.com/docs/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/reddit-ads-campaigns) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated Reddit Ads API inspection and confirmed live campaign management through ClawLink.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
