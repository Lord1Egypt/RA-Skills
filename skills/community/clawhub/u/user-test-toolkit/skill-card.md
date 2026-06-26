## Description: <br>
A user-testing toolkit for web apps that helps agents add behavior tracking, milestone-based task guidance, checkpoint surveys, SUS/EV/NPS questionnaires, and SAM emotion assessments to usability testing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ildar981105-create](https://clawhub.ai/user/ildar981105-create) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and user researchers use this skill to instrument web pages for usability tests, collect user behavior timelines, and embed task-based surveys during real product flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolkit can collect detailed behavior and survey data without built-in privacy controls. <br>
Mitigation: Use it only on intended test sites, add a clear privacy notice or consent step, and define retention and deletion rules before collecting real-user data. <br>
Risk: Collected events are sent to a configured analytics endpoint. <br>
Mitigation: Configure only a trusted HTTPS endpoint and restrict collection to pages that do not expose sensitive data. <br>
Risk: File names and free-text survey responses may contain personal or sensitive information. <br>
Mitigation: Avoid collecting filenames and free text unless necessary, and review survey prompts to minimize sensitive data entry. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ildar981105-create/user-test-toolkit) <br>
- [README](README.md) <br>
- [Survey configuration reference](references/survey-spec.md) <br>
- [Tracker API reference](references/tracker-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with HTML and JavaScript configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser-side tracker and survey integration guidance for an agent to apply to a target web application.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
