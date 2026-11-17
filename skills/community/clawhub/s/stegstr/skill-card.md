## Description:

Decode and embed Stegstr payloads in PNG images for extracting hidden Nostr data, encoding payloads into cover PNGs, and working with steganographic social networking workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunkstr](https://clawhub.ai/user/brunkstr)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and automation agents use this skill to decode hidden payloads from Stegstr PNG images, embed text, JSON, binary, or Nostr bundle payloads into cover PNGs, and create Nostr note bundles for steganographic sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer fetches and builds mutable remote code during installation.

Mitigation: Review the installer before running it and prefer a pinned, verified Stegstr release or fixed commit.

Risk: Examples include passing Nostr private keys through agent-visible commands.

Mitigation: Do not pass real Nostr private keys directly in agent-visible commands; use safer secret-handling practices outside the agent transcript.

Risk: Generated output PNGs may contain hidden data.

Mitigation: Treat generated or modified PNGs as files that may carry embedded payloads and review sharing or storage accordingly.

## Reference(s):

- [Stegstr homepage](https://stegstr.com)
- [Stegstr GitHub repository](https://github.com/brunkstr/Stegstr)
- [For AI agents](https://www.stegstr.com/wiki/for-agents.html)
- [CLI documentation](https://www.stegstr.com/wiki/cli.html)
- [Nostr bundle schema](https://raw.githubusercontent.com/brunkstr/Stegstr/main/schema/bundle.schema.json)
- [Stegstr releases](https://github.com/brunkstr/Stegstr/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, file paths, and CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or inspection of PNG files that contain hidden Stegstr payloads.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
