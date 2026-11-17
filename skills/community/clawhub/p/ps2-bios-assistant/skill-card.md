## Description:

Inspect a local PS2 BIOS file by reporting MD5, SHA-1, file size, and basic dump-size validation without providing BIOS downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nbkdevs](https://clawhub.ai/user/nbkdevs)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to inspect a local PS2 BIOS dump they already have, calculate MD5 and SHA-1 hashes, check basic dump-size expectations, and compare against an optional user-supplied expected hash.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included external homepage may steer users toward BIOS downloads, conflicting with the skill's no-download policy.

Mitigation: Replace or ignore that link, do not download or attach BIOS binaries, and use only BIOS files that the user has legally dumped themselves.

Risk: Checksum equality can be mistaken for legal authenticity or proof of lawful possession.

Mitigation: Present hash matches as reference-only and avoid making legal authenticity claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nbkdevs/skills/ps2-bios-assistant)
- [Metadata homepage from ClawHub evidence](https://allps2bios.com/ps2-bios-retroarch/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with local checksum results and optional shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not provide BIOS binaries; hash matches are reference-only.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
