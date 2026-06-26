## Description: <br>
Search and call monetized AI skills from Skillz Market with automatic USDC payments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hiich](https://clawhub.ai/user/Hiich) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to discover Skillz Market services, inspect skill metadata, and call paid x402-enabled endpoints with USDC payments from a configured wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend USDC from the configured wallet when paid calls are made. <br>
Mitigation: Use a dedicated low-balance wallet and review the destination and price before running paid calls. <br>
Risk: The direct command can call arbitrary x402-enabled endpoints. <br>
Mitigation: Avoid direct endpoint calls unless the endpoint is trusted. <br>
Risk: Request JSON may be sent to external paid services. <br>
Mitigation: Do not include secrets or sensitive data in request payloads. <br>


## Reference(s): <br>
- [SkillzMarket on ClawHub](https://clawhub.ai/Hiich/skillzmarket) <br>
- [Skillz Market](https://skillz.market) <br>
- [x402 Protocol](https://x402.org) <br>
- [Skillz Market API](https://api.skillz.market) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and SKILLZ_PRIVATE_KEY for paid call and direct endpoint commands.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
