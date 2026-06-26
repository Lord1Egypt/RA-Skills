## Description: <br>
Automatically generate session summaries and save to Obsidian. Use at session end to capture decisions, progress, and next actions. Triggers on "セッション終了", "サマリー", "今日の成果", "終わり". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taka3693](https://clawhub.ai/user/taka3693) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill at the end of a work session to capture decisions, progress, next actions, and changed files as an Obsidian daily note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session summaries can store secrets, sensitive project details, or private work context in local Obsidian notes. <br>
Mitigation: Use explicit summary commands, review the configured vault path, and avoid saving sessions containing sensitive information unless local note retention is acceptable. <br>
Risk: A fixed Obsidian vault path may write summaries to an unintended local location if reused across machines. <br>
Mitigation: Confirm or update the vault path and daily notes folder before relying on saved summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taka3693/session-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files] <br>
**Output Format:** [Markdown session summary saved to an Obsidian daily notes folder] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes session timing, key decisions or achievements, progress, next actions, and modified files when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
