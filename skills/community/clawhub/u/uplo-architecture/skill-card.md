## Description: <br>
AI-powered architecture knowledge management for searching building designs, code compliance records, project specifications, and BIM data with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Architecture teams and agents use this skill to search firm knowledge, verify project facts, find subject matter experts, retrieve directives, and ground answers in building design, code compliance, project specification, and BIM records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive organizational architecture data, including confidential project or agreement information. <br>
Mitigation: Install only with a scoped, revocable UPLO token and follow the documented classification tiers before sharing or exporting information. <br>
Risk: Conversation logging may capture project context without clear user consent or retention controls. <br>
Mitigation: Confirm organizational approval for conversation logging and avoid logging sensitive details unless policy permits it. <br>
Risk: Full organizational context export can expose more internal knowledge than a specific task requires. <br>
Mitigation: Use targeted search tools first and reserve full context export for explicitly approved workflows. <br>
Risk: The skill depends on an external MCP server package and UPLO instance configuration. <br>
Mitigation: Vet or pin the MCP server package and configure the UPLO endpoint and token according to internal security review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-architecture) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a scoped UPLO MCP token and source citation when sharing UPLO information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
