## Description: <br>
Query UK National Rail live departure boards, arrivals, delays, and train services for GB stations via Darwin/Huxley2 APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jabbslad](https://clawhub.ai/user/Jabbslad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer questions about UK train departures, arrivals, delays, platforms, service details, and station codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: National Rail tokens are used in live API requests and could be exposed if shared, logged, or configured in an unsafe environment. <br>
Mitigation: Use a dedicated, revocable token and keep it in private environment or skill configuration storage. <br>
Risk: The shell helper can send the access token to the configured HUXLEY_URL endpoint. <br>
Mitigation: Use the default endpoint or another trusted endpoint only; do not set HUXLEY_URL to an untrusted service. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Jabbslad/uk-trains) <br>
- [National Rail OpenLDBWS registration](https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/) <br>
- [National Rail Darwin OpenLDBWS endpoint](https://lite.realtime.nationalrail.co.uk/OpenLDBWS/ldb12.asmx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a National Rail token for live rail queries; station search can run without the token in the shell helper.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
