## Description: <br>
Converts natural-language smart-home intents into predictive 4D timeline tracks with scheduled keyframes for the S2 6-Element Matrix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home automation builders use this skill to turn a resident's routine or scenario description into scheduled device keyframes for simulated or mounted S2 spatial devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LLM-generated smart-home schedules may be saved for later execution without strong validation or confirmation. <br>
Mitigation: Review rendered_tracks.json before any executor acts on it, and require separate confirmation, validation, and rollback before connecting to real devices. <br>
Risk: Routine descriptions and device inventories are sent to a local LLM service. <br>
Mitigation: Install only where local LLM privacy boundaries are acceptable, and avoid entering sensitive routines or device details unless the environment is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-timeline-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/SpaceSQ) <br>
- [Space2 homepage](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration] <br>
**Output Format:** [Console text and JSON timeline records written to rendered_tracks.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates scheduled keyframes from a natural-language routine and active device inventory; review outputs before device execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
