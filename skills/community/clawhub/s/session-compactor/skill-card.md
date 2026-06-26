## Description: <br>
Session Compactor helps an agent reduce long conversation history into a structured summary while preserving recent messages, tool-call context, and key facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangbb-coder](https://clawhub.ai/user/fangbb-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to compact long OpenClaw sessions when conversation history approaches token limits. It can be invoked manually or configured for automatic compaction while retaining recent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included deploy.sh script can publish the local directory to a hardcoded GitHub repository. <br>
Mitigation: Review the artifact before installation and do not run deploy.sh unless that publishing behavior is intended. <br>
Risk: Session compaction is irreversible and can discard early-message detail. <br>
Mitigation: Use conservative token thresholds, keep enough recent messages, and avoid automatic compaction for sessions that require exact historical detail. <br>
Risk: The current summary generation uses heuristic extraction rather than model-quality summarization. <br>
Mitigation: Review compacted summaries for important decisions, tool results, and facts before relying on them as the only retained context. <br>


## Reference(s): <br>
- [Session Compactor architecture](references/architecture.md) <br>
- [ClawHub skill page](https://clawhub.ai/fangbb-coder/session-compactor) <br>
- [claw-code reference project](https://github.com/instructkr/claw-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result objects and Markdown session summaries, with setup guidance in Markdown and shell-command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Compaction is irreversible and token counts are heuristic estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
