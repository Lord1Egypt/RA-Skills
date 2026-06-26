## Description: <br>
Compile SKILL.md files into runtime artifacts, verify freshness and health, and prepare portable publish-ready skill folders for ClawHub-style registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoyanji](https://clawhub.ai/user/shaoyanji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill maintainers use this skill to compile SKILL.md source files into runtime artifacts, check local compiler dependencies, and prepare skill folders for publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports missing helper scripts referenced by the skill. <br>
Mitigation: Verify helper scripts from a trusted source before installation or use. <br>
Risk: Compilation can broadly change skill runtime files. <br>
Mitigation: Run the compiler only on the intended skill directory and review generated file diffs before relying on them. <br>
Risk: Generic execute-style triggers and the publish command can be ambiguous if invoked without scope. <br>
Mitigation: Use exe, execute, and publish commands only when the requested action is explicit and scoped. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shaoyanji/skill-compiler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and generated skill artifact files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates SKILL.struct.json and SKILL.toon artifacts for each input SKILL.md.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
