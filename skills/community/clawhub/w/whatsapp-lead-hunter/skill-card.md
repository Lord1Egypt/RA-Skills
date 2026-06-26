## Description: <br>
WhatsApp Lead Hunter guides agents through scraping Google Maps business leads, drafting personalized outreach, and sending WhatsApp messages through WAHA with rate limits and ignore lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[izletenadam-creator](https://clawhub.ai/user/izletenadam-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, marketing, and operations teams use this skill to build local-business lead lists, personalize WhatsApp outreach, and run small, permission-based WAHA sending batches with suppression and ignore lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live WhatsApp outreach can create spam, consent, and account-enforcement risk. <br>
Mitigation: Use only lawful, permission-based outreach; run dry-runs first; manually approve every recipient list and message; and enforce small batch limits with delays. <br>
Risk: Lead files and phone-number logs can contain compliance-sensitive contact data. <br>
Mitigation: Set retention and deletion rules for lead files and phone logs, and limit access to the stored data. <br>
Risk: A leaked WAHA API key or exposed WAHA endpoint could allow unauthorized message sending. <br>
Mitigation: Protect the WAHA key and keep WAHA bound to localhost or a trusted network. <br>
Risk: Automated bot replies can interact with outreach recipients unexpectedly. <br>
Mitigation: Maintain suppression and opt-out lists, and add outreach numbers to bot ignore lists before sending. <br>


## Reference(s): <br>
- [Pitch Templates by Sector](references/pitch-templates.md) <br>
- [WhatsApp Lead Hunter on ClawHub](https://clawhub.ai/izletenadam-creator/whatsapp-lead-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and WAHA API snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce lead JSON structures, outreach copy, ignore-list guidance, dry-run commands, and batch-send commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
