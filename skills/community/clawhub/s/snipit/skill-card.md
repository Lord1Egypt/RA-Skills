## Description: <br>
Share code snippets and files via snipit.sh with AES-256 encryption, password protection, burn-after-read, auto-expiration, and CLI or curl workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homecity](https://clawhub.ai/user/homecity) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to share code, configuration snippets, logs, diffs, secrets, and build output through snipit.sh with optional password protection, burn-after-read behavior, and expiration settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared snippets, files, command output, logs, diffs, or configuration content are uploaded to the snipit.sh service. <br>
Mitigation: Review exactly what will be uploaded before running commands, redact sensitive values, and use password protection, burn-after-read, and short expirations for sensitive snippets. <br>
Risk: Installing and running the snipit CLI depends on trusting the snipit-sh npm package and the snipit.sh service. <br>
Mitigation: Install only when that package and service are approved for the environment where the agent is operating. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/homecity/snipit) <br>
- [Publisher profile](https://clawhub.ai/user/homecity) <br>
- [snipit-sh npm package](https://www.npmjs.com/package/snipit-sh) <br>
- [snipit.sh snippets API](https://snipit.sh/api/snippets) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that upload selected file, stdin, log, diff, or configuration content to the snipit.sh service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
