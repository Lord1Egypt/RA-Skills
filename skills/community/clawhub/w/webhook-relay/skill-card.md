## Description: <br>
Webhook Relay guides an agent through forwarding webhooks, exposing local or private HTTP/TCP services through public tunnels, debugging webhook payloads, transforming requests, and scheduling recurring webhooks with the relay CLI and bin API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rusenask](https://clawhub.ai/user/rusenask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Webhook Relay workflows for receiving provider webhooks, forwarding traffic to local or private services, creating public tunnels, inspecting webhook payloads, and adding transforms or cron-triggered webhook calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public tunnels and forwarding workflows can expose local or private services to the internet. <br>
Mitigation: Confirm the destination is intended to be public, use authentication where appropriate, and avoid exposing admin panels, databases, SSH, or internal dashboards unless the exposure is explicitly approved. <br>
Risk: Webhook bins are public and temporary, so captured request data may be readable by anyone with the bin identifier. <br>
Mitigation: Do not send secrets, production credentials, or sensitive personal data to bins; use them only for inspection and switch to the real handler after debugging. <br>
Risk: Buckets, tunnels, functions, cron jobs, or background relay services may continue forwarding traffic after testing. <br>
Mitigation: Remove temporary resources and stop background services when finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rusenask/webhook-relay) <br>
- [Webhook Relay Homepage](https://webhookrelay.com) <br>
- [Webhook Relay Docs Index](https://webhookrelay.com/llms.txt) <br>
- [Webhook Relay CLI Installation](https://webhookrelay.com/docs/installation/cli.md) <br>
- [Receive Webhooks on Localhost or Private Networks](https://webhookrelay.com/docs/webhooks/internal/localhost.md) <br>
- [Forward Webhooks to Public Destinations](https://webhookrelay.com/docs/webhooks/public/public-destination.md) <br>
- [Webhook Relay Tunnels](https://webhookrelay.com/tunnels.md) <br>
- [Webhook Transformation Functions](https://webhookrelay.com/docs/webhooks/functions.md) <br>
- [Cron Webhooks](https://webhookrelay.com/docs/webhooks/cron/using-cron-webhooks.md) <br>
- [Webhook Bin](https://webhookrelay.com/webhook-bin.md) <br>
- [Forwarding Rules](https://webhookrelay.com/features/forwarding-rules.md) <br>
- [Custom Domains](https://webhookrelay.com/docs/webhooks/custom-domains.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell command, JSON, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes relay CLI and curl examples for buckets, inputs, outputs, tunnels, bins, functions, cron jobs, verification, and cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
