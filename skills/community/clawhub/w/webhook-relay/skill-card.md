## Description:

Webhook Relay helps agents guide users through receiving, forwarding, tunneling, debugging, transforming, and scheduling webhooks with the relay CLI and public bin API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rusenask](https://clawhub.ai/user/rusenask)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Webhook Relay for local webhook development, private-network forwarding, public tunnels, webhook capture, payload transformation, and scheduled webhook delivery. It is most useful when an agent needs to produce practical relay CLI commands, curl examples, setup guidance, and safety notes for exposing or inspecting HTTP traffic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook forwarding and tunnels can expose private or local services to public endpoints, including persistent exposure when the relay runs as a background service.

Mitigation: Use non-sensitive demo endpoints until the exposure model is understood, review created buckets and tunnels before sharing URLs, and know how to stop and remove any installed relay service.

Risk: The HMAC example can send a real webhook signing secret to an external /v1/hmac endpoint.

Mitigation: Compute webhook signatures locally for real secrets and use the external HMAC endpoint only with test or throwaway values.

Risk: Putting tunnel passwords directly on the command line can expose them through shell history or process listings.

Mitigation: Avoid real tunnel passwords in command-line arguments and prefer safer credential handling approved for the deployment environment.

Risk: Public webhook bins are temporary and readable by anyone with the bin ID.

Mitigation: Do not send secrets, credentials, or personal data to bins; switch to the real protected destination after debugging.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rusenask/skills/webhook-relay)
- [Webhook Relay Homepage](https://webhookrelay.com)
- [Webhook Relay Docs](https://webhookrelay.com/docs)
- [Webhook Relay Plain-Markdown Docs Index](https://webhookrelay.com/llms.txt)
- [Install the CLI](https://webhookrelay.com/docs/installation/cli.md)
- [Receive Webhooks on Localhost and Private Networks](https://webhookrelay.com/docs/webhooks/internal/localhost.md)
- [Forward to a Public URL](https://webhookrelay.com/docs/webhooks/public/public-destination.md)
- [Multiple Destination URLs](https://webhookrelay.com/docs/webhooks/public/multiple-destination-urls.md)
- [Tunnels Overview](https://webhookrelay.com/tunnels.md)
- [Tunnel Regions](https://webhookrelay.com/docs/tunnels/regions.md)
- [Webhook Transformation Functions](https://webhookrelay.com/docs/webhooks/functions.md)
- [Recurring Cron Webhooks](https://webhookrelay.com/docs/webhooks/cron/using-cron-webhooks.md)
- [Webhook Bin Debugging](https://webhookrelay.com/webhook-bin.md)
- [Forwarding Rules](https://webhookrelay.com/features/forwarding-rules.md)
- [Custom Subdomains](https://webhookrelay.com/docs/webhooks/custom-subdomains.md)
- [Custom Domains](https://webhookrelay.com/docs/webhooks/custom-domains.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, curl examples, JavaScript snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public endpoint URLs, relay CLI command sequences, webhook bin API calls, and operational cleanup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
