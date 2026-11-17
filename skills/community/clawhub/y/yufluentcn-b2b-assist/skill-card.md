## Description:

B2B foreign trade inquiry reply and RFQ quotation assistant executed through the Yufluent cloud harness, supporting FOB/CIF quotations, MOQ negotiation, lead-time replies, and company profile responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External trade and sales users use this skill to draft B2B inquiry responses, RFQ quotation replies, and negotiation-ready summaries for products, MOQ, FOB/CIF pricing, lead time, payment terms, and company profile context. Agents should return the generated reply for human business review before it is sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens and customer inquiry or quotation details may be sent to the configured cloud endpoint.

Mitigation: Use only a trusted HTTPS Yufluent endpoint, keep TOKENAPI_KEY in local environment or secret storage, and avoid committing keys or sensitive inquiry data to shared files.

Risk: Setting TOKENAPI_BASE_URL to an arbitrary host could expose credentials and business data to an untrusted service.

Mitigation: Leave the endpoint unset unless a trusted deployment requires it, and review endpoint configuration before processing real customer or pricing data.

Risk: Generated quotation replies may include business commitments such as pricing, lead time, payment terms, MOQ, or company profile statements.

Mitigation: Have a responsible business user verify costs, exchange rates, capacity, certifications, trade restrictions, and final terms before sending the reply.

Risk: The security summary notes an import-path weakness that merits review before installation.

Mitigation: Install from the trusted release package, review local scripts before execution, and run the skill from a controlled working directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-b2b-assist)
- [Publisher profile](https://clawhub.ai/user/metahuan)
- [Yufluent homepage](https://claw.changzhiai.com)
- [Yufluent OpenClaw documentation](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON response with formatted text for an inquiry reply or quotation summary; the CLI can print the formatted text directly.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY and may use TOKENAPI_BASE_URL to select the Yufluent API endpoint.]

## Skill Version(s):

1.1.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
