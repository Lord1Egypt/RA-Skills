## Description: <br>
Smart token cost optimization for OpenClaw that reduces AI token consumption through context compression, semantic caching, and adaptive optimization while maintaining response quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzming9](https://clawhub.ai/user/jzming9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to reduce token usage and API costs in long conversations by compressing older context, caching similar queries, and reporting savings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically rewrites and caches chat context, which can affect data handling for sensitive conversations. <br>
Mitigation: Use only for conversations where automatic compression and caching are acceptable; avoid sensitive content unless the publisher documents cache retention and scope. <br>
Risk: The optimization behavior depends on the unprovided @token-saver/core package. <br>
Mitigation: Review the publisher-provided core source or pinned dependency details before relying on the skill in production. <br>
Risk: Context compression may omit details that are important for precision-critical work. <br>
Mitigation: Use quality-priority mode for debugging, code review, and tasks where full context retention is required. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jzming9/token-saver-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jzming9) <br>
- [OpenClaw plugin manifest schema](https://clawhub.io/schemas/plugin-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text command responses with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces status reports, savings estimates, mode-change confirmations, cache information, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
