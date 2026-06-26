## Description: <br>
Helps with the socket abstraction, socket options, blocking vs non-blocking I/O, and multiplexing (select, poll, epoll). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for guidance on socket APIs, socket options, blocking versus non-blocking I/O, I/O multiplexing, Unix domain sockets, and structuring TCP/UDP server code at the socket layer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network-facing code generated from socket guidance may be incorrect, insecure, or unsuitable for production without review. <br>
Mitigation: Review generated server and client code before production use, especially binding addresses, ports, timeouts, error handling, and socket lifecycle behavior. <br>
Risk: Hard-coded IP addresses, ports, or Unix socket paths can make deployments brittle or expose unintended interfaces. <br>
Mitigation: Use configuration or environment variables for network addresses, ports, and socket paths. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration instructions] <br>
**Output Format:** [Markdown with explanatory text, option tables, and language-specific examples when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable artifact output; generated network-facing code should be reviewed before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
