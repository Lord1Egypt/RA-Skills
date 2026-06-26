## Description: <br>
Generates Waze navigation links for addresses, establishment names, and calendar-event locations, including resolving vague destinations against the user's city before producing the link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dicasdomaroto-maker](https://clawhub.ai/user/dicasdomaroto-maker) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and assistants use this skill to create clean, clickable Waze route links for conversations and morning briefings. It is intended for navigation requests involving specific addresses, establishment names, or calendar locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved profile location and calendar-event location text can be sensitive. <br>
Mitigation: Use full addresses manually for sensitive appointments and avoid sending vague destination searches when privacy matters. <br>
Risk: Vague destination requests may be resolved through an external search provider and can identify the wrong nearby location. <br>
Mitigation: Confirm the user's city, include state and country in generated addresses, and present options when multiple plausible matches exist. <br>


## Reference(s): <br>
- [ClawHub Waze skill page](https://clawhub.ai/dicasdomaroto-maker/waze) <br>
- [Publisher profile](https://clawhub.ai/user/dicasdomaroto-maker) <br>
- [Waze deep link format used by the skill](https://waze.com/ul?q=ENDERECO_CODIFICADO&navigate=yes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown link with concise destination text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a clickable Waze URL and may include resolved destination details when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
