## Description: <br>
Korean SRT (Super Rapid Train) search, reservation, and booking management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khj809](https://clawhub.ai/user/khj809) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search Korean SRT trains, make reservations, monitor for canceled seats, list reservations, and cancel reservations. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SRT account credentials and can manage real train reservations. <br>
Mitigation: Install only for trusted use, keep SRT_PHONE and SRT_PASSWORD private, and verify train or reservation details before booking or canceling. <br>
Risk: Monitoring can post reservation details to Discord. <br>
Mitigation: Use private Discord channels and avoid sharing reservation IDs unless they are necessary for the workflow. <br>
Risk: The stop command can terminate a process identified by a user-writable PID file. <br>
Mitigation: Store PID files in a private directory and confirm the process status before stopping a monitoring job. <br>
Risk: Long-running monitoring can repeatedly attempt reservations. <br>
Mitigation: Set short monitoring timeouts and review logs for success, timeout, or unexpected process termination. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/khj809/srt) <br>
- [SRTrain on PyPI](https://pypi.org/project/SRTrain) <br>
- [SRTrain Source Reference](https://github.com/ryanking13/SRT) <br>
- [SRT Online Service](https://etk.srail.kr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, uv, SRT_PHONE, and SRT_PASSWORD; reservation and monitoring flows can write private cache, log, and PID files.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
