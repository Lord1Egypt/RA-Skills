## Description: <br>
Searches, reviews, and installs skills from skill4agent.com using CLI commands or HTTPS API calls, with Chinese-language support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[osulivan](https://clawhub.ai/user/osulivan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find relevant skills, inspect their details, and install selected skills from skill4agent.com. It supports CLI-based workflows through npx and direct HTTPS API workflows when Node.js is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide installation of remote skills that persist locally and may affect future agent sessions. <br>
Mitigation: Install only trusted skills, review skill details before installation, and inspect any script warnings before allowing installation. <br>
Risk: Candidate skills may include scripts or sensitive code flagged by skill4agent metadata. <br>
Mitigation: Require user approval before installing flagged skills and recheck the reported script locations after installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/osulivan/skill4agent-cn) <br>
- [Publisher profile](https://clawhub.ai/user/osulivan) <br>
- [skill4agent source site](https://www.skill4agent.com) <br>
- [skill4agent npm package](https://www.npmjs.com/package/skill4agent) <br>
- [skill4agent API](https://skill4agent.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API URLs, and JSON-oriented result handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce skill search summaries, candidate recommendations, installation commands, and security-review guidance for downloaded skills.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
