## Description: <br>
Manages a three-layer OpenClaw memory system with LanceDB Pro autoCapture and autoRecall, scheduled micro-sync, daily summaries, weekly compaction, scope isolation, deduplication, and archive workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylin19860916](https://clawhub.ai/user/kylin19860916) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to configure an agent memory workflow that captures, recalls, summarizes, compacts, and scopes long-term conversation memory across hot, warm, and cold layers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring memory jobs can scan, summarize, retain, and recall conversation history without clear retention or sensitive-data controls. <br>
Mitigation: Enable the skill only when long-term memory is intentional, define what must never be stored, and maintain a process to inspect and delete saved memories. <br>
Risk: Scheduled tasks may lead to changes in MEMORY.md, SYSTEM_GUIDE.md, or other persistent agent guidance. <br>
Mitigation: Require approval before scheduled tasks modify persistent guidance, and review HEARTBEAT.md tasks before they are acted on. <br>
Risk: Auto-captured memories can include low-value, duplicate, or cross-scope content. <br>
Mitigation: Use the artifact's deduplication, scope isolation, autoCapture review, and weekly scope audit steps before relying on recalled memory. <br>


## Reference(s): <br>
- [AGENTS.md memory rules template](artifact/references/agents-rules.md) <br>
- [ClawHub skill page](https://clawhub.ai/kylin19860916/three-layer-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates scheduled memory maintenance tasks that append to HEARTBEAT.md and guide updates to MEMORY.md, second-brain summaries, and archive files.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
