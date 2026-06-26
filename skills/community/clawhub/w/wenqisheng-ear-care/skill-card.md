## Description: <br>
Provides customer-service guidance for Wenqisheng Ear Care storefront inquiries, including hours, locations, appointments, services, promotions, Wi-Fi, brand information, and ear or eye care FAQ responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liubuq-sys](https://clawhub.ai/user/liubuq-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External customers and storefront operators use this skill to answer Wenqisheng Ear Care customer questions and guide users through store, service, appointment, promotion, hygiene, and basic wellness-information workflows. <br>

### Deployment Geography for Use: <br>
China, with service content specific to Wenqisheng storefronts in Nanchang. <br>

## Known Risks and Mitigations: <br>
Risk: The release includes self-updating installation behavior through git pulls and scheduled updates. <br>
Mitigation: Install from a pinned, inspected release and disable or remove unattended cron or scheduled-task updates unless automatic updates are explicitly required. <br>
Risk: The documentation suggests broad auto-discovery rules that can install or update the skill when matching keywords appear in agent conversations. <br>
Mitigation: Use manual installation and avoid adding broad CLAUDE.md auto-install rules unless the deployment owner has reviewed and approved that behavior. <br>
Risk: The optional bot server uses sensitive model-provider credentials and includes webhook and development-bot behavior that the security evidence flags for review. <br>
Mitigation: Keep the bot server private until webhook signature verification is complete, unrelated development-bot routes are removed or isolated, and credentials are stored in a secret manager or equivalent protected environment. <br>
Risk: Ear and eye symptom handling can be mistaken for medical advice. <br>
Mitigation: Treat responses as wellness and store-service information only, avoid diagnosis, and direct users with severe or urgent symptoms to appropriate medical care. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liubuq-sys/wenqisheng-ear-care) <br>
- [Publisher profile](https://clawhub.ai/user/liubuq-sys) <br>
- [Business information](references/business-info.md) <br>
- [Services](references/services.md) <br>
- [Promotions](references/promotions.md) <br>
- [FAQ](references/faq.md) <br>
- [Brand](references/brand.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text customer-service responses, with occasional shell commands or configuration snippets for installation and operator workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses depend on readable reference files and configured model-provider credentials when the optional bot server is used.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
