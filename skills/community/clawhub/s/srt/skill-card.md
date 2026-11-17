## Description:

Korean SRT (Super Rapid Train) search, reservation, and booking management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khj809](https://clawhub.ai/user/khj809)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search Korean SRT trains, make one-shot reservations, monitor for canceled seats, list reservations, and cancel reservations from an agent workflow.

### Deployment Geography for Use:

Global (service use is for Korean SRT routes).

## Known Risks and Mitigations:

Risk: The skill uses SRT account credentials and can make or cancel reservations under the user's account.

Mitigation: Run it only in a trusted environment, provide credentials through the documented environment variables, and review reservation or cancellation actions before execution.

Risk: Continuous monitoring can create long-running background processes, cron jobs, logs, and Discord reports containing booking details.

Mitigation: Use monitoring only with an explicit timeout, known log and Discord destinations, and cleanup steps for reporting and termination jobs.

Risk: Weak PID-file process control and an unpinned SRTrain dependency can affect process management and dependency trust.

Mitigation: Use only PID files created for the current run and prefer a pinned, reviewed SRTrain dependency version.

## Reference(s):

- [ClawHub SRT Skill Page](https://clawhub.ai/khj809/skills/srt)
- [SRT Skill Homepage](https://github.com/khj809/openclaw-srt-skill)
- [SRTrain PyPI Package](https://pypi.org/project/SRTrain)
- [SRTrain GitHub Repository](https://github.com/ryanking13/SRT)
- [SRT Booking Website](https://etk.srail.kr)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reservation identifiers, seat details, payment-required status, process status, log summaries, and exit codes.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
