## Description: <br>
Build your digital twin through conversation. Your AI learns who you are by talking to you - not by reading a form. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to build and maintain a local digital-twin profile through guided conversation. The agent interviews the user, writes a SOUL.md identity document, tracks onboarding progress, and evolves the profile when the user confirms updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store sensitive personal and workplace details in a persistent local profile. <br>
Mitigation: Avoid sharing secrets or confidential company information, review the generated SOUL.md and session files, and delete ~/.openclaw/data/second-me/ when the stored profile is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paul-leo/second-me) <br>
- [Publisher profile](https://clawhub.ai/user/paul-leo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown files and JSON progress records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores SOUL.md, progress.json, and conversation session files under ~/.openclaw/data/second-me/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
