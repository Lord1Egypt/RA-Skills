## Description:

Manage Roblox game passes and developer products via Open Cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teddyengel](https://clawhub.ai/user/teddyengel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Roblox experience operators use this skill to list, create, retrieve, and update game passes and developer products through Roblox Open Cloud with a configured API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented launch command downloads and runs an unpinned Bun runtime while a Roblox API key may be present.

Mitigation: Use a pinned or preinstalled Bun runtime and review the resolved runtime before running commands with ROBLOX_API_KEY.

Risk: A Roblox API key can grant write access to game passes and developer products.

Mitigation: Use keys scoped to only the needed experiences and permissions, and keep separate read-only and write-capable keys.

Risk: Create and update commands can change monetized Roblox assets.

Mitigation: Confirm the universe ID, item ID, price, and for-sale flag before executing write commands.

## Reference(s):

- [Roblox Open Cloud API Documentation](https://create.roblox.com/docs/cloud)
- [Roblox API Keys Guide](https://create.roblox.com/docs/cloud/auth/api-keys)
- [Game Passes API](https://create.roblox.com/docs/cloud/reference/features/game-passes)
- [Developer Products API](https://create.roblox.com/docs/cloud/reference/features/developer-products)
- [Roblox Creator Hub Credentials](https://create.roblox.com/dashboard/credentials)
- [ClawHub Skill Page](https://clawhub.ai/teddyengel/skills/roblox-cli)
- [Source Link From Skill Metadata](https://github.com/ingalls-ltd/RobloxCliSkillOpenClaw)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON command responses with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ROBLOX_API_KEY and Roblox Open Cloud permissions for the requested operation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
