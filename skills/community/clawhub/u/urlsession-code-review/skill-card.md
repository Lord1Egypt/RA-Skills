## Description: <br>
Reviews URLSession networking code for iOS/macOS, covering async/await patterns, request building, error handling, caching, and background sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review iOS and macOS networking code that uses URLSession, URLRequest, URLCache, HTTPURLResponse, or URLError. It helps structure findings around response validation, resource handling, configuration, background transfers, and security-sensitive request construction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce incorrect or incomplete review findings if the relevant URLSession handler, delegate, or helper implementation is not visible. <br>
Mitigation: Require findings to cite file and line evidence, and mark missing handlers or lifecycle details as unknown instead of assuming behavior. <br>
Risk: Agent-proposed fixes for networking, uploads, caching, or secret handling can change application behavior or security posture. <br>
Mitigation: Review and test any generated code changes before applying them to an iOS or macOS project. <br>


## Reference(s): <br>
- [URLSession Async/Await Reference](references/async-networking.md) <br>
- [URLRequest Building Reference](references/request-building.md) <br>
- [URLSession Error Handling Reference](references/error-handling.md) <br>
- [URLSession Caching and Configuration Reference](references/caching.md) <br>
- [Apple URLSession cache response documentation](https://developer.apple.com/documentation/foundation/urlsessiondatadelegate/urlsession(_:datatask:willcacheresponse:completionhandler:)) <br>
- [ClawHub release page](https://clawhub.ai/anderskev/urlsession-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, guidance] <br>
**Output Format:** [Markdown review findings with file and line references and concise remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are organized by severity and should cite the reviewed source files when reporting issues.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
