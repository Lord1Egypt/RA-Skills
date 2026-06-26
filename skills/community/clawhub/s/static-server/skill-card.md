## Description: <br>
Start a local HTTP server to preview static HTML pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujintao-2021](https://clawhub.ai/user/liujintao-2021) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to start a local Python HTTP server for previewing static HTML files, testing browser-accessible pages, and working around file:// restrictions in browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The preview server listens on all network interfaces and could expose the served folder beyond localhost. <br>
Mitigation: Prefer changing the server to bind to 127.0.0.1 and run it only for the duration of local testing. <br>
Risk: Serving a directory that contains secrets, credentials, private documents, or .env files could disclose sensitive files. <br>
Mitigation: Serve only minimal test directories that have been checked for sensitive content before starting the server. <br>


## Reference(s): <br>
- [Static Server on ClawHub](https://clawhub.ai/liujintao-2021/static-server) <br>
- [Publisher profile: liujintao-2021](https://clawhub.ai/user/liujintao-2021) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and localhost URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a localhost preview URL, the served directory, and stop instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
