## Description: <br>
Regex safety and correctness analyzer that detects catastrophic backtracking, portability errors, correctness bugs, maintainability issues, anchoring problems, and pattern injection risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use RegexGuard to scan source code for regex safety, portability, correctness, maintainability, anchoring, and pattern injection issues. It can generate local scan results for one-off audits, CI checks, and git-hook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: License-token handling and parsing are review-worthy, and the skill requires sensitive license credentials for paid tiers. <br>
Mitigation: Review scripts before installation, avoid license keys from untrusted sources, and prefer environment or config storage over passing keys on the command line. <br>
Risk: Git-hook install and uninstall flows can modify lefthook configuration and run automatic commit or push scans. <br>
Mitigation: Use hook commands only after reviewing the lefthook configuration and confirming the repository should enforce RegexGuard scans. <br>


## Reference(s): <br>
- [RegexGuard Homepage](https://regexguard.pages.dev) <br>
- [RegexGuard Hook Documentation](https://regexguard.pages.dev/docs/hooks) <br>
- [ClawHub RegexGuard Listing](https://clawhub.ai/suhteevah/regexguard) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, HTML, Shell commands, Guidance] <br>
**Output Format:** [Text, Markdown, JSON, or HTML scan reports with file, line, severity, check ID, description, and remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local scanning output includes regex quality scores and pass/fail exit codes for CI or hook use.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
