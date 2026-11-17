## Description: <br>
Remix认证工具 helps developers and operations teams configure, store, and verify Remix Bearer API keys for server-side API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to set up REMIX_API_KEY, test Remix API connectivity, and troubleshoot Bearer-token authentication in development or CI environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad read, write, and exec authority while its intended purpose is API-key setup and connectivity checks. <br>
Mitigation: Limit use to Remix API-key setup and connectivity checks, review proposed file and command actions before execution, and avoid unrelated file, command, import/export, reset, or delete operations. <br>
Risk: Real API keys could be exposed if written into source files or committed to version control. <br>
Mitigation: Store REMIX_API_KEY in environment variables, local ignored .env files, or secret managers, and keep real keys out of source control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/remix-auth-tool-free) <br>
- [Remix API documentation](https://api.remix.gg/docs) <br>
- [Remix API key console](https://remix.gg/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, JavaScript, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference REMIX_API_KEY and Remix API endpoints; users should keep real API keys out of source control.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
