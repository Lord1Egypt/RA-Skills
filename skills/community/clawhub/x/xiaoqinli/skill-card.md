## Description: <br>
Xiaoqinli helps agents write structured .xql.json AST files and compile them to Go, Rust, TypeScript, Kotlin, Swift, or Python with type, effect, and capability checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freecode100year](https://clawhub.ai/user/freecode100year) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create, validate, and compile .xql.json AST programs into common target languages. It is useful when an agent needs structured code generation guidance without relying on free-form source syntax. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to build and use an external xql binary. <br>
Mitigation: Review the linked Xiaoqinli source repository and build the binary only if you trust it. <br>
Risk: Generated source code may not match user intent or target-language safety expectations. <br>
Mitigation: Run xql validate, choose output paths deliberately, and inspect generated code before building or running it. <br>


## Reference(s): <br>
- [ClawHub Xiaoqinli Skill Page](https://clawhub.ai/freecode100year/xiaoqinli) <br>
- [Xiaoqinli Project Repository](https://github.com/Freecode100Year/xiaoqinli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown instructions with shell, JSON, and generated-code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides validation and compilation of .xql.json files; generated code should be inspected before building or running it.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
