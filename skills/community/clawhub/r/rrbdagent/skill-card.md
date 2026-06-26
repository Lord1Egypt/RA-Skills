## Description: <br>
OpenClaw skill for RRBD Admin that helps users call RRBD backend APIs and automate account, digital-human, video, task, and finance operations through natural-language conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengjwmail](https://clawhub.ai/user/zengjwmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to interact with RRBD Admin through natural-language requests that map to authenticated API calls, including digital-human listing, video creation, account information, task workflows, and wallet or commission checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext credential storage or hardcoded account usage can expose RRBD account credentials. <br>
Mitigation: Remove hardcoded credentials, rotate any exposed password, and disable plaintext password persistence before use. <br>
Risk: The skill can perform real account actions such as video creation, deletion, withdrawal, or other authenticated operations. <br>
Mitigation: Require explicit confirmation before delete, withdrawal, video-creation, or other account-changing actions. <br>
Risk: Using the skill sends RRBD account data and video scripts to the configured backend service. <br>
Mitigation: Use only in environments where sending those credentials, scripts, and account data to the configured RRBD backend is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zengjwmail/rrbdagent) <br>
- [RRBD API base URL](https://rrbd20.yzidea.net/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown or plain text with optional JavaScript, Python, JSON configuration, shell commands, and API response summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform authenticated RRBD API operations and persist login details in local configuration unless changed before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
