## Description: <br>
Spec Engine automates project specification generation, validation scoring, task decomposition, dashboard reporting, version comparison, and historical analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yj85814](https://clawhub.ai/user/yj85814) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent teams use this skill to turn project ideas into structured specs, validate spec completeness, decompose accepted specs into tasks, compare versions, and generate analysis or dashboard reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package contains undocumented news collection scripts that make outbound web requests to public websites. <br>
Mitigation: Review the package before installing and remove or ignore the daily_news and collectors files if news collection is not needed. <br>
Risk: The news collection code uses ambient proxy environment variables. <br>
Mitigation: Run the skill in an environment with explicit network and proxy controls when using or inspecting those scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yj85814/spec-engine) <br>
- [Spec template](templates/spec-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, HTML, and command-line text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce spec documents, validation scores, task breakdowns, comparison reports, historical analysis, and static dashboard files.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
