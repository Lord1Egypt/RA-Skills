## Description: <br>
Analyzes acoustic emotion and semantic intent to prepare a timed Home Assistant smart-home action sequence for context-aware environment control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home integrators use this skill to evaluate voice/acoustic distress cues and prepare a timed Home Assistant response, with dry-run behavior as the default before any local device actuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling real actuation can control local Home Assistant devices and affect the physical environment. <br>
Mitigation: Keep dry-run mode enabled until the hardcoded entity_id and payload are reviewed for the target installation. <br>
Risk: A Home Assistant token or endpoint configured from an untrusted source could expose local devices or direct requests to unintended services. <br>
Mitigation: Protect the Home Assistant token and set HA_BASE_URL to a fixed trusted local Home Assistant endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-voice-multimodal-aligner) <br>
- [Project homepage](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text with configuration values and optional Home Assistant REST calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; real actuation requires non-default Home Assistant credentials and an enabled actuation flag.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
