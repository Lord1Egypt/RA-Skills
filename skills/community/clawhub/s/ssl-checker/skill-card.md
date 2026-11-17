## Description:

Check SSL certificate health, protocols, and cipher suites on domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run basic OpenSSL-based checks for certificate details, expiry, protocol support, cipher output, and chain information for a supplied domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a basic SSL-checking shell script with quality and accuracy limitations.

Mitigation: Use its output as a preliminary signal and confirm important findings with a dedicated TLS assessment tool or manual review.

Risk: The documented commands appear to have broken argument handling.

Mitigation: Test commands in a controlled environment and fix argument handling before relying on results.

Risk: The skill makes outbound TLS connections to user-supplied domains.

Mitigation: Run it only against domains you are authorized to assess and from a network where those outbound connections are acceptable.

## Reference(s):

- [Ssl Checker on ClawHub](https://clawhub.ai/xueyetianya/skills/ssl-checker)
- [BytesAgain](https://bytesagain.com)
- [Publisher Profile](https://clawhub.ai/user/xueyetianya)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill stores local data under ~/.local/share/ssl-checker and makes outbound TLS connections to domains supplied by the user.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
