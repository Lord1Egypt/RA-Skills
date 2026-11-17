## Description:

依托全球蜜罐网络及百万级节点构建的IP情报分析平台，提供精准的IP画像与威胁预警服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and security analysts use this skill to query threat intelligence for a specified IP address, including geolocation, ASN, and historical malicious activity signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Xiaobenyang API key and stores it in a local plaintext .env file.

Mitigation: Prefer providing the key through a secure environment or secret store and avoid shared workspaces for this skill.

Risk: Queried IP data is sent to the configured Xiaobenyang API endpoint.

Mitigation: Review data handling requirements before submitting sensitive or regulated IP lookup requests.

Risk: Server security evidence reports stale instructions, a broken tool definition, and credential-storage handling concerns.

Mitigation: Review and scan the skill before deployment, and use it only after those issues are accepted or fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/xby-ip-query)
- [Xiaobenyang service](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Xiaobenyang API key before querying IP intelligence.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
