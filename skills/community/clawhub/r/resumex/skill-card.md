## Description: <br>
Auto Job Applying Agent manages a user's Resumex resume, searches for matching jobs, fills approved job application forms with local browser automation, and logs application outcomes to Resumex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atharva-badgujar](https://clawhub.ai/user/atharva-badgujar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers use this agent to manage a Resumex resume, find and rank job listings, submit selected applications, and track application status. It is also useful for resume updates, tailoring, and optional Telegram delivery of resume summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real job applications using personal resume data. <br>
Mitigation: Keep AUTO_APPLY_MODE=false, review the ranked job list, and approve only specific jobs before submission. <br>
Risk: Submitted applications and Resumex tracker entries may be difficult or impossible to undo. <br>
Mitigation: Test on one selected job first and confirm application details before allowing broader submission. <br>
Risk: The skill requires sensitive credentials, including a Resumex API key and optional Telegram token. <br>
Mitigation: Use a dedicated revocable Resumex API key, avoid Telegram delivery unless needed, and revoke credentials immediately if exposure is suspected. <br>
Risk: Local browser automation may be detected or blocked by job portals. <br>
Mitigation: Use transparent Playwright automation without stealth behavior and fall back to manual completion when a portal blocks automation or requires complex steps. <br>
Risk: Dependency installation downloads Playwright and a Chromium browser binary. <br>
Mitigation: Install dependencies in a virtual environment or sandbox before using auto-apply. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atharva-badgujar/resumex) <br>
- [Resumex](https://resumex.dev) <br>
- [Resumex API documentation](https://resumex.dev/api-docs) <br>
- [Privacy policy](artifact/PRIVACY.md) <br>
- [Security guide](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell command snippets and JSON helper results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESUMEX_API_KEY; optionally uses Telegram credentials and local Playwright browser automation.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
