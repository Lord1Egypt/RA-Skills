## Description: <br>
Syscheck is a command-line sysops helper advertised for system health checks, with artifact behavior centered on storing, searching, exporting, and reporting local history entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators can use Syscheck from the command line to record, review, search, and export local operational notes that are presented as sysops status entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Advertised diagnostic scope may not match artifact behavior. <br>
Mitigation: Treat Syscheck as a local note/history logger and verify any system health claims independently before operational use. <br>
Risk: Sensitive operational text may be stored locally and later searched or exported. <br>
Mitigation: Do not enter hostnames, incident details, credentials, tokens, remediation plans, or other sensitive operational text unless storage under ~/.local/share/syscheck is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/syscheck) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text logs and optional JSON, CSV, or TXT exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local history and export files under ~/.local/share/syscheck.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
