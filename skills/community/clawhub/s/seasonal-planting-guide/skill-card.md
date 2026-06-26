## Description: <br>
Provides monthly, zone-specific planting schedules, plant details, and custom entries to help gardeners plan seasonal crops year-round. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johstracke](https://clawhub.ai/user/johstracke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External gardeners, small farmers, and garden-planning agents use this skill to identify what to plant by month and USDA hardiness zone, inspect plant details, add local custom entries, and optionally export a planting calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom plant names and notes are saved locally under ~/.openclaw/workspace. <br>
Mitigation: Avoid entering sensitive information in custom plant names or notes, and review local files before sharing workspace data. <br>
Risk: Calendar export can create or overwrite a local Markdown file at the path the user chooses. <br>
Mitigation: Review the export path before running the command and keep exports within intended workspace, home, or temporary directories. <br>


## Reference(s): <br>
- [Seasonal Planting Guide on ClawHub](https://clawhub.ai/johstracke/seasonal-planting-guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output and optional Markdown calendar export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save custom plant data locally under ~/.openclaw/workspace and may write a Markdown export to a user-selected safe path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
