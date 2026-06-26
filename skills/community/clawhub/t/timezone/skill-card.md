## Description: <br>
Convert times across world timezones and compare availability. Use when converting meetings, checking offsets, comparing zones, generating tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and terminal users can invoke this skill for timezone-related command-line workflows, including recording convert, compare, analyze, and export actions. Review outputs carefully because the security scan says the script mainly stores user input in local logs instead of performing timezone calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a timezone converter, but server security evidence says the script mainly logs user input instead of performing timezone calculations. <br>
Mitigation: Do not rely on it for scheduling decisions without independently verifying any timezone results with a trusted source. <br>
Risk: Meeting details, travel plans, names, client information, or private schedules entered into the tool may be stored locally under ~/.local/share/timezone. <br>
Mitigation: Avoid entering sensitive details unless local storage is acceptable, and review or remove the local history files when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/timezone) <br>
- [Publisher Profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files] <br>
**Output Format:** [Terminal text with local log files and JSON, CSV, or TXT exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores action history under ~/.local/share/timezone.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
