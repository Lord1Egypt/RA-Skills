## Description: <br>
Maps Chinese historical cases to realistic decision questions and produces structured situation judgment, historical comparisons, key variables, optional paths, sandbox simulation, transferable principles, and boundary reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greatxiaory](https://clawhub.ai/user/greatxiaory) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for structured history-based analysis of organization, business, team strategy, reform, alliance, leadership, control-rights, and similar decision questions. It can also help agents add sourced historical cases to a local case library after user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated historical analogies may be mistaken for reliable predictions or direct strategy instructions. <br>
Mitigation: Treat outputs as structured decision support, preserve the skill boundary reminders, and require human judgment before acting. <br>
Risk: User-added cases can persist sensitive private details in data/user_cases.json. <br>
Mitigation: Review generated case JSON before saving and omit confidential, personal, or unnecessary operational details. <br>
Risk: Organizational-control guidance can be misused as tactical direction in sensitive governance situations. <br>
Mitigation: Use the output for lawful governance and risk analysis, not as a substitute for professional, legal, financial, or employment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/greatxiaory/yi-shi-wei-jian) <br>
- [Skill homepage](https://github.com/GreatXiaoRY/LearnFromHistory-skill) <br>
- [README](README.md) <br>
- [Safety boundary prompt](prompts/safety_boundary.md) <br>
- [Case schema](data/cases.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown sections with optional JSON case records and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a fixed Chinese section structure and may persist reviewed user-supplied cases to data/user_cases.json.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
