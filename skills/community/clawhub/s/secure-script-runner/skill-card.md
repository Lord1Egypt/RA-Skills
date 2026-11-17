## Description:

A documentation skill that teaches agents how to store encrypted scripts in MGC Blackbox and execute them through MCP, API, or WebUI paths with explicit user authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to document and follow MGC Blackbox workflows for encrypted script storage, blackbox execution, runtime parameter passing, credential access, and script sealing. It is intended for explicitly approved local script execution where the agent receives results rather than script plaintext.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opaque scripts may have broad local access to files, network, and MGC-stored credentials without clear technical scoping.

Mitigation: Install only when MGC Blackbox and the scripts are trusted; run under a low-privilege account, deny outbound network access by default, and require separate approval for each named credential.

Risk: The agent cannot audit script plaintext when executing scripts through blackbox workflows.

Mitigation: Require the user to verify each script source, purpose, and expected data or credential access before authorizing execution.

Risk: MGC 1.4.9 script execution issues may cause parameter parsing failures, silent failures, or blocked stdout.

Mitigation: Use parse_known_args, strip added quotes from runtime parameters, prefer forward-slash paths and explicit named arguments, and write substantive output to files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zkeviny/skills/secure-script-runner)
- [MGC Blackbox Repository](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Blackbox Issues](https://github.com/zkeviny/MGC-Blackbox/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown documentation with Python, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MGC 1.4.9 workaround guidance for parse_known_args, manual quote stripping, and file-based outputs.]

## Skill Version(s):

1.1.1 (source: server-resolved release, SKILL.md frontmatter, and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
