## Description:

循古·算命 helps agents handle explicit user requests for BaZi, daily fortune, Liu Yao, Da Liu Ren, Lu Ming, luck-cycle, and annual-fortune readings through the xungufa.com divination service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnyouker](https://clawhub.ai/user/cnyouker)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill when they explicitly want Chinese astrology or divination readings. The agent collects the requested birth or casting details, calls the relevant xungufa.com service, and returns formatted readings with practical interpretation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth details and divination query data may be sent to xungufa.com.

Mitigation: Use the skill only when the user explicitly requests these readings and is comfortable sharing the relevant details with the third-party service.

Risk: The skill may look for XUNGU_API_TOKEN in environment variables or local .env files.

Mitigation: Configure the token through a scoped secret or environment variable and avoid placing unrelated credentials in files the agent can read.

Risk: Birth profile details may be stored locally in plaintext if the user agrees to save them.

Mitigation: Decline profile saving unless persistence is needed, and use the documented delete flow to remove saved profile data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnyouker/skills/xungu-query)
- [cnyouker publisher profile](https://clawhub.ai/user/cnyouker)
- [循古排盘 service](https://xungufa.com)
- [BaZi API endpoint](https://xungufa.com/api/agent/bazi)
- [Liu Yao API endpoint](https://xungufa.com/api/agent/liuyao)
- [Da Liu Ren API endpoint](https://xungufa.com/api/agent/daliuren)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown text with formatted divination charts, API status notices, and narrative guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authentication or quota notices and prompts asking whether to save or delete a local birth profile.]

## Skill Version(s):

1.0.13 (source: server evidence release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
