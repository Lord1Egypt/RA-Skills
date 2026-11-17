## Description:

Generates BaZi chart data from QiyueAstro's public API using birth date, birth time, and gender, then displays the returned four pillars, day master, five-element statistics, palaces, and fortune periods without model interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloodymarygg](https://clawhub.ai/user/bloodymarygg)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request an entertainment and self-exploration BaZi chart from QiyueAstro by providing birth details and gender. The agent returns the API's chart fields in a readable format without adding fortune-telling interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends birth date, birth time, gender, and any optional question to qiyueastro.com.

Mitigation: Install only if this data sharing is acceptable, and avoid entering unnecessary sensitive details in the optional question field.

Risk: Users could treat chart output as personalized advice beyond the returned API data.

Mitigation: Keep responses limited to the API's chart fields and avoid adding independent interpretation or judgment.

## Reference(s):

- [QiyueAstro](https://qiyueastro.com)
- [QiyueAstro BaZi Public API](https://qiyueastro.com/api/v1/openclaw/bazi)
- [ClawHub skill page](https://clawhub.ai/bloodymarygg/skills/qiyue-bazi-drawer)
- [Publisher profile](https://clawhub.ai/user/bloodymarygg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API calls]

**Output Format:** [Markdown text with structured BaZi chart fields returned by the API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the original API chart data, avoids independent chart interpretation, and ends with a QiyueAstro call-to-action.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
