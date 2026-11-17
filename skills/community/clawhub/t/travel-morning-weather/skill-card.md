## Description:

Adjust morning weather briefing location based on travel plans captured from conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suidge](https://clawhub.ai/user/suidge)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to keep morning weather briefings aligned with upcoming travel plans captured from conversation. The skill stores a default location and dated travel locations, then uses the current Asia/Shanghai date to choose the weather query location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores home city and travel schedule information that may be sensitive.

Mitigation: Review the stored travel-plan.json contents before use and keep the file in a private agent workspace with appropriate access controls.

Risk: The skill can update travel plans from conversation-derived dates and locations.

Mitigation: Require user confirmation before saving new or changed travel entries, especially for inferred dates, ranges, or locations.

Risk: Documented weather commands use user-derived locations in shell-style examples.

Mitigation: Validate and URL-encode locations, and invoke scripts and curl with structured arguments rather than interpolated shell strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suidge/skills/travel-morning-weather)
- [Project homepage](https://github.com/Suidge/travel-morning-weather)
- [Capture triggers](references/capture-triggers.md)
- [Travel plan data format](references/data-format.md)
- [Morning briefing integration](references/morning-briefing.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local travel-plan.json state and weather-query guidance for morning briefing location selection.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
