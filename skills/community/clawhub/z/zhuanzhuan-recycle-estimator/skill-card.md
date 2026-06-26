## Description: <br>
Supports Zhuanzhuan recycle valuation requests across product categories by using images, text, model details, specifications, and condition information to provide reference trade-in prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjinxinlove](https://clawhub.ai/user/chenjinxinlove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to estimate the recycle or resale value of pre-owned goods such as phones, tablets, laptops, audio devices, cameras, and home appliances. The skill helps identify missing details, ask clarifying questions, and provide non-binding reference price ranges before a user proceeds to Zhuanzhuan Recycle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Item descriptions and photos may be sent to Zhuanzhuan for valuation. <br>
Mitigation: Install only if this data sharing is acceptable for the intended users and environment. <br>
Risk: The image argument can upload arbitrary local files as images. <br>
Mitigation: Do not pass unrelated local file paths as --image, and review image inputs before execution. <br>
Risk: A custom base URL can redirect valuation payloads to another destination. <br>
Mitigation: Avoid --base-url unless the destination is fully trusted. <br>
Risk: Session and IP-related state can persist between valuation sessions. <br>
Mitigation: Reset state between unrelated valuation sessions in shared or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenjinxinlove/zhuanzhuan-recycle-estimator) <br>
- [Publisher profile](https://clawhub.ai/user/chenjinxinlove) <br>
- [Zhuanzhuan valuation endpoint](https://zai.zhuanzhuan.com/zai/find_mate/v1/openclaw/recycle-skill/valuate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or concise user-facing text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recognized item details, reference price ranges, missing fields, clarification options, and next-step guidance; estimates are not binding offers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
