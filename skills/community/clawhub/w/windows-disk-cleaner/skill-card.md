## Description: <br>
Safe Windows disk cleanup assistant that scans a selected drive, analyzes cache and storage usage, and produces cleanup guidance and reports with user-confirmed deletion steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guge0](https://clawhub.ai/user/guge0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, power users, and IT support staff use this skill to inspect Windows disk usage, identify safe cleanup candidates, and generate reviewable cleanup reports and commands before removing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local scan reports can contain filenames, paths, and system or cache metadata. <br>
Mitigation: Keep scan_result.json and cleanup_report.html private and avoid sharing them unless the contents have been reviewed. <br>
Risk: Generated cleanup commands can remove user data or persistent development resources if run without review. <br>
Mitigation: Inspect each generated PowerShell command before execution, especially commands touching Downloads, Docker volumes, node_modules, and Remove-Item targets. <br>
Risk: Some cleanup candidates require user judgment, such as large files, duplicate files, virtual environments, and old project dependencies. <br>
Mitigation: Confirm each review-tier item before deletion and prefer backup, recycle-bin, or tool-native cleanup workflows when available. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/guge0/windows-disk-cleaner) <br>
- [Windows safe cleanup paths reference](references/safe_paths.md) <br>
- [OpenClaw runtime metadata](metadata.openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell and Python command snippets, JSON scan output, and generated HTML cleanup reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Windows environments and requires powershell and python3.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
