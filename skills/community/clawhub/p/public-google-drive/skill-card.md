## Description: <br>
Create public Google Docs and Google Sheets through Memyard without requiring Google OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[memyard](https://clawhub.ai/user/memyard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to create, append to, inspect, and share public Google Docs or Sheets hosted in Memyard's workspace without a Google sign-in flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents created through this skill are public to anyone with the link. <br>
Mitigation: Do not use the skill for secrets, confidential business information, regulated personal data, or private notes unless public link viewing is acceptable. <br>
Risk: The skill stores a local Memyard service key in the user's home directory. <br>
Mitigation: Keep the per-user config file protected and remove ~/.memyard/agent_config.json if the service is no longer used. <br>


## Reference(s): <br>
- [ClawHub listing: Public Google Drive](https://clawhub.ai/memyard/public-google-drive) <br>
- [Memyard Drive API base URL](https://api.memyard.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates public, link-viewable document or spreadsheet content through a plan-then-execute workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
