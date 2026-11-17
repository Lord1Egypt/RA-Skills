## Description:

Manage multiple paths with Tailscale Serve so an agent can guide users through serving files, directories, or local ports without path conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snopoke](https://clawhub.ai/user/snopoke)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill when configuring Tailscale Serve paths for local files, directories, and services. It helps them check current mappings, add non-conflicting paths, share resulting tailnet URLs, and troubleshoot common serving issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could expose sensitive local files or directories through Tailscale Serve.

Mitigation: Check tailscale serve status, avoid broad or sensitive folders such as home directories, and confirm who has tailnet access before sharing URLs.

Risk: Using root-path serving or reset commands could overwrite or remove active mappings unintentionally.

Mitigation: Review current mappings before adding root-path serves or running tailscale serve reset, and use set-path for additive changes when preserving existing shares.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
