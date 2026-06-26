## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaowl1023](https://clawhub.ai/user/zhaowl1023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to drive browser-based workflows for UI testing, structured page inspection, data extraction, form filling, screenshots, PDFs, recordings, and session-based automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can expose cookies, local storage, saved sessions, screenshots, PDFs, recordings, traces, or other sensitive browser artifacts. <br>
Mitigation: Use test accounts or dedicated browser sessions, avoid printing cookies or storage values, keep saved state files such as auth.json out of repositories, and delete generated browser artifacts when no longer needed. <br>
Risk: Full browser automation can perform actions such as form submissions, uploads, network routing, and JavaScript evaluation against live pages. <br>
Mitigation: Review target URLs and proposed actions before execution, prefer staging environments or low-privilege accounts, and confirm destructive or externally visible actions before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaowl1023/wskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline bash commands and structured command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce browser snapshots, JSON output, screenshots, PDFs, videos, traces, and saved session state files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
