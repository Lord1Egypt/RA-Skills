## Description: <br>
Fetches hidden takeout coupon lists and redemption guidance for Meituan, Taobao Flash/Ele.me, and JD.com from a disclosed third-party coupon API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moooai](https://clawhub.ai/user/moooai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current takeout coupon codes, QR redemption links, and platform-specific redemption instructions for Meituan, Taobao Flash/Ele.me, and JD.com. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned coupon codes, QR images, and redemption pages are external promotional content. <br>
Mitigation: Show users the destination context and advise them not to enter sensitive account or payment information unless they independently trust the destination. <br>
Risk: The skill depends on a third-party coupon API whose availability or response structure can change. <br>
Mitigation: Handle request failures and unexpected response shapes gracefully, and tell users to retry later when coupon data cannot be fetched. <br>
Risk: Coupon codes may contain platform-specific special characters that are easy to corrupt. <br>
Mitigation: Display coupon_code values exactly as returned by the API without translation, formatting, added spacing, or character changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moooai/takeout-coupon) <br>
- [Publisher profile](https://clawhub.ai/user/moooai) <br>
- [Clawdis homepage](https://github.com/moooai/skills) <br>
- [API documentation](references/api_documentation.md) <br>
- [Coupon API endpoint](https://agskills.moontai.top/coupon/takeout) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown or JSON containing coupon titles, unmodified coupon codes, QR image URLs, and redemption instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coupon codes are external promotional content and should be displayed exactly as returned by the API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
