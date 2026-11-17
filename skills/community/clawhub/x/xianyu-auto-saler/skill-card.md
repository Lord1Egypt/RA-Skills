## Description:

咸鱼自动发货 helps agents monitor Xianyu chat for paid-order cards and run configurable virtual-goods fulfillment workflows through browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sliverp](https://clawhub.ai/user/sliverp)

### License/Terms of Use:

MIT

## Use Case:

External sellers and automation developers use this skill to monitor Xianyu conversations for payment confirmations and send virtual goods such as keys, links, images, files, or API-generated fulfillment data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automation can act on a live seller account and send fulfillment content after detecting payment-like chat state.

Mitigation: Use a dedicated browser profile or account and require manual confirmation or authoritative order verification before sending keys or other goods.

Risk: Product keys and buyer details may be stored in plaintext key files, fulfillment logs, or chat messages.

Mitigation: Avoid logging full keys, restrict file permissions, rotate keys, and store only the minimum buyer and order data needed for fulfillment.

Risk: Optional notification and API examples may send buyer identifiers or keys to third-party services.

Mitigation: Remove those integrations unless the destination is trusted, privacy-reviewed, and configured with pinned and verified dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sliverp/skills/xianyu-auto-saler)
- [Publisher profile](https://clawhub.ai/user/sliverp)
- [Artifact README](artifact/README.md)
- [Artifact quickstart](artifact/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash snippets and shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires agent-browser and a configured browser session for live site automation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
