## Description: <br>
Fully conversational remote job finder for WhatsApp powered by Remote Rocketship. Uses rr_jobs_search tool (server-side RR_API_KEY) and supports pagination ("20 more"). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lior539](https://clawhub.ai/user/Lior539) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to find, browse, paginate, and monitor remote job listings in conversational chat. It collects job-search preferences, calls the rr_jobs_search tool, and returns concise WhatsApp-friendly listings with apply and company links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gateway extension uses a server-side Remote Rocketship API key. <br>
Mitigation: Keep RR_API_KEY on the OpenClaw server, do not ask users to paste secrets in chat, and restart the gateway after setting or rotating the key. <br>
Risk: The skill may remember job-search preferences and scheduled checks. <br>
Mitigation: Collect only the job-search preferences needed for matching and avoid storing or sharing unnecessary personal detail. <br>
Risk: Installing the server extension changes files under ~/.openclaw/extensions. <br>
Mitigation: Review the gateway extension before installing and back up existing ~/.openclaw/extensions files before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Lior539/remote-jobs-finder) <br>
- [Remote Rocketship](https://www.remoterocketship.com) <br>
- [Remote Rocketship OpenClaw Jobs API](https://www.remoterocketship.com/api/openclaw/jobs) <br>
- [README](artifact/README.md) <br>
- [Server Install Guide](artifact/INSTALL_SERVER.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, api calls, configuration, shell commands, guidance] <br>
**Output Format:** [WhatsApp-friendly Markdown text with bulleted job listings, status messages, and inline links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call rr_jobs_search with Remote Rocketship filters; defaults to 20 results per page and excludes full job descriptions unless requested.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
