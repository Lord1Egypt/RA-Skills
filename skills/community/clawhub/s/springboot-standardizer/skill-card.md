## Description: <br>
Analyzes and standardizes SpringBoot + MyBatis projects by identifying structure issues, recommending migrations, and generating conventional layers plus MyBatis, Redis, and Kafka templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davieyang](https://clawhub.ai/user/davieyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect non-standard SpringBoot + MyBatis projects, plan refactors, and generate a conventional project structure with standard configuration templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Redis configuration includes an unsafe deserialization pattern. <br>
Mitigation: Replace the generated Redis serializer with a safer typed or restricted serialization approach before using it in production. <br>
Risk: Project analysis and scaffolding can affect files in a target project path. <br>
Mitigation: Run the skill against a version-controlled or disposable project path and review diffs before keeping generated files. <br>


## Reference(s): <br>
- [Kafka configuration template](references/kafka-config.md) <br>
- [MyBatis configuration guide](references/mybatis-config.md) <br>
- [Java SpringBoot naming conventions](references/naming-conventions.md) <br>
- [Redis configuration template](references/redis-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated SpringBoot project files or configuration templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files and refactor recommendations should be reviewed before adoption.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
