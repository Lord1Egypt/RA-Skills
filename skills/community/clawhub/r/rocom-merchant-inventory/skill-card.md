## Description:

查询《洛克王国世界》远行商人当前库存，并自动过滤出本轮仍有效的商品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitansde](https://clawhub.ai/user/nitansde)

### License/Terms of Use:

MIT-0

## Use Case:

External users and game-assistant agents use this skill to check the current RoCom merchant inventory and return the items still valid in the current merchant round. It is useful when a user wants a concise text summary or JSON result and can provide their own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user-provided Roco merchant API key to the documented wegame.shallow.ink endpoint.

Mitigation: Install only if that endpoint is acceptable for the deployment, and provide ROCOM_API_KEY from a controlled environment.

Risk: Passing the API key with --api-key can expose it through shell history, logs, or shared terminal output.

Mitigation: Prefer ROCOM_API_KEY over command-line arguments and rotate the key if it may have been exposed.

Risk: Inventory results depend on a live remote API and current Beijing-time filtering.

Mitigation: Treat empty or failed results as live-service conditions and retry or verify directly before acting on the inventory.

## Reference(s):

- [API 说明](references/api.md)
- [ClawHub skill page](https://clawhub.ai/nitansde/skills/rocom-merchant-inventory)
- [Entropy-Increase-Team API key source](https://github.com/Entropy-Increase-Team/)
- [RoCom merchant inventory API endpoint](https://wegame.shallow.ink/api/v1/games/rocom/merchant/info?refresh=true)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Plain text inventory summary or JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied ROCOM_API_KEY and filters items to the current Beijing-time merchant round.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
