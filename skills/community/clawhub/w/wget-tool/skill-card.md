## Description: <br>
Download files from the web via HTTP/HTTPS/FTP with resume support, recursive mirroring, rate limiting, and progress feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch files or datasets from web URLs during automation. It is suited to simple downloads, with supported options verified before relying on wget-style behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download untrusted remote content to local paths. <br>
Mitigation: Use trusted URLs, choose safe output directories, and review downloaded content before using it. <br>
Risk: The documented command and wget-style options do not match the included implementation. <br>
Mitigation: Confirm the installed entrypoint and supported options before relying on resume, recursion, rate limiting, custom headers, or JSON output. <br>
Risk: Custom header examples may encourage passing sensitive credentials to remote services. <br>
Mitigation: Avoid long-lived secrets in headers and prefer short-lived, scoped credentials when authentication is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/wget-tool) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, shell commands] <br>
**Output Format:** [Downloaded file plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network and filesystem side effects depend on the URL and output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
