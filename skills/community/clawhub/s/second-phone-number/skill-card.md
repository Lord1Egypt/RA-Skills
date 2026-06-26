## Description: <br>
Get a dedicated second phone number instantly. Keep your personal number private, separate work from life, and let AI handle the calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsz](https://clawhub.ai/user/mrsz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to obtain and manage a dedicated PollyReach phone number for outbound calls, incoming call answering, voicemail transcription, spam filtering, and call summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill handles sensitive phone numbers, call instructions, inbound messages, call summaries, transcripts, recordings, and custom answering prompts through PollyReach. <br>
Mitigation: Use it only when comfortable with PollyReach processing that data, avoid one-time codes or highly sensitive calls, and review returned transcripts and summaries before relying on them. <br>
Risk: The PollyReach token grants access to the phone-number integration and related call operations. <br>
Mitigation: Keep the PollyReach token file private and rotate or remove it if the local environment is shared or compromised. <br>
Risk: Periodic inbound-call polling can create ongoing checks for new calls. <br>
Mitigation: Enable scheduled polling only when explicitly desired and choose an interval appropriate for the user's privacy and notification expectations. <br>


## Reference(s): <br>
- [PollyReach](https://pollyreach.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/mrsz/second-phone-number) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PollyReach API calls and a local token file to activate a number, send call tasks, poll results, check balance, retrieve inbound call summaries, and update answering prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
