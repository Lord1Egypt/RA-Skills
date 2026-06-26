## Description: <br>
Creates Xiaozhi recycling orders through the Xiaozhi Recycle Open Platform API for device and clothing recycling, including information collection, optional clothing price quotes, WeChat scan authorization, and order submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiongdong-tech](https://clawhub.ai/user/xiongdong-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect contact, address, item, and pickup details, obtain clothing recycling prices when needed, and submit Xiaozhi recycling pickup orders after WeChat scan authorization. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real recycling pickup orders using user-provided contact, address, item, pickup time, and price details. <br>
Mitigation: Use it only when a real order is intended, show an order summary, and require user confirmation before authorization and submission. <br>
Risk: Personal contact and address data and WeChat authorization are sent to a third-party recycling service. <br>
Mitigation: Collect only the details needed for the order, avoid reusable WeChat tokens, and make sure the user understands the data will be sent to Xiaozhi recycling APIs. <br>
Risk: Custom API endpoint overrides could send order data or authorization tokens to untrusted services. <br>
Mitigation: Use the default Xiaozhi endpoints unless the replacement endpoint is fully trusted and reviewed. <br>


## Reference(s): <br>
- [Xiaozhi Recycle Order on ClawHub](https://clawhub.ai/xiongdong-tech/xiaozhi-order-creator) <br>
- [Xiaozhi Recycle Open Platform API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a local WeChat mini-program code image for user authorization.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
