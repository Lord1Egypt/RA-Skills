## Description: <br>
A constrained browser automation skill for web navigation, screenshots, public data extraction, and testing when safety boundaries are enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[janewert](https://clawhub.ai/user/janewert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to automate browser navigation, page inspection, capture workflows, form interactions, and public web data extraction. It is intended for authorized targets with domain allowlists, action policies, and output limits configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad browser automation beyond a safe public-page reader, including navigation, interaction, authenticated sessions, script execution, local file access, proxy use, uploads, downloads, and capture workflows. <br>
Mitigation: Use strict domain allowlists and action policies, review proposed commands before execution, and grant only the browser capabilities required for the task. <br>
Risk: Cookies, saved sessions, screenshots, PDFs, videos, text captures, downloads, and trace files may contain sensitive information. <br>
Mitigation: Avoid saved authenticated sessions unless necessary, encrypt or clean state files, store generated artifacts in controlled locations, and treat captures as sensitive data. <br>
Risk: Proxy rotation, uploads, local file access, and automation of authenticated sites can be misused against unauthorized systems or data. <br>
Mitigation: Use these features only for authorized targets, keep action policy restrictions enabled, and block local file access or uploads unless the workflow explicitly requires them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/janewert/testsafe) <br>
- [Command Reference](references/commands.md) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>
- [Profiling](references/profiling.md) <br>
- [Proxy Support](references/proxy-support.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with inline bash commands, shell templates, and generated browser artifacts such as screenshots, PDFs, text captures, videos, traces, and state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser output can include sensitive page content, cookies, saved state, downloaded files, screenshots, PDFs, videos, and trace files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
