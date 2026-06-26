## Description: <br>
Generate complete, image-rich travel plans from trip dates and destination, including day-by-day itinerary, transportation, lodging area guidance, budget ranges, local transit notes, and risk and backup plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daiwk](https://clawhub.ai/user/daiwk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel planners use this skill to turn destinations, exact dates, traveler preferences, budget, pace, and interests into structured Markdown trip plans. It is intended to support itinerary drafting that is later enriched with current travel facts from primary sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates Markdown itinerary files in the current working directory. <br>
Mitigation: Review the chosen output path before running the script; the artifact restricts outputs to .md files under the current working directory. <br>
Risk: Travel links, dates, opening hours, schedules, visa rules, weather, and pricing can become stale or inaccurate. <br>
Mitigation: Verify time-sensitive facts during the current run using primary sources and keep the verification log with source and checked date. <br>
Risk: User-provided travel details or links may contain sensitive information or unsafe URL schemes. <br>
Mitigation: Avoid providing booking credentials or private account details, keep user text plain, and use only trusted HTTPS image URLs. <br>


## Reference(s): <br>
- [Travel Research Checklist](references/research-checklist.md) <br>
- [Output Specification](references/output-spec.md) <br>
- [Travel Itinerary Planner on ClawHub](https://clawhub.ai/daiwk/travel-itinerary-planner) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown itinerary draft with tables, checklists, image links, and placeholder fields for verified travel facts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script writes a .md file inside the current working directory and validates image URLs as HTTPS.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
