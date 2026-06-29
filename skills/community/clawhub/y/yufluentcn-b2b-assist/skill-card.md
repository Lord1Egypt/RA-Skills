## Description: <br>
Assists B2B import-export teams with inquiry replies and RFQ quotations for FOB/CIF pricing, MOQ negotiation, lead times, and company profiles through the Yufluent cloud harness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, sales teams, and export operators use this skill to turn buyer inquiries into structured B2B reply drafts and RFQ quotation content. The skill is intended to collect quotation inputs, call the Yufluent service, and return text that a business user reviews before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends buyer inquiries, pricing, MOQ, lead-time, payment terms, and company profile text to the configured Yufluent/OpenClaw service. <br>
Mitigation: Use the skill only with an approved service endpoint and avoid submitting information that should not leave the user's environment. <br>
Risk: The skill requires TOKENAPI_KEY and can use TOKENAPI_BASE_URL, so leaked credentials or an untrusted endpoint could expose requests. <br>
Mitigation: Keep TOKENAPI_KEY out of source control and logs, rotate it if exposed, and set TOKENAPI_BASE_URL only to a trusted host. <br>
Risk: Generated quotation or reply text could contain incorrect pricing, lead-time, certification, or trade-compliance statements. <br>
Mitigation: Have a business user verify costs, exchange rates, capacity, company claims, import/export restrictions, and sanctions considerations before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-b2b-assist) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw setup](https://claw.changzhiai.com/app/openclaw) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text with optional JSON-backed skill output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include email body text, quotation summary content, run metadata, and optional file output from the CLI.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
