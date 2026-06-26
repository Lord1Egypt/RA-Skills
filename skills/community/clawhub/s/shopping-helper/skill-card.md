## Description: <br>
购物省钱攻略，当用户询问网购、购物、买东西、划算时调用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GeraldAlexanderrw](https://clawhub.ai/user/GeraldAlexanderrw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask about online shopping, coupons, product categories, and platform-specific deals to get current discount suggestions for major Chinese e-commerce platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coupon data and links come from a third-party service and may be stale, unavailable, or point to destinations the user has not independently verified. <br>
Mitigation: Verify coupon destinations before opening links, and treat offers as time-sensitive shopping information rather than authoritative pricing. <br>
Risk: The skill can run a user-triggered upgrade command as a maintenance action. <br>
Mitigation: Use the upgrade command deliberately, and install or update only when comfortable with the publisher and release source. <br>
Risk: Shopping workflows can expose private account or payment information if users provide it unnecessarily. <br>
Mitigation: Do not provide shopping account passwords, payment details, or private account data to this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GeraldAlexanderrw/shopping-helper) <br>
- [Third-party coupon API endpoint](https://open.datadex.com.cn/dexserver/dex-api/v1/getcoupon) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text shopping recommendations with coupon codes, links, and short usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include time-sensitive coupon links or copy-and-open app instructions.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
