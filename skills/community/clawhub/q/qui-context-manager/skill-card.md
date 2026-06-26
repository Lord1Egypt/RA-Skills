## Description: <br>
AI-powered context management for OpenClaw sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect session context usage, generate AI summaries, and compress long-running sessions while preserving backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and summarize OpenClaw session history, which may include sensitive conversation content. <br>
Mitigation: Install only where session-history access is acceptable and review generated summaries before using them to continue work. <br>
Risk: The --replace flow resets a session after creating a backup. <br>
Mitigation: Run the non-destructive summarize command first, verify the summary, and use --replace only for sessions that can be reset from the saved backup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quincygunter/qui-context-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; invoked workflows can create Markdown summaries and JSONL backups.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw gateway access, jq, and SKILLBOSS_API_KEY for AI summarization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
