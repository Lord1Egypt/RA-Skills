## Description: <br>
Find ICP-matching exhibitors, prospects, and partners at trade shows using the Lensmor API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
B2B sales and marketing teams use this skill before trade shows to find exhibitors that match a company URL or target-audience description, then prioritize prospects, partners, and competitors for outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends company URLs, event interests, and target-audience descriptions to the Lensmor API. <br>
Mitigation: Verify trust in Lensmor before use and avoid submitting sensitive internal strategy or personal data. <br>
Risk: The Lensmor API key could be exposed through prompts, logs, or generated output. <br>
Mitigation: Use a revocable API key, never print LENSMOR_API_KEY, and rotate the key if exposure is suspected. <br>
Risk: Returned exhibitor matches or ICP rationale may be incomplete or inaccurate for outreach decisions. <br>
Mitigation: Ground rationale only in returned fields and review suggested prospects before taking action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/weilun88313/trade-show-exhibitor-search) <br>
- [Publisher profile](https://clawhub.ai/user/weilun88313) <br>
- [Lensmor API documentation](https://api.lensmor.com/) <br>
- [Lensmor platform base URL](https://platform.lensmor.com) <br>
- [Example: SaaS Vendor Prospecting at Dreamforce 2026](examples/saas-vendor-at-dreamforce.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown table with result summary, ICP match notes, error messages, and follow-up suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; output must not expose API keys, raw endpoint paths, raw curl commands, or fabricated exhibitor entries.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
