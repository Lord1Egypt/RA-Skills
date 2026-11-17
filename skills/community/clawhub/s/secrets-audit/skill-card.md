## Description:

Scans projects for exposed secrets, API keys, tokens, passwords, and other hardcoded credentials, then reports severity-ranked findings with remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit codebases for exposed credentials, review severity-ranked findings, and plan remediation such as secret rotation, environment variable use, and prevention hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan reports or CI logs may expose detected secrets.

Mitigation: Treat reports and logs as sensitive, restrict access, redact before sharing, and rotate any confirmed exposed credentials.

Risk: The scanner can read outside the selected folder through symlinks.

Mitigation: Run it only on trusted repositories or isolated copies until symlink handling is fixed, and review the target tree for symlinks before scanning.

Risk: The local scanner reads the project files it is pointed at.

Mitigation: Use it only on projects you are authorized to inspect and avoid running it on untrusted repositories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/secrets-audit)
- [Secret Patterns Reference](references/secret-patterns.md)
- [Prevention Guide](references/prevention-guide.md)
- [git-secrets](https://github.com/awslabs/git-secrets.git)
- [detect-secrets](https://github.com/Yelp/detect-secrets)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Severity-ranked text or JSON scan reports with remediation guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI-oriented exit codes distinguish clean scans, low or medium findings, and high severity findings.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
