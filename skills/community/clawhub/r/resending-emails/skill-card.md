## Description:

Helps agents operate Resend through the official CLI for installation, authentication, email sending, domains, webhooks, inbound mail, contacts, broadcasts, templates, API keys, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute Resend CLI workflows from agents, terminals, or CI. It supports deterministic command selection, file scaffolding, diagnostics, subprocess handling, and fallback guidance when the CLI does not cover a task cleanly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer commands can execute unpinned code, and CI examples may expose an email API key during installation.

Mitigation: Use pinned and verified CLI installation methods, separate install steps from authenticated send steps, and inject RESEND_API_KEY only where it is needed.

Risk: Live Resend operations can send email, batch send, forward inbound mail, create broadcasts, modify webhooks or domains, and create or delete API keys.

Mitigation: Require explicit confirmation before state-changing operations and verify results with read, list, or get commands after each mutation.

Risk: Over-broad credentials can expand the impact of a mistaken command or exposed CI secret.

Mitigation: Use least-privilege, domain-scoped keys and prefer environment variables or stored profiles over command-line API key arguments.

Risk: Known CLI coverage gaps can lead an agent to overpromise template sending, domain receiving toggles, or streaming command behavior.

Mitigation: Check the documented coverage gaps, inspect local CLI help for the installed version, and fall back to MCP or API only when the CLI surface is insufficient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tristanmanchester/skills/resending-emails)
- [Agent Operating Model](artifact/references/agent-operating-model.md)
- [Command Selection](artifact/references/command-selection.md)
- [Install, Auth, and Profiles](artifact/references/install-auth-and-profiles.md)
- [Subprocess Contract](artifact/references/subprocess-contract.md)
- [Templates and Coverage Gaps](artifact/references/templates-and-coverage-gaps.md)
- [Source Manifest](artifact/assets/source-manifest.json)
- [Resend CLI Repository](https://github.com/resend/resend-cli)
- [Resend CLI Changelog](https://resend.com/changelog/cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and generated file scaffolds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON from the bundled helper and may materialize scaffold files when explicitly requested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
