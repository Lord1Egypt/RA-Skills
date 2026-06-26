## Description: <br>
Scan projects and codebases for exposed secrets, API keys, tokens, passwords, and sensitive credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit local projects for hardcoded credentials, exposed API keys, populated environment files, and secrets retained in git history, then prioritize remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secrets reports can contain sensitive credential material or surrounding code context. <br>
Mitigation: Avoid sharing or committing generated reports, redact sensitive values before review, and store reports only where project secrets are permitted. <br>
Risk: Scanning broad directories or enabling git-history checks can expose more sensitive data than intended. <br>
Mitigation: Point the scanner at the smallest relevant directory and use git-history checks only when needed for committed-secret investigation. <br>
Risk: The evidence lists wallet, purchase, OAuth, and sensitive-credential capability tags that are not required by the current artifacts. <br>
Mitigation: Do not grant wallet, purchase, OAuth, or unrelated account permissions for this skill based on the provided artifacts. <br>


## Reference(s): <br>
- [Prevention Guide](references/prevention-guide.md) <br>
- [Secret Patterns Reference](references/secret-patterns.md) <br>
- [git-secrets](https://github.com/awslabs/git-secrets.git) <br>
- [detect-secrets](https://github.com/Yelp/detect-secrets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON severity-ranked secrets report with remediation steps and optional command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include file paths, line numbers, redacted matches, surrounding context, summary counts, recommendations, and CI-oriented exit codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
