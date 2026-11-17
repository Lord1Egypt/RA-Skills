## Description:

truetime-cn helps agents answer Chinese-focused time and calendar questions by running a local Python utility for current time, offsets, time zones, DST checks, lunar dates, Chinese statutory holidays, make-up workdays, and solar terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sereinnyaa](https://clawhub.ai/user/sereinnyaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to verify time-sensitive Chinese-language scheduling, deadline, holiday, time-zone, and lunar-calendar questions before answering users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill strongly encourages agents to run its Python script for many time-related questions, and responses are Chinese-oriented by default.

Mitigation: Use it for time-sensitive or calendar-specific tasks, then adapt the final answer language and level of detail to the user's request.

Risk: Chinese holiday data is bundled for 2026; later years may fall back to weekend-only rules.

Mitigation: Check the script's holiday_data_year_available field and disclose unavailable holiday data before making scheduling recommendations.

Risk: The skill depends on local execution of bundled Python code.

Mitigation: Run it in a sandboxed context without credentials, network access, or background permissions, and inspect the JSON result or error before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sereinnyaa/skills/truetime-cn)
- [cnLunar upstream repository](https://github.com/OPN48/cnLunar)
- [cccat6/truetime inspiration](https://github.com/openclaw/skills/tree/main/skills/cccat6/truetime)
- [2026 China holiday notice source](http://politics.people.com.cn/n1/2025/1104/c1001-40596715.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON from the Python utility plus concise Chinese-oriented Markdown or text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python execution; no external package installation; UTC is the canonical time value.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
