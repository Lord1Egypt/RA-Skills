## Description: <br>
Get AI-ranked exhibitors matching a user's ICP and shortlist the top accounts worth outreach at a trade show. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
B2B sales, marketing, and event teams use this skill before a trade show to find exhibitors that match an ideal customer profile and prioritize outreach targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends trade-show and ICP query data to Lensmor's API. <br>
Mitigation: Use it only when Lensmor is trusted for that data and avoid submitting sensitive prospecting details that should not leave the user's environment. <br>
Risk: The skill requires a LENSMOR_API_KEY secret. <br>
Mitigation: Store the API key as a secret and do not paste real keys into examples, prompts, shared logs, or generated output. <br>
Risk: The skill may hand off results to downstream contact-finding or outreach workflows. <br>
Mitigation: Review downstream skills and generated outreach before use, especially when handling personal contact data or sales communications. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/weilun88313/trade-show-lead-recommender) <br>
- [Lensmor API Documentation](https://api.lensmor.com/) <br>
- [Lensmor Platform Base URL](https://platform.lensmor.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown with ranked tables, ICP match rationale, and follow-up suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Lensmor API results and must not reveal the LENSMOR_API_KEY value.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
