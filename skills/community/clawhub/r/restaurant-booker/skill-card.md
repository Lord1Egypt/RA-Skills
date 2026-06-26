## Description: <br>
Book restaurant reservations by phone - just say where, when, and how many; Polly calls the restaurant, handles the conversation, and confirms your table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alionkissadeer](https://clawhub.ai/user/alionkissadeer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register a PollyReach phone agent, book restaurant reservations by outbound call, retrieve call results, and manage incoming call summaries. It can also support broader phone-agent tasks beyond restaurant booking when the user authorizes that behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled for restaurant booking, but evidence.security says it also enables broad phone-agent behavior including inbound call answering, unread-message polling, full transcripts and recordings, and prompt control. <br>
Mitigation: Install only if the broader PollyReach phone-agent behavior is intended, and review activation, inbound answering, polling, and prompt-update settings before using it with personal, customer, or business calls. <br>
Risk: Call summaries, transcripts, recordings, phone numbers, and task details may be exposed through PollyReach responses. <br>
Mitigation: Avoid sensitive calls unless the user has approved that data handling, and present transcript and recording links only to the authorized user. <br>
Risk: Outbound calls can make reservations or other commitments and consume account credits. <br>
Mitigation: Require clear user authorization before calling, check balance when relevant, and report the call result, credits used, and remaining credits after completion. <br>


## Reference(s): <br>
- [Restaurant Booker on ClawHub](https://clawhub.ai/alionkissadeer/restaurant-booker) <br>
- [alionkissadeer ClawHub profile](https://clawhub.ai/user/alionkissadeer) <br>
- [PollyReach](https://pollyreach.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return call transcripts, recording links, detail links, balance information, and inbound prompt-update status from PollyReach.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
