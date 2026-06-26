## Description: <br>
Creates a structured summary when /new or /reset ends a session and archives it to memory/YYYY-MM-DD.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thelast0802](https://clawhub.ai/user/thelast0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users who frequently start or reset sessions use this hook to preserve a concise, structured record of the prior conversation for later continuation and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent session text may be sent to the model provider configured in the user's OpenClaw models.json. <br>
Mitigation: Use only trusted providers and scoped API keys, and avoid this hook for sessions containing secrets or regulated data. <br>
Risk: Generated memory files may retain sensitive conversation details locally. <br>
Mitigation: Periodically review or delete generated memory files according to the workspace's data retention needs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thelast0802/session-memory-structured) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown summary appended to a dated local memory file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a four-section session summary and stores it under memory/YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
