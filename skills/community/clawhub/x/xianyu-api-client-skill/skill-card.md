## Description:

Secure Xianyu Guanjia API client with endpoint allowlisting, enforced confirmation for high-risk actions, dry-run mode, and unsafe methods for automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crab-xieyujin](https://clawhub.ai/user/crab-xieyujin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external marketplace operators use this skill to let an agent configure and call the Xianyu Guanjia Open Platform for product, order, shop, category, logistics, and area-data workflows. The skill is intended for Xianyu shop automation where API credentials and write permissions are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform write operations against Xianyu shop products and orders when valid credentials are provided.

Mitigation: Install only for Xianyu shop automation, use dedicated low-permission credentials, and review write requests before execution.

Risk: The artifact includes credential-like example values.

Mitigation: Do not use the bundled example values; rotate or revoke any real credentials that match the published examples.

Risk: Unsafe methods bypass the normal confirmation prompt for automation.

Mitigation: Use unsafe methods only in controlled automation after dry-run review and with minimum-necessary API permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crab-xieyujin/skills/xianyu-api-client-skill)
- [OpenClaw source listing](https://clawhub.com/skills/xianyu-api-client)
- [Xianyu Guanjia Open Platform](https://www.goofish.pro)
- [Xianyu Open API endpoint host](https://open.goofish.pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request payloads, dry-run previews, and credential configuration guidance.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
