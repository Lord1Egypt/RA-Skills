## Description: <br>
Implement, troubleshoot, and generate integrations for Yuboto Omni API covering SMS, Viber and messaging endpoints, callbacks, lists, contacts, blacklist, cost, balance, and account methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinaras](https://clawhub.ai/user/dinaras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to build, troubleshoot, and run Yuboto/Octapush messaging workflows, including SMS sends, CSV bulk sends, delivery-status polling, balance checks, cost estimates, and API integration examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMS sends and CSV bulk sends can reach unintended recipients or incur unexpected cost. <br>
Mitigation: Confirm recipients, sender, message text, CSV files, batch size, and cost before sending. <br>
Risk: API keys can be exposed through command history, URLs, source files, or local configuration mistakes. <br>
Mitigation: Store OCTAPUSH_API_KEY through OpenClaw or environment variables, never put API keys in URLs or source files, and rotate the key if exposure is suspected. <br>
Risk: Callback URLs and API base URL overrides can send message status data to untrusted destinations. <br>
Mitigation: Use only trusted HTTPS callback and base URLs. <br>
Risk: Runtime logs and local state may contain sensitive message metadata and can contain payload details if full persistence is enabled. <br>
Mitigation: Keep full payload persistence disabled unless needed and treat local logs and state as sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinaras/yuboto-omni-api) <br>
- [Yuboto Omni API quick reference](references/api_quick_reference.md) <br>
- [Yuboto Omni API raw documentation v1.10](references/omni_api_v1_10_raw.md) <br>
- [Yuboto Omni API Swagger v1 snapshot](references/swagger_v1.json) <br>
- [Yuboto Omni API user guide](references/user-guide.md) <br>
- [Version history](references/version.md) <br>
- [Yuboto API documentation](https://api.yuboto.com/scalar/#description/introduction) <br>
- [Yuboto Swagger JSON](https://api.yuboto.com/swagger/v1/swagger.json) <br>
- [Yuboto account registration](https://octapush.yuboto.com) <br>
- [Yuboto messaging product information](https://messaging.yuboto.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance, code snippets, shell commands, configuration examples, and JSON output from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and OCTAPUSH_API_KEY; helper scripts use the Python standard library and may call the live Yuboto API.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release metadata and references/version.md, released 2026-03-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
