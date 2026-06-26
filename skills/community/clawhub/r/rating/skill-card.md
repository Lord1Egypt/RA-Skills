## Description: <br>
Rating is a command-line utility for recording, searching, reporting, and exporting local rating activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and command-line users use Rating to save rating-related entries, view recent activity and statistics, search local logs, and export records as JSON, CSV, or text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered activity is stored locally under ~/.local/share/rating/ and may later be searchable or exportable. <br>
Mitigation: Avoid entering secrets, tokens, private paths, or sensitive personal content; periodically review or delete the local data directory if local privacy matters. <br>


## Reference(s): <br>
- [Rating on ClawHub](https://clawhub.ai/ckchzh/rating) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Plain text stdout with optional JSON, CSV, or text export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores activity locally under ~/.local/share/rating/ unless configured otherwise.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
