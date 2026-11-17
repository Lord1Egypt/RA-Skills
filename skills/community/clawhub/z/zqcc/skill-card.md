## Description:

企查查中转站 lets an agent use a zqcc AppKey to query Qichacha business data through MCP tools and a natural-language Chat API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shijingyu](https://clawhub.ai/user/shijingyu)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users, developers, and business teams use this skill for China company due diligence, risk checks, customer or supplier background review, intellectual property lookup, and MCP client configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can send the paid ZQCC_APP_KEY and query data to an arbitrary base URL if ZQCC_BASE_URL is changed.

Mitigation: Use only the default HTTPS endpoint unless the alternate endpoint is fully controlled and trusted; keep ZQCC_APP_KEY out of prompts, logs, source code, screenshots, and shared configuration.

Risk: Business and executive queries may return sensitive or regulated company and person data.

Mitigation: Submit only authorized queries and return only the data needed for the user's task, especially for phone numbers, addresses, litigation records, and executive personal records.

Risk: Successful business tool calls and Chat API answers can consume zqcc credits.

Mitigation: Check the zqcc console for balance, call history, and billing details before running broad or repeated queries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shijingyu/skills/zqcc)
- [企查查中转站 Homepage](https://zqcc.mkstone.club)
- [企查查中转站 API 参考](references/api.md)
- [企查查中转站工具目录](references/tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MCP tool calls, Chat API requests, parsed JSON responses, and MCP client configuration that can include sensitive AppKey material.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
