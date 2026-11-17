## Description:

竞品 Listing 快照对比分析，通过粘贴竞品文案进行多维度对标（标题/五点/描述/关键词），输出差异化建议与机会点。经 Yufluent 云端 Harness 执行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and agents use this skill to compare manually supplied competitor listing copy against their own product or listing and receive a cloud-generated differentiation report for Amazon, Shopify, or TikTok.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local file contents supplied as competitor or own-listing inputs to Yufluent's cloud service.

Mitigation: Provide only intended listing text, and do not pass sensitive local paths such as .env files, SSH keys, cloud credentials, or private configs.

Risk: TOKENAPI_BASE_URL can redirect the API key and payload data to an alternate endpoint.

Mitigation: Leave TOKENAPI_BASE_URL unset unless intentionally using a trusted endpoint.

Risk: The security verdict is suspicious because the client sends listing payloads and the API key to a network service.

Mitigation: Install and run only when comfortable sharing competitor and first-party listing text with Yufluent's service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/metahuan/skills/yufluent-clawhub-publish-yufluentcn-comp-track)
- [Yufluent Console](https://claw.changzhiai.com)
- [Yufluent OpenClaw Integration](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text report from the cloud service, with optional file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY; accepts competitor text or a local text file, plus optional own-listing text.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
