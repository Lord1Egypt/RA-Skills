## Description: <br>
美团优惠券 helps users authenticate with Meituan by SMS, claim available Meituan coupon benefits, and query local coupon-claim history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users invoke this skill when they want an agent to help claim Meituan coupon benefits or check previously claimed coupons for a Meituan account. The skill handles SMS-based account authentication, coupon issuance, and history lookup through its bundled scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authenticate to Meituan by SMS and reuse a locally stored Meituan token. <br>
Mitigation: Use the skill only when the user explicitly wants to log in or claim/query coupons, and do not ask for or use an SMS code unless the user intends to complete login. <br>
Risk: Reusable account tokens and coupon history are stored locally. <br>
Mitigation: Use the documented environment-variable paths for isolation when needed, and clear the auth or history files when the user wants to remove local account data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-openplatform/waimai-coupon) <br>
- [Meituan coupon skill update page](https://clawhub.ai/meituan-zhengchang/meituan-coupon) <br>
- [Meituan coupon service host](https://peppermall.meituan.com) <br>
- [Meituan EDS Claw SMS login interface documentation](https://km.sankuai.com/collabpage/2752893495) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include coupon details, masked phone numbers, login prompts, error messages, and local history lookup results.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
