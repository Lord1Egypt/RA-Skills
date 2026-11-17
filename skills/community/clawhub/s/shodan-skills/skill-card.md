## Description:

Queries Shodan for internet-connected device information, security data, DNS records, host details, search counts, and network asset analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security analysts use this skill to query Shodan for authorized IP, domain, device, and organization investigations and to produce structured security assessments or asset reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends IP addresses, domains, search terms, and the configured Shodan API key to Shodan.

Mitigation: Use the skill only when sharing those targets with Shodan is approved, and avoid sensitive internal targets unless authorized.

Risk: Shodan searches can expose information about systems outside the user's authority.

Mitigation: Limit investigations to assets the user is authorized to assess and review generated findings before acting on them.

Risk: The Shodan API key is a credential required for every API call.

Mitigation: Store SHODAN_API_KEY in a secret store, avoid placing it in prompts or logs, and rotate it if exposure is suspected.

Risk: The artifact pins requests==2.28.0, which evidence.security flags for update before proxy-sensitive use.

Mitigation: Update the pinned requests dependency before deploying in proxy-sensitive environments.

## Reference(s):

- [Shodan API Reference](references/api-reference.md)
- [Shodan Developer API](https://developer.shodan.io/api)
- [ClawHub Skill Page](https://clawhub.ai/moxin1044/skills/shodan-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SHODAN_API_KEY and sends Shodan queries to the Shodan API.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
