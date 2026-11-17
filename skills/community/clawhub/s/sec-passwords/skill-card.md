## Description:

Provides curated top password lists for authorized security testing, including common, leaked, and worst passwords under 10MB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandaai-1337](https://clawhub.ai/user/pandaai-1337)

### License/Terms of Use:

MIT-0

## Use Case:

Security practitioners, developers, and authorized testers use this skill to access curated password wordlists for password policy validation, credential testing, password spraying, brute force testing, and authentication testing within approved scopes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included password lists can enable abusive login attempts if used outside an authorized scope.

Mitigation: Use only on systems you own or are explicitly authorized to test, and keep testing within approved rules of engagement.

Risk: Real-world password corpora may include offensive words.

Mitigation: Review outputs before sharing them in reports, training material, or customer-facing deliverables.

## Reference(s):

- [Security Passwords ClawHub listing](https://clawhub.ai/pandaai-1337/skills/sec-passwords)
- [500-worst-passwords.txt](references/Passwords/Common-Credentials/500-worst-passwords.txt)
- [10k-most-common.txt](references/Passwords/Common-Credentials/10k-most-common.txt)
- [100k-most-used-passwords-NCSC.txt](references/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt)
- [darkweb2017_top-10000.txt](references/Passwords/Common-Credentials/darkweb2017_top-10000.txt)
- [probable-v2_top-12000.txt](references/Passwords/Common-Credentials/probable-v2_top-12000.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with references to text wordlist files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static password-wordlist content; no executable behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
