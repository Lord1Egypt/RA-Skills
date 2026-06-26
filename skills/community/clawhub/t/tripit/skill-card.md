## Description: <br>
Create and update TripIt travel plans by sending structured confirmation emails to plans@tripit.com for flights, hotels, activities, car rentals, rail, and cruises. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamwestland](https://clawhub.ai/user/adamwestland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to turn user-provided itinerary details into TripIt-approved email bodies and sending guidance so TripIt can create or update travel plan entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle personal travel details while generating and sending TripIt confirmation emails. <br>
Mitigation: Review the generated email before sending and use it only when the user is comfortable sending those details to TripIt through the available email tool. <br>
Risk: A private TripIt iCal feed URL can continue exposing travel details if stored or shared insecurely. <br>
Mitigation: Do not store the feed URL unless the user explicitly approves secure storage, retention, and deletion rules; regenerate the feed URL if it is exposed. <br>
Risk: TripIt may ignore or misparse emails if the sender address is not linked, the message is not plain text, or required fields are missing. <br>
Mitigation: Confirm the sender email is connected to the TripIt account, send plain text, and validate required fields before sending. <br>


## Reference(s): <br>
- [TripIt Email Template Format Reference](references/template-format.md) <br>
- [TripIt ClawHub release page](https://clawhub.ai/adamwestland/tripit) <br>
- [Publisher profile: adamwestland](https://clawhub.ai/user/adamwestland) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text email bodies with optional subject lines, plus Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an external email-sending capability and user-provided travel details; can optionally use a private TripIt iCal feed URL for verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
