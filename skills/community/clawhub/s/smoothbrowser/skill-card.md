## Description: <br>
Browser for AI agents to navigate websites, fill forms, extract web data, test web apps, and automate browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antoniocirclemind](https://clawhub.ai/user/antoniocirclemind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use SmoothBrowser to operate a Smooth CLI browser session for web navigation, authenticated workflows, form completion, data extraction, testing, file handling, and browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over web browsing, logins, uploaded files, JavaScript execution, downloads, and saved sessions. <br>
Mitigation: Prefer anonymous or read-only sessions, restrict allowed URLs when possible, avoid sensitive uploads unless necessary, and require explicit approval before submitting forms, posting content, purchasing, downloading private data, changing account settings, or reusing logged-in profiles. <br>
Risk: The release evidence security verdict is suspicious because approval boundaries are not sufficiently clear for high-impact browser actions. <br>
Mitigation: Review planned browser actions before execution and use profiles, live-view handoffs, and allowed URL constraints to keep automated actions within the user's intended scope. <br>


## Reference(s): <br>
- [Smooth application and API key portal](https://app.smooth.sh) <br>
- [SmoothBrowser ClawHub release](https://clawhub.ai/antoniocirclemind/smoothbrowser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, Code] <br>
**Output Format:** [Markdown with inline bash, JSON schema, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce browser session commands, structured extraction schemas, file-management commands, and JavaScript snippets for execution through Smooth CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
