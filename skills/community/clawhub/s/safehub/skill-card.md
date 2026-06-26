## Description: <br>
Scan OpenClaw skills for malware and security issues before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumeetghimire](https://clawhub.ai/user/sumeetghimire) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use SafeHub to scan OpenClaw skills from local paths or trusted repository URLs before installation, review static and sandbox findings, and decide whether to install with caution or reject a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted GitHub scan targets can reach a shell command. <br>
Mitigation: Use local paths or only trusted repository URLs until cloning is changed to a non-shell API. <br>
Risk: Sandbox results may overstate what behavior monitoring actually observes. <br>
Mitigation: Treat sandbox output as advisory and review static findings and source behavior before relying on the recommendation. <br>
Risk: Rule updates can overwrite local rules from the configured rules repository. <br>
Mitigation: Run updates only with a trusted SAFEHUB_RULES_REPO and branch. <br>


## Reference(s): <br>
- [SafeHub ClawHub listing](https://clawhub.ai/sumeetghimire/safehub) <br>
- [Publisher profile](https://clawhub.ai/user/sumeetghimire) <br>
- [SafeHub homepage](https://github.com/sumeetghimire/safehub) <br>
- [SafeHub support](https://github.com/sumeetghimire/safehub/issues) <br>
- [Semgrep](https://semgrep.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, analysis] <br>
**Output Format:** [Terminal text with scan findings, trust score, recommendation, and cached JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, Semgrep, and git; Docker is optional for sandbox execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter, package.json, skill.json, clawhub.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
