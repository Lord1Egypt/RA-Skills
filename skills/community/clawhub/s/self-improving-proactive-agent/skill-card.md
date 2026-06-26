## Description: <br>
A unified OpenClaw skill that merges self-improvement and proactivity: learn from corrections, maintain active state, recover context fast, and keep work moving with clear boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yueyanc](https://clawhub.ai/user/Yueyanc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to give an agent a unified operating model for durable learning, active task state, context recovery, and useful follow-through. It is suited for multi-step work where corrections, preferences, blockers, and next moves should be tracked locally across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory and task-state notes can accidentally retain private context or secrets. <br>
Mitigation: Do not store credentials, tokens, or secrets in memory files, and review ~/self-improving/ and ~/proactivity/ periodically. <br>
Risk: Durable behavior rules can become misleading if they are learned from weak signals. <br>
Mitigation: Capture lessons from explicit corrections, explicit preferences, reflections, or repeated successful workflows; avoid learning from silence or assumptions. <br>
Risk: Proactive follow-through can cross user boundaries if treated as permission to act externally. <br>
Mitigation: Ask before sending messages, spending money, deleting data, publishing publicly, making commitments, or scheduling for others. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Yueyanc/self-improving-proactive-agent) <br>
- [Publisher profile](https://clawhub.ai/user/Yueyanc) <br>
- [README](artifact/README.md) <br>
- [Setup](artifact/setup.md) <br>
- [Boundaries](artifact/boundaries.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with local filesystem paths, checklists, and operating rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No required binaries are disclosed; the skill guides local memory and task-state file use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
