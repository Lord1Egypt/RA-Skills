## Description:

Walter Info gathers global city weather forecasts and cross-border e-commerce news, then generates Chinese Markdown reports and JSON data files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyondbright](https://clawhub.ai/user/beyondbright)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to collect weather forecasts for configured global cities and current cross-border e-commerce news for review, reporting, and operational planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News fetching disables TLS certificate verification.

Mitigation: Restore certificate verification or run only behind trusted network controls before relying on fetched news content.

Risk: The artifact includes undocumented helper scripts, including cleanup.py, that modify local skill files.

Mitigation: Remove or ignore undocumented maintenance scripts before installation and execute only the documented weather and news entry points.

Risk: Article text used for LLM summaries is untrusted external content.

Mitigation: Use a constrained summarization agent that treats llm_input article text as data, not instructions.

Risk: The skill writes dated Markdown and JSON files locally under its output directory.

Mitigation: Run it in a controlled workspace and review generated files before sharing or using them operationally.

## Reference(s):

- [Walter Info on ClawHub](https://clawhub.ai/beyondbright/skills/walter-info)
- [ennews](https://www.ennews.com/news/)
- [cifnews](https://www.cifnews.com/)
- [wttr.in weather API](https://wttr.in/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Chinese Markdown reports and JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated weather and news reports under the skill output directory; full runs may prepare llm_input JSON for short Chinese article summaries.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
