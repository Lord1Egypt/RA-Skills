## Description:

Monitor computer activities via periodic screenshots, extract text with OCR, and generate daily review reports with ROI analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drpris](https://clawhub.ai/user/drpris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to monitor macOS screen activity, extract text from captured screenshots, and generate daily productivity review reports with time allocation, ROI analysis, and suggested next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Continuous screenshot capture and OCR can collect sensitive screen content.

Mitigation: Install only when continuous monitoring is intended, grant macOS permissions deliberately, expand the app blacklist, use pause/resume for sensitive sessions, and disable OCR when text capture is unnecessary.

Risk: Logs and reports can preserve window titles, OCR samples, and derived activity history indefinitely.

Mitigation: Review the ~/.screen-reviewer directory regularly and delete logs or reports that are no longer needed; screenshot cleanup does not remove all retained history.

Risk: Cloud AI report generation may send derived activity summaries, window titles, and OCR samples to external providers.

Mitigation: Use local Ollama for sensitive work or only configure cloud API keys after accepting the data-sharing implications.

## Reference(s):

- [Screen Reviewer ClawHub page](https://clawhub.ai/drpris/skills/screen-reviewer)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Daily review prompt template](artifact/templates/review_prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, terminal command output, JSONL activity logs, YAML configuration, and operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can create local screenshots, logs, reports, configuration files, and launchd service definitions under user-controlled paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
