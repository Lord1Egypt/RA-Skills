## Description: <br>
Ring-a-Ding lets an agent place US and Canada phone calls through the rad CLI for scheduling, reservations, customer-service calls, hands-free sessions, and returns transcripts, summaries, and optional structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlbeta](https://clawhub.ai/user/vlbeta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their users use this skill to delegate phone-based tasks such as appointment scheduling, reservation changes, customer-service follow-up, voicemail, and hands-free working sessions. It is intended for calls to US and Canadian numbers where the user has confirmed the recipient, purpose, and context to share. <br>

### Deployment Geography for Use: <br>
United States and Canada <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real phone calls and share call metadata, transcripts, and provided context with Ring-a-Ding and downstream providers. <br>
Mitigation: Install only when those providers are trusted for the call content; confirm the exact number, recipient, purpose, and details before each call. <br>
Risk: Calls may include sensitive personal, medical, financial, insurance, address, or order details. <br>
Mitigation: Avoid sensitive details unless necessary for the task and explicitly approved by the user. <br>


## Reference(s): <br>
- [Ring-a-Ding documentation](https://ringading.ai/docs) <br>
- [Ring-a-Ding OpenClaw quick start](https://ringading.ai/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples; completed calls return transcript, summary, and optional extracted data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires rad, RAD_API_KEY, and OPENAI_API_KEY; calls are limited to US and Canadian numbers and may require polling or scheduled follow-up.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
