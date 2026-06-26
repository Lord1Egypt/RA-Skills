## Description: <br>
Run stopwatch, timer, and lap tracking with precision in terminal. Use when timing tasks, checking durations, running countdowns, analyzing splits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other terminal users can use this skill to run shell-based time-entry, history, search, stats, and export workflows. Security evidence says the artifacts behave mainly as a persistent local text logbook rather than a true stopwatch or countdown timer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a stopwatch/timer, but server security evidence says the artifacts mainly implement persistent local text logging with search and history behavior. <br>
Mitigation: Install only when a local timestamped logbook is acceptable, and do not rely on it as a precise stopwatch or countdown timer without separate validation. <br>
Risk: Entered text is stored locally under ~/.local/share/stopwatch and can be redisplayed, searched, or exported later. <br>
Mitigation: Avoid entering secrets, credentials, private notes, or sensitive operational details; review and remove local log files when retention is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ckchzh/stopwatch) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output and file-based logs or exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local log and export files under ~/.local/share/stopwatch.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
