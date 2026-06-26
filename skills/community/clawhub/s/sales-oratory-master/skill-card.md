## Description: <br>
Handles B2B presales and renewal negotiations with value-shift tactics and compliance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ken0122](https://clawhub.ai/user/ken0122) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales and customer-facing teams use this skill to draft Chinese-language B2B software presales, renewal, upsell, and objection-handling responses for price, budget, competitor, and value concerns. It asks for deal stage and customer persona so the generated guidance can be tailored before review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated sales language may be inaccurate, overpromising, noncompliant, or poorly matched to the customer context. <br>
Mitigation: Review generated messaging before sending it to customers, especially for legal, commercial, technical, security, and negotiation claims. <br>
Risk: Customer quotes, deal stage, and persona details may contain sensitive customer or deal information. <br>
Mitigation: Avoid pasting sensitive customer data unless that context is approved for processing by the configured LLM runtime. <br>
Risk: Prompt-injection or adversarial customer text could try to override the sales and compliance instructions. <br>
Mitigation: Treat customer-provided text as input data, preserve the compliance guardrails, and verify the final response against the documented redlines. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ken0122/sales-oratory-master) <br>
- [PROMISE_GUARD.md](artifact/PROMISE_GUARD.md) <br>
- [prompt_template.md](artifact/prompt_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown sections containing sales analysis, suggested response copy, rationale, and compliance risk notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated through the configured LLM client after loading the prompt template and compliance guard text.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
