## Description: <br>
Runs a post-meeting workflow that scans eligible meetings, retrieves or accepts meeting transcripts, generates minutes and draft issues, writes them to Gitea, and prepares organizer notification details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill in scheduled ClawHub/OpenClaw workflows to process meeting records after a grace period, create reviewable minutes and draft issue files, update Gitea state, and prepare notification email payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Gitea repositories and meeting status across a broad repository scope. <br>
Mitigation: Use a least-privilege Gitea bot token and restrict the configured repositories the bot may modify. <br>
Risk: Meeting transcripts, attendee details, and organizer emails may be exposed through runner output, scan results, or logs. <br>
Mitigation: Run in a controlled environment, limit log retention and access, and review scan output handling before production use. <br>
Risk: Setup defaults may encourage insecure configuration, including non-HTTPS service URLs or untrusted environment sourcing. <br>
Mitigation: Require HTTPS-only Gitea URLs, pin dependencies, and review the local .env file before sourcing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/myd2002/skill-c-fetch-minutes) <br>
- [Publisher profile: myd2002](https://clawhub.ai/user/myd2002) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command responses plus Markdown meeting artifacts and email payload text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces transcript, optional AI summary, minutes, and draft issue content for Gitea submission.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
