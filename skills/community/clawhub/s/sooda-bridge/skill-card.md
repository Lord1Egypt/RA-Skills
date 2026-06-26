## Description: <br>
Connects to business AI agents on the Sooda network when a user specifically asks to reach a Sooda agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkim5574](https://clawhub.ai/user/tkim5574) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to send user-chosen messages to named business agents through the Sooda network, including support, travel, dining, procurement, and vendor workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages are sent through Sooda as a third-party relay to business agents. <br>
Mitigation: Use the skill only when the user intends to contact a Sooda agent, and avoid sending sensitive business data unless appropriate for that workflow. <br>
Risk: The SOODA_API_KEY authorizes relay access for the session. <br>
Mitigation: Protect the API key, keep it out of logs and shared output, and use an environment variable or in-memory session value. <br>
Risk: Some target agents can participate in real-world workflows such as bookings, refunds, or purchase orders. <br>
Mitigation: Verify the target agent before each message and require explicit user confirmation before any real-world action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tkim5574/sooda-bridge) <br>
- [Sooda](https://sooda.ai) <br>
- [Sooda signup endpoint](https://sooda.ai/api/v1/signup) <br>
- [Sooda relay endpoint](https://sooda.ai/api/v1/relay/{agent}) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and SOODA_API_KEY; relays user-selected message content to third-party Sooda agents.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
