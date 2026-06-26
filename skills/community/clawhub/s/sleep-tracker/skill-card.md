## Description: <br>
Sleep Tracker helps agents analyze sleep timing, suggest improvement steps, plan sleep schedules, optimize sleep environments, guide naps, and maintain sleep or wellness logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to log sleep and wellness activity, inspect recent entries, calculate sleep duration and cycle alignment, and receive sleep hygiene guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sleep, wellness, meal, exercise, or symptom notes may contain sensitive personal information, and the sleep journal script writes journal entries to /tmp/sleep_journal.txt. <br>
Mitigation: Use a private data directory for tracker logs, avoid entering sensitive notes in shared environments, and inspect or remove /tmp/sleep_journal.txt after use. <br>
Risk: Documented reset behavior may not fully clear stored tracker data. <br>
Mitigation: Manually verify and delete stored files in the configured tracker directory and temporary journal path when clearing data. <br>
Risk: Sleep and wellness suggestions are general guidance and may not address medical conditions. <br>
Mitigation: Treat the output as informational wellness support and seek qualified professional advice for persistent or serious sleep symptoms. <br>


## Reference(s): <br>
- [Sleep Tracker on ClawHub](https://clawhub.ai/bytesagain-lab/sleep-tracker) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Sleep Tracker Tips](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local text log files for sleep, wellness, command history, and journal entries.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
