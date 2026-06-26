## Description: <br>
Every 15 minutes, this OpenClaw cron skill scans for meetings scheduled 15 minutes to 6 hours ahead, coordinates Gitea activity reporting, prepares pre-meeting brief content, commits status updates, and returns email payloads for attendee distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to automate pre-meeting progress briefs for Gitea-managed projects. It scans eligible scheduled meetings, gathers repository activity, guides AI brief generation, stores meeting artifacts, updates meeting status, and prepares email content for attendees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unattended and scan or modify Gitea repositories. <br>
Mitigation: Install it with a dedicated least-privilege Gitea token and an explicit repository allowlist. <br>
Risk: The workflow can collect attendee emails and trigger automatic pre-meeting email distribution. <br>
Mitigation: Confirm organizational approval for attendee email use and automatic sending before enabling the cron workflow. <br>
Risk: Meeting identifiers and workflow logs may be written to a remote meta repository. <br>
Mitigation: Review data handling requirements and restrict log access before deployment. <br>
Risk: Gitea access over non-HTTPS configuration can expose repository data or credentials. <br>
Mitigation: Use HTTPS-only Gitea configuration and do not deploy with the sample HTTP endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skill-b-pre-brief) <br>
- [Publisher profile](https://clawhub.ai/user/myd2002) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command responses with Markdown instructions, shell command examples, and HTML email payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cron-oriented workflow; scan output includes meeting metadata and commit output includes brief_email fields for downstream email delivery.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
