## Description:

Access Chia blockchain data including blocks, transactions, addresses, CAT tokens, NFTs, network stats, and XCH price via the Spacescan.io API with an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to query Chia blockchain data from Spacescan, including blocks, transactions, addresses, network status, CAT tokens, NFTs, and XCH price information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried Chia addresses, transaction IDs, hashes, and search terms are sent to Spacescan.

Mitigation: Use the skill only when sharing those identifiers with Spacescan is acceptable for the deployment context.

Risk: The skill requires a Spacescan API key.

Mitigation: Use a limited API key, keep it in environment variables or a secrets manager, and avoid committing shell profiles or dotfiles that contain it.

Risk: The security summary recommends updating or pinning npm dependencies before sensitive use.

Mitigation: Review and pin dependency versions, then run normal dependency and security checks before deployment in sensitive environments.

## Reference(s):

- [ClawHub Spacescan Skill Page](https://clawhub.ai/koba42corp/skills/spacescan)
- [Spacescan](https://www.spacescan.io)
- [Spacescan API Plans](https://www.spacescan.io/apis)
- [Chia Network](https://chia.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Formatted text and Markdown with inline command and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Spacescan API key and sends requested blockchain identifiers to the Spacescan API.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
