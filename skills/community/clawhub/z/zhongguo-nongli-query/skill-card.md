## Description:

Provides Chinese lunar calendar date conversion for Gregorian dates, including lunar year/month/day, zodiac, and ganzhi lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leocdchina](https://clawhub.ai/user/leocdchina)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert specific Gregorian dates or date ranges into Chinese lunar calendar data. It is best suited for date conversion and zodiac/ganzhi lookup, not primary auspicious-day selection or broader Huangli judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens can be sent to an environment-selected API base.

Mitigation: Install only from a trusted publisher, leave HUANGLI_BASE unset or set it only to the official HTTPS API host, and avoid sharing HUANGLI_TOKEN beyond the intended service.

Risk: Large date ranges can cause excessive API calls or quota usage.

Mitigation: Keep batch ranges bounded and review requested date spans before execution.

Risk: The artifact includes broader Huangli search/filter behavior than the narrow date-conversion framing suggests.

Mitigation: Use this skill for lunar date conversion and route auspicious-day or吉凶择日 requests to the dedicated Huangli/Jixiong skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leocdchina/skills/zhongguo-nongli-query)
- [Official skill homepage](https://nongli.skill.4glz.com)
- [Huangli Toolkit Reference](references/reference.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HUANGLI_TOKEN and HTTPS access to the Huangli API service.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
