## Description: <br>
Scan registered Gitea or Obsidian Git material sources manually or on a schedule, detect added, modified, or deleted files, create incremental compilation jobs, and update source fingerprints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and PaperKB operators use this skill to scan registered Gitea or Obsidian Git material sources, detect file changes, and start incremental compilation workflows with confirmation for large updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires broad Gitea credentials and can perform persistent remote writes. <br>
Mitigation: Install it only in a dedicated PaperKB/Gitea environment, use a narrowly scoped service account where possible, and restrict allowed scan output and repository write locations. <br>
Risk: The sample configuration uses an HTTP Gitea endpoint. <br>
Mitigation: Replace the sample endpoint with a trusted HTTPS Gitea URL before deployment. <br>
Risk: Dependencies are not pinned in the artifact requirements. <br>
Mitigation: Pin dependency versions and review updates before running the skill in a production environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skills/scan-updates) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution depends on configured Gitea credentials and OpenClaw context values; scripts may persist scan results, task records, job records, source fingerprints, and repository updates.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
