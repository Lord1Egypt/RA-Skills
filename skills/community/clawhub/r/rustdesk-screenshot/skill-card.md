## Description: <br>
Launches the RustDesk remote desktop client on Windows, prepares a screenshot directory, captures a full-screen screenshot, and returns the screenshot path as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nontrace](https://clawhub.ai/user/nontrace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate launching RustDesk and capturing a Windows desktop screenshot when remote access context or the current RustDesk screen needs to be shared. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full-screen screenshots may expose passwords, RustDesk temporary credentials, or private content. <br>
Mitigation: Review the desktop before capture and avoid using the skill when secrets or private information are visible. <br>
Risk: The configured screenshot directory can be cleared before capture. <br>
Mitigation: Use a dedicated screenshot directory and do not point SCREENSHOT_DIR at an important folder. <br>
Risk: RUSTDESK_PATH can point to a different executable than the default RustDesk client. <br>
Mitigation: Override RUSTDESK_PATH only with a trusted RustDesk executable path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nontrace/rustdesk-screenshot) <br>
- [Server-resolved GitHub provenance](https://github.com/yaohx-star/rustdesk-screenshot.git) <br>
- [Publisher profile](https://clawhub.ai/user/nontrace) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration] <br>
**Output Format:** [PNG screenshot file plus JSON status output containing the screenshot path or error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses optional RUSTDESK_PATH, SCREENSHOT_DIR, and WAIT_SECONDS environment variables; intended for Windows with Python and Pillow.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
