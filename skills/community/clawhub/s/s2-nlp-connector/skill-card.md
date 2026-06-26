## Description: <br>
Generates declarative IoT control templates from device API documentation using a local LLM, mapping open devices into S2 spatial primitive elements and blocking unsupported closed protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and IoT integrators use this skill to prototype adapter templates that translate open device APIs into S2 spatial primitive control mappings. It is intended for reviewing and staging generated templates before any real hardware execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated IoT control templates may contain incorrect methods, endpoints, payloads, or target-device mappings. <br>
Mitigation: Manually inspect each generated method, endpoint, payload, and device target before another system uses the template on real hardware. <br>
Risk: API documentation, device details, or proprietary integration notes entered into the skill may be sent to a local model server. <br>
Mitigation: Use only trusted local model servers and avoid entering secrets or proprietary API details unless that server is approved for the data. <br>
Risk: Saved templates can become a path for unintended physical device actions if used without review. <br>
Mitigation: Test generated templates in simulation or a controlled environment before enabling execution against live hardware. <br>


## Reference(s): <br>
- [S2-Spatial-Primitive OS Whitepaper](artifact/S2-Spatial-Primitive-OS-Whitepaper.md) <br>
- [ClawHub release page](https://clawhub.ai/SpaceSQ/s2-nlp-connector) <br>
- [Project homepage](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, configuration, guidance] <br>
**Output Format:** [Interactive console text with generated JSON control templates saved to local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated templates include connection status, device mapping, protocol method, endpoint suffix, and payload schema when adapter generation succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
