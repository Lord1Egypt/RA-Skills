## Description: <br>
Scan your installed ClawHub skills for dangerous code patterns, including credential harvesting, shell injection, unauthorized network calls, and known malicious signatures, and produce a per-skill safety report with SAFE, WARN, or DANGEROUS ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infectit007](https://clawhub.ai/user/infectit007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit installed ClawHub skills before trusting them, after installing new skills, or when they want a local summary of scanner findings. It formats OpenClaw security audit results into actionable safety ratings and review or removal guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup commands can remove installed skills if the wrong skill name or path is approved. <br>
Mitigation: Confirm the DANGEROUS rating, skill name, and filesystem path before approving uninstall or rm -rf commands. <br>
Risk: Recurring scans can create persistent scheduled activity and store scan summaries in memory. <br>
Mitigation: Only add the cron schedule when recurring local audits and retained summaries are desired. <br>
Risk: WARN ratings may reflect legitimate shell execution or environment access rather than malicious behavior. <br>
Mitigation: Review the cited source path and evidence before treating WARN findings as malicious. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infectit007/skill-safety-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/infectit007) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Per-skill SAFE, WARN, or DANGEROUS ratings with evidence, recommendations, and optional user-approved cleanup or scheduling commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
