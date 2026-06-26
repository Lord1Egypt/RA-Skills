## Description: <br>
Shipcheck helps agents run the @symbolstar/shipcheck CLI before publishing npm packages, OpenClaw skill folders, or git repos to catch personal information leaks, secrets, private infrastructure details, codenames, and oversized binary files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[symbolstar](https://clawhub.ai/user/symbolstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill before publishing packages, skills, or public repositories to run a best-effort check for personal information, credentials, private infrastructure details, codenames, and large binary files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external npm CLI. <br>
Mitigation: Install only if you trust the @symbolstar/shipcheck package and run it on the specific project intended for publication. <br>
Risk: Scan output may contain sensitive findings such as credentials or personal information. <br>
Mitigation: Keep raw scan output in trusted channels and rotate any real credentials the scan discovers. <br>
Risk: The scanner is best effort and is not a replacement for manual review or a full secret scanner. <br>
Mitigation: Use it as a pre-publish check alongside manual review and dedicated secret-scanning tools for higher-assurance releases. <br>


## Reference(s): <br>
- [Shipcheck on ClawHub](https://clawhub.ai/symbolstar/shipcheck) <br>
- [symbolstar publisher profile](https://clawhub.ai/user/symbolstar) <br>
- [@symbolstar/shipcheck npm package](https://www.npmjs.com/package/@symbolstar/shipcheck) <br>
- [Shipcheck public source mirror](https://github.com/SymbolStar/shipcheck) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scan triage guidance, exit-code interpretation, and suggested publish-blocking workflow steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
