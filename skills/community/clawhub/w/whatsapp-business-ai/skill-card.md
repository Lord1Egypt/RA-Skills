## Description: <br>
Automates WhatsApp conversations for local businesses, including replies, bookings, lead capture, and follow-ups for gyms, restaurants, salons, clinics, and service businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcvanstad](https://clawhub.ai/user/marcvanstad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business operators and developers use this skill to configure a WhatsApp Business assistant that classifies incoming messages, sends replies, captures leads, books appointments, schedules follow-ups, and escalates selected conversations to humans. <br>

### Deployment Geography for Use: <br>
South Africa <br>

## Known Risks and Mitigations: <br>
Risk: Customer chats and leads may be stored or shared with connected services without clear retention and disclosure controls. <br>
Mitigation: Define retention periods, disclose storage and third-party sharing to customers, and use least-privilege test credentials before production deployment. <br>
Risk: Automated follow-ups and broadcast messages may contact customers without sufficient consent. <br>
Mitigation: Require explicit opt-in for marketing and recurring follow-ups, honor opt-out requests, and keep human approval on broadcast workflows. <br>
Risk: Clinic, prescription, complaint, refund, and booking workflows can require human judgment or regulated handling. <br>
Mitigation: Route these workflows through human approval or escalation before sending commitments, advice, refunds, or final booking decisions. <br>
Risk: Plaintext environment files and development ngrok tunnels can expose credentials or webhook traffic if used carelessly. <br>
Mitigation: Secure or replace plaintext .env storage and use a hardened production webhook endpoint instead of an unhardened ngrok tunnel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcvanstad/whatsapp-business-ai) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Business configuration template](artifact/reference/config/business.yaml) <br>
- [Prompt configuration template](artifact/reference/config/prompts.yaml) <br>
- [Booking workflow template](artifact/reference/workflows/booking.yaml) <br>
- [Webhook startup script](artifact/reference/scripts/start-webhook.sh) <br>
- [Meta WhatsApp subscription endpoint](https://graph.facebook.com/v18.0/$WHATSAPP_PHONE_NUMBER_ID/subscriptions) <br>
- [Google Calendar OAuth scope](https://www.googleapis.com/auth/calendar) <br>
- [ngrok download](https://ngrok.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WhatsApp reply templates, intent labels, booking workflows, lead handling, follow-up behavior, and operator commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
