## Description: <br>
Generate, review, debug, and refactor Python, JavaScript/TypeScript, Go, Rust, Java, and C/C++ code with syntax checks and optional tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate working code, review existing code, debug reported errors, and refactor code while receiving verification commands or results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace files and code snippets may be sent to api.evolink.ai for analysis and generation. <br>
Mitigation: Use the skill only with explicit user consent, avoid repositories containing secrets or confidential information, and prefer a sandbox or test repository for sensitive work. <br>
Risk: Verification commands and tests may execute local project code. <br>
Mitigation: Review commands before execution and run the skill in a trusted or sandboxed environment. <br>
Risk: Example authentication code is not production hardened. <br>
Mitigation: Replace demo secrets, disable debug mode, and harden authentication and storage before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EvoLinkAI/verified-code) <br>
- [EvoLink publisher profile](https://clawhub.ai/user/EvoLinkAI) <br>
- [Evolink API reference](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=code-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, command examples, verification output, and concise explanations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local syntax checks or tests and may require EVOLINK_API_KEY for external API use.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
