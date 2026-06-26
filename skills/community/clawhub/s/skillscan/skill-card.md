## Description: <br>
SkillScan scans skill packages through its hosted service, reports security verdicts, and guides agents to block high- or critical-risk skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tokauthai](https://clawhub.ai/user/tokauthai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use SkillScan to scan installed, newly added, zipped, or remote skill packages and decide whether to proceed, warn, or block based on scan verdicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill contents are uploaded to skillscan.tokauth.com for analysis. <br>
Mitigation: Scan only skills whose contents can be shared with the service; avoid private, proprietary, or secret-bearing skills unless that upload is acceptable. <br>
Risk: The scanner stores device-linked client information for reuse across scan requests. <br>
Mitigation: Review the generated client information and run the scanner only in environments where this telemetry is acceptable. <br>
Risk: The scanner can replace its own files through the update path. <br>
Mitigation: Review or disable automatic updates when deterministic tooling or separate change control is required. <br>
Risk: Scan results are advisory unless the surrounding agent or workflow enforces the scanner exit codes. <br>
Mitigation: Configure the calling workflow to enforce nonzero exit codes and require review for low or medium findings. <br>


## Reference(s): <br>
- [SkillScan ClawHub Release](https://clawhub.ai/tokauthai/skillscan) <br>
- [SkillScan Service](https://skillscan.tokauth.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and scanner verdict summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish pass, warning, block, and scan-failure outcomes.] <br>

## Skill Version(s): <br>
1.1.6 (source: release evidence, SKILL.md frontmatter, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
