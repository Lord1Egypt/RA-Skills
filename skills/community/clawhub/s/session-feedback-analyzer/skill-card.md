## Description: <br>
Parses Claude Code session JSONL to detect skill invocations, classify nearby user responses, and compute per-skill correction metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to mine Claude Code session logs for implicit feedback, identify skills with high correction rates, and produce feedback.jsonl for improvement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The analyzer reads local Claude Code session history and may process more project history than intended. <br>
Mitigation: Run it with a narrow --session-dir and --skill-filter so analysis is limited to the intended session set or skill. <br>
Risk: Generated feedback files may contain user-message excerpts and project history. <br>
Mitigation: Use --no-snippets when possible and treat feedback-store/feedback.jsonl and archived feedback files as sensitive local artifacts. <br>
Risk: Keyword and 3-turn-window heuristics can misclassify or miss some feedback signals. <br>
Mitigation: Use minimum sample thresholds, review representative events before acting on a trend, and treat correction-rate changes as directional signals. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/lanyasheng/session-feedback-analyzer) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, JSONL files, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python examples; generated feedback events are JSON Lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default analysis reads ~/.claude/projects and writes feedback-store/feedback.jsonl; --no-snippets, --session-dir, and --skill-filter narrow collected output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
