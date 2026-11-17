## Description:

Alipay+ Payment Integration Assistant helps acquirers and mobile service providers integrate Alipay+ payments, including customer-presented and merchant-presented payment modes, configuration generation, signature verification testing, ACQP notification debugging, and reconciliation file processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wypride](https://clawhub.ai/user/wypride)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to plan and troubleshoot Alipay+ ACQP and MPP payment integrations. It helps generate configuration, test signatures, debug ACQP webhooks, process reconciliation files, and identify when official Alipay+ documentation is required for detailed API fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles payment credentials, private keys, webhook payloads, and reconciliation data that may expose secrets or financial records.

Mitigation: Review before installing, use sandbox or test data by default, redact logs, restrict file permissions, and avoid pasting or printing real private keys.

Risk: Webhook debugging and replay behavior can expose local services or send test notifications to inappropriate endpoints.

Mitigation: Use access controls for any tunnel, avoid exposing local services unnecessarily, and do not replay webhook data to production endpoints.

Risk: SFTP and signature examples may be copied into production without hardening.

Mitigation: Treat scripts as starting points, validate the SFTP and signature examples against official Alipay+ requirements, and harden them before production use.

## Reference(s):

- [Alipay+ Integration Flows](references/flows.md)
- [Alipay+ API Reference](references/api-reference.md)
- [Alipay+ Signature Guide](references/signature-guide.md)
- [Alipay+ Webhook Configuration Guide](references/webhook-guide.md)
- [Reconciliation File Download Guide](references/reconciliation-guide.md)
- [ACQP Integration Checklist](references/acqp-checklist.md)
- [MPP Integration Checklist](references/mpp-checklist.md)
- [Configuration Template](references/config-template.json)
- [ACQP API Overview Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/)
- [MPP API Overview Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/)
- [MPP Android Client SDK Quick Start Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/android_quick)
- [MPP iOS Client SDK Quick Start Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/ios_quick)
- [MPP Server SDK Quick Start Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/server_quick)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, and JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, signature-test, webhook-debug, and reconciliation-processing artifacts when the user runs bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
