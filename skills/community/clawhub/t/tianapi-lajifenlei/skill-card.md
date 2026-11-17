## Description:

根据物品名称查询垃圾分类信息，支持模糊搜索和精确搜索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up waste classification by item name through TianAPI and present classification suggestions, disposal tips, and explanations to end users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TianAPI credentials may be exposed if passed on the command line or committed in scripts/.env.

Mitigation: Use a dedicated, low-privilege TianAPI key, prefer TIANAPI_LAJIFENLEI_KEY, and avoid committing local credential files.

Risk: Queried item names are sent to TianAPI and could contain sensitive or personal text.

Mitigation: Do not submit sensitive or personal text as item names, and make the third-party API lookup clear to users.

Risk: The artifact advertises JSON output, but the bundled script does not define a --json command-line option.

Mitigation: Validate command behavior before relying on JSON output, or use the documented TianAPI endpoint directly when structured output is required.

## Reference(s):

- [TianAPI Lajifenlei API Documentation](https://www.tianapi.com/apiview/97)
- [TianAPI Lajifenlei API Endpoint](https://apis.tianapi.com/lajifenlei/index)
- [ClawHub Skill Page](https://clawhub.ai/workxin/skills/tianapi-lajifenlei)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and API lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TianAPI key via TIANAPI_LAJIFENLEI_KEY, scripts/.env, or --key; queried item names are sent to TianAPI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
