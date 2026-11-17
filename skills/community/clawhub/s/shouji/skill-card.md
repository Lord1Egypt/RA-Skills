## Description:

根据手机号查归属省市、运营商与卡类型。当用户说：138xxxx 是哪里的号？这个号码联通还是移动？或类似手机号归属地问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query a mobile phone number's province, city, carrier, and card type through JisuAPI. Agents can call the included Python script with a JSON request and summarize the returned attribution fields for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried phone numbers are sent to JisuAPI, a third-party service.

Mitigation: Submit only numbers the user is authorized to check, avoid unnecessary exposure of full numbers in conversation, and follow JisuAPI's terms and privacy expectations.

Risk: The script relies on a JISU_API_KEY from the runtime environment.

Mitigation: Store the API key in environment configuration, do not paste it into prompts or logs, and rotate it if exposure is suspected.

Risk: Returned data and error messages come from the third-party API and may be incomplete, unavailable, or service-dependent.

Mitigation: Present results as JisuAPI-provided attribution data and preserve API error context when a lookup fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/shouji)
- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI mobile phone number location API documentation](https://www.jisuapi.com/api/shouji/)
- [JisuAPI mobile phone number query endpoint](https://api.jisuapi.com/shouji/query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable; query results and API errors are returned as JSON.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
