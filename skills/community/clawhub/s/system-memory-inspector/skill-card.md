## Description: <br>
The skill guides an agent through Linux system memory inspections by scanning all processes, recording memory snapshots, analyzing RSS growth trends, and producing leak-suspect reports with triage guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhur0ng](https://clawhub.ai/user/zhur0ng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operators use this skill to inspect Linux hosts for process-level memory growth, identify likely memory leaks, and generate follow-up investigation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated inspection workflows can persist system-wide process command lines that may contain secrets or sensitive arguments. <br>
Mitigation: Use only on Linux hosts where system-wide process inspection is authorized, redact or remove command-line fields before scheduled use, and avoid sharing reports until command-line arguments have been checked for secrets. <br>
Risk: Snapshots and reports stored under /var/log/memory-inspector may expose process inventory and operational details. <br>
Mitigation: Restrict permissions on /var/log/memory-inspector, define retention and cleanup rules, and share generated reports only with authorized responders. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plain-text inspection report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Linux hosts with ps, awk, sort, and uniq available; reports may include process command lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
