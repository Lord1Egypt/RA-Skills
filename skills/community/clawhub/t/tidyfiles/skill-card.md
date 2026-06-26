## Description: <br>
Records file-organization notes and command activity in local logs with search, statistics, and export commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other command-line users can use this skill to record file cleanup notes, directory checks, disk-usage observations, and generated cleanup reports for later review or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill may appear to organize files while mainly storing user-entered activity notes in local plaintext logs. <br>
Mitigation: Use it only when local activity logging is intended, avoid entering secrets or sensitive file paths, and review or delete ~/.local/share/tidyfiles when the stored history is no longer needed. <br>


## Reference(s): <br>
- [Tidyfiles on ClawHub](https://clawhub.ai/xueyetianya/tidyfiles) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and local file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The accompanying shell script stores entries and exports data as plain text, CSV, or JSON under ~/.local/share/tidyfiles.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
