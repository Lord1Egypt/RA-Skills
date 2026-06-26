## Description: <br>
Agent Execution Guard by WorldLoops is a safe-by-default responsibility layer for AI agents that turns scattered work signals into governed open loops while preserving externalWrite:false. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swit001](https://clawhub.ai/user/swit001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to convert already-read work signals from tools such as Gmail, Calendar, Slack, GitHub, OpenClaw, or gog into governed open loops, proposals, approval decisions, local transitions, and receipts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local work-signal state can be stored under .worldloops. <br>
Mitigation: Review where .worldloops is created, protect or clean that directory as appropriate, and avoid running the skill on sensitive inbox or workspace data unless local storage is acceptable. <br>
Risk: Some commands can send signal content to the WorldLoops API. <br>
Mitigation: Configure WORLDLOOPS_API_BASE_URL and WORLDLOOPS_API_KEY intentionally, and review the input files before running commands that may transmit signal content. <br>
Risk: Telegram support is a live external integration. <br>
Mitigation: Use Telegram only with an intentionally configured bot token and chat, and treat delivered briefs as external messages rather than purely local demo output. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/swit001/worldloops) <br>
- [Project homepage](https://github.com/swit001/worldloops) <br>
- [README](README.md) <br>
- [Adapter Guide](ADAPTER_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and CLI text with JSON receipts and local state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local .worldloops state and receipt files; some commands can transmit signal content to the configured WorldLoops API.] <br>

## Skill Version(s): <br>
1.13.0 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
