## Description:

按频道与日期查电视节目单，可查频道列表。当用户说：央视一套今晚有什么节目？湖南卫视节目表，或类似电视节目问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up Chinese TV channel identifiers and dated program schedules, then summarize or filter program listings for user questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured JISU_API_KEY and TV channel/date query details to JisuAPI.

Mitigation: Use a JisuAPI-scoped key, avoid placing sensitive information in channel/date queries, and rotate the key if it is exposed.

Risk: Program data depends on the third-party TV data provider and can be unavailable, rate-limited, expired, or returned as API errors.

Mitigation: Handle documented API error responses in agent output and verify important schedule information before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/tv)
- [JisuAPI TV Program Preview API documentation](https://www.jisuapi.com/api/tv/)
- [JisuAPI](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends channel and date query details to JisuAPI.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
