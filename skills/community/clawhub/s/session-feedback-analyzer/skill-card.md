## Description:

Parse Claude Code session JSONL to extract implicit user feedback signals, detect skill invocations, classify user responses within a 3-turn influence window, and compute per-skill correction_rate metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze Claude Code session logs, identify skills with frequent user corrections, and produce feedback.jsonl signals for an improvement pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad session scans can collect more Claude Code history than intended.

Mitigation: Run with a narrow --session-dir or --skill-filter that targets only the sessions or skill under review.

Risk: feedback.jsonl and archived feedback files may contain copied user-message text.

Mitigation: Use --no-snippets, write output outside shared repositories, and review or delete feedback-store archives after analysis.

Risk: Heuristic feedback classification can mislabel ambiguous user responses.

Mitigation: Treat correction_rate and hotspot reports as prioritization signals that require review before they drive skill changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/session-feedback-analyzer)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, JSONL files, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with bash and Python examples; analyzer scripts produce JSONL feedback events and plain-text metric reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output may include user-message snippets unless --no-snippets is used.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
