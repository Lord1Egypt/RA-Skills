## Description: <br>
Detects topic switches in conversations and creates or manages context frames to maintain work-related context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shewingong](https://clawhub.ai/user/shewingong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to detect topic changes, start or manage context frames, and inspect a simulated conversation flow for context management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived summaries may be saved persistently in a local OpenClaw workspace file without a clear prompt. <br>
Mitigation: Review the storage behavior before installing; prefer a package-scoped or user-approved path and make persistence opt-in or easy to delete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shewingong/scenique-context-frame) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Plain text console output and JSON records for pending context frames] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The demo tool accepts a mode parameter; topic switches may persist conversation-derived summaries in a local OpenClaw workspace file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
