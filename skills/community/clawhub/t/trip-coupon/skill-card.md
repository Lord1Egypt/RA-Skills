## Description: <br>
获取出行优惠券，支持滴滴出行大礼包、携程礼包天天领（酒店、机票、门票），并返回领取链接和二维码图片供用户领取优惠。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moooai](https://clawhub.ai/user/moooai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent to retrieve available DiDi ride-hailing and Ctrip travel coupon offers. The skill helps agents present coupon titles, redemption links, QR code image links, and brief redemption guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls an external coupon API and may display third-party redemption links or QR code image URLs. <br>
Mitigation: Review returned destinations before opening links in WeChat or scanning QR codes. <br>
Risk: Bundled reference files describe unrelated food-delivery coupon flows, creating package consistency risk. <br>
Mitigation: Prefer a corrected release whose reference files match the travel-coupon purpose before deploying broadly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moooai/trip-coupon) <br>
- [Project homepage from ClawHub metadata](https://github.com/moooai/trip-coupon) <br>
- [Trip coupon API endpoint](https://agskills.moontai.top/coupon/trip) <br>
- [Packaged API documentation](references/api_documentation.md) <br>
- [Packaged API reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with coupon links, QR code image URLs, and optional JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes external redemption links and QR code image URLs returned by the coupon API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; packaged artifact frontmatter and _meta.json say 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
