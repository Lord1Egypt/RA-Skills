## Description: <br>
Provides a Yufluent cloud-backed paid ads optimization coach for Meta, TikTok, Google, and multi-channel campaigns across targeting, creatives, bidding, landing page, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, ecommerce operators, and agents use this skill to collect campaign context and request Yufluent-generated optimization guidance for paid ads. The generated recommendations are intended for human review before any campaign changes are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign messages, product details, market data, metrics, and related business context are sent to a remote Yufluent service. <br>
Mitigation: Install only if the provider's retention and access policies are acceptable, and avoid sending confidential customer, financial, or unreleased strategy data. <br>
Risk: The skill requires an authenticated API key and can direct requests through a configurable API base URL. <br>
Mitigation: Keep API keys scoped and revocable, review TOKENAPI_BASE_URL before use, and rotate credentials if an endpoint or environment is no longer trusted. <br>
Risk: Advertising recommendations may be incorrect, incomplete, or unsuitable for a platform policy or target-market regulation. <br>
Mitigation: Review proposals manually before execution, verify them against platform ad policies and applicable law, and do not treat the skill output as evidence that an ad account was changed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/metahuan/yufluent-clawhub-publish-yufluentcn-ad-optimize) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw integration](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text guidance returned by the Yufluent cloud client, with optional shell command examples for invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY and may use TOKENAPI_BASE_URL; supported dimensions are targeting, creatives, bidding, landing, and analytics.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
