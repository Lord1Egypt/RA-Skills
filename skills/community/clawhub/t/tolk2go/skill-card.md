## Description: <br>
Helps agents search interpreter availability, price options, and book professional Tolk2Go interpreters for phone, video, or on-site appointments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tolk2go](https://clawhub.ai/user/tolk2go) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find language pairs, interpreter situations, availability, pricing, and booking options through the Tolk2Go public API. <br>

### Deployment Geography for Use: <br>
Netherlands, Belgium, Germany, Luxembourg, and France. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive account, appointment, medical, legal, address, or free-text details to Tolk2Go. <br>
Mitigation: Collect only the minimum details needed for the booking and avoid unnecessary sensitive context in descriptions or free-text fields. <br>
Risk: The skill can create, cancel, or confirm bookings without an explicit user confirmation step. <br>
Mitigation: Show the exact login, registration, booking, cancellation, or confirmation request and require user approval before sending it. <br>


## Reference(s): <br>
- [Tolk2Go OpenAPI specification](https://api.tolk2go.com/api/v1/spec) <br>
- [Tolk2Go website](https://www.tolk2go.com) <br>
- [ClawHub skill page](https://clawhub.ai/tolk2go/tolk2go) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, shell commands] <br>
**Output Format:** [Markdown with endpoint summaries, request steps, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concrete API request payloads for login, registration, availability searches, booking creation, cancellation, and confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
