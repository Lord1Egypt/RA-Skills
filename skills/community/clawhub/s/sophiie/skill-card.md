## Description: <br>
Manage Sophiie sales pipeline data, inquiries, appointments, FAQs, policies, SMS, and calls through the Sophiie REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomc98](https://clawhub.ai/user/tomc98) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sophiie customers and their agents use this skill to manage live sales pipeline workflows, review organization data, and initiate customer communications from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on a live Sophiie account and modify CRM, FAQ, policy, and lead records. <br>
Mitigation: Use a test or least-privileged API key where possible, and require explicit confirmation before create, update, or delete actions. <br>
Risk: The skill can initiate outbound SMS messages and calls to real leads or phone numbers. <br>
Mitigation: Confirm the recipient, phone number, and message or call intent with the user before sending. <br>
Risk: Changes to FAQs and policies may alter customer-facing assistant behavior. <br>
Mitigation: Review proposed content before applying it and verify changes against the organization's approved customer guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tomc98/sophiie) <br>
- [Sophiie Documentation](https://docs.sophiie.ai) <br>
- [Sophiie API Reference](https://docs.sophiie.ai/api) <br>
- [Sophiie Dashboard](https://app.sophiie.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command invocations and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOPHIIE_API_KEY, curl, and jq; commands can read and modify live Sophiie account data.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
