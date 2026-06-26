## Description: <br>
Generates a structured report HTML based on a specific template for reports, slides, or summary cards from raw content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juguangyuan520-dotcom](https://clawhub.ai/user/juguangyuan520-dotcom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to turn raw report content into a responsive four-section HTML report and capture it as a screenshot when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unescaped report content can be rendered into local HTML and opened in a browser, creating a script-execution risk. <br>
Mitigation: Use trusted report content only, or update the generator to HTML-escape all user-supplied fields before rendering and screenshot capture. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juguangyuan520-dotcom/report-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [HTML file plus JSON status output and screenshot-capture guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local HTML reports from JSON input; screenshot capture is performed by the agent after generation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
