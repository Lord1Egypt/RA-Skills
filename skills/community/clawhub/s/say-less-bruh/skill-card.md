## Description: <br>
Compresses assistant replies into short, natural, human-sounding chunks without dropping critical context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jakeacp](https://clawhub.ai/user/jakeacp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill when they want an assistant to keep responses brief, conversational, and minimally formatted while preserving critical warnings, blockers, commands, code, and configuration details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ordinary requests such as "keep it short" can enable brief-response mode for the rest of the conversation, which may reduce detail unexpectedly. <br>
Mitigation: Tell the assistant to disable SLB, turn off brief mode, or provide a full response when detailed guidance is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jakeacp/say-less-bruh) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Publisher profile](https://clawhub.ai/user/jakeacp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Short plain-text or Markdown assistant replies, normally prefixed with SLB when the mode is active] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 1 to 2 sentences and caps normal replies at 5 sentences unless more detail is needed for correctness or safety.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
