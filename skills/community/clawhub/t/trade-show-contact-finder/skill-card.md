## Description: <br>
Find decision-makers and key contacts at exhibitor companies using the Lensmor API for pre-show LinkedIn outreach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
B2B sales and marketing teams use this skill to identify senior decision-makers, influencers, and likely outreach contacts at exhibitor companies before trade shows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends company names and role filters to Lensmor and returns contact and LinkedIn profile data for outreach. <br>
Mitigation: Confirm Lensmor is trusted for these inputs and use returned data only under applicable privacy, marketing, anti-spam, and platform-use rules. <br>
Risk: Returned contact data may be incomplete, stale, or unsuitable for a specific buyer function. <br>
Mitigation: Verify high-priority contacts before outreach, broaden filters when results are sparse, and do not fabricate missing contacts or email addresses. <br>
Risk: The skill requires a Lensmor API key. <br>
Mitigation: Store LENSMOR_API_KEY securely, never print it in responses, and stop execution when the key is missing or rejected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/weilun88313/trade-show-contact-finder) <br>
- [Lensmor API Documentation](https://api.lensmor.com/) <br>
- [Lensmor Platform](https://platform.lensmor.com) <br>
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=trade-show-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown with prioritized contact tables and outreach notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; does not return email addresses and uses LinkedIn as the primary outreach channel.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
