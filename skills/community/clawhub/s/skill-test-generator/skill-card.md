## Description: <br>
Automatically generate test documentation for existing skills that have scripts but lack testing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[834948655](https://clawhub.ai/user/834948655) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to inspect scripts in an existing skill and draft testing documentation, including test case tables, expected outcomes, and executable command examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated testing documentation may contain incorrect or incomplete expected behavior for a target skill. <br>
Mitigation: Review generated TESTING.md content or SKILL.md patches before applying or publishing them. <br>
Risk: Generated test commands may exercise untrusted or unsafe target scripts. <br>
Mitigation: Inspect target scripts before running generated commands, especially when the target skill comes from an untrusted source. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with test case tables and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a standalone TESTING.md draft or a testing section for SKILL.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
