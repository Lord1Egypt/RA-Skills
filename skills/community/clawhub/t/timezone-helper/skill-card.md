## Description: <br>
Timezone Helper converts times, shows world clocks, plans meetings across time zones, and provides DST guidance using built-in IANA timezone data for 200+ cities without APIs or scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to convert times, check world clocks, plan meetings across regions, and reason about DST-sensitive scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DST-sensitive timezone guidance can become outdated because the skill relies on static reference data. <br>
Mitigation: For important scheduling, legal, or business deadlines, verify results against a current authoritative timezone source. <br>
Risk: Ambiguous abbreviations or partial place names can map to the wrong timezone. <br>
Mitigation: Clarify ambiguous inputs such as IST or CST before giving a final conversion. <br>


## Reference(s): <br>
- [City to IANA Timezone Mapping](references/cities.md) <br>
- [ClawHub skill page](https://clawhub.ai/ToBeWin/timezone-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style text with time conversions, world clock tables, meeting options, and DST notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline reference guidance with no code execution, credential access, persistence, or data transmission.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
