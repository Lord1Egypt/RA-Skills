## Description:

Helps users route Shanghai government service questions to likely departments, service items, online or offline handling paths, and official verification sources using public Shanghai "一网通办" data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aibot88](https://clawhub.ai/user/aibot88)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to identify likely Shanghai municipal departments, service items, official guide URLs, online handling indicators, and next steps for personal or organization service needs. It is routing help and should not be treated as final legal, eligibility, fee, deadline, or window-address advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shanghai government-service guidance may be incomplete, stale, or mistaken if public data changes or local references do not cover the user's case.

Mitigation: Verify actionable recommendations on the official "一网通办" page, through "随申办", or by calling 021-12345 before acting.

Risk: The package references a missing service_items.jsonl file, so item coverage may be incomplete unless the data is supplied or refreshed.

Mitigation: Refresh or provide the service item dataset before relying on broad coverage, and label low-confidence or unmatched required items as needing official verification.

Risk: Users may share unnecessary personal, medical, legal, or financial details while describing government service needs.

Mitigation: Ask only for the minimum high-level facts needed to route the request and avoid collecting sensitive details that are not required for department or item matching.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aibot88/skills/tongban)
- [Shanghai Government Online-Offline Service Portal](https://zwdt.sh.gov.cn/govPortals/index.do)
- [Shanghai One-Stop Service Index](artifact/references/index.md)
- [Shanghai Municipal Departments Reference](artifact/references/departments.json)
- [Required Service Items Reference](artifact/references/required-items.md)
- [Required Service Items Data](artifact/references/required_items.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Files]

**Output Format:** [Markdown response with ranked candidates, official URLs, online-handling indicators, and optional shell commands for reference-data refreshes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns 1-5 ranked service candidates when supported by reference data; asks a clarifying question or presents low-confidence candidates when matches are weak.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
