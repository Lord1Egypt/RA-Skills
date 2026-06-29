## Description: <br>
TCM dietary therapy and syndrome differentiation API client for pattern diagnosis, ingredient properties, food therapy plans, and tea recipe lookup through the remote api.tcmplate.com service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanqubing](https://clawhub.ai/user/fanqubing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call a remote TCM dietary API for informational syndrome differentiation, ingredient lookup, food therapy suggestions, and tea recipe recommendations. It is a reference tool and does not provide medical diagnosis, prescription, or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries send symptom descriptions, constitution types, disease terms, and ingredient searches to api.tcmplate.com. <br>
Mitigation: Use only when comfortable sending that data to the remote service, and do not include names, addresses, phone numbers, ID numbers, or highly sensitive medical details in query text. <br>
Risk: The skill can return health-related dietary guidance that users may mistake for medical advice. <br>
Mitigation: Treat outputs as informational reference material and consult a licensed medical practitioner for health concerns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanqubing/skills/tcm-dietary-api) <br>
- [TCMPlate API documentation](https://tcmplate.com/docs) <br>
- [TCMPlate privacy policy](https://tcmplate.com/privacy) <br>
- [TCMPlate support](https://tcmplate.com/support) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; API calls return JSON dictionaries or lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote HTTPS API client; free tier allows 10 calls per day per IP, with optional paid API key configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
