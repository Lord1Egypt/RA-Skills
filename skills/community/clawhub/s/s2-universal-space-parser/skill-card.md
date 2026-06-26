## Description: <br>
S2 Official Smart Space Engine parses 62 spatial types into a six-element hardware matrix and includes a local MCP server plus S2-SWM causality data harvester. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and smart-space designers use this skill to turn a room or facility type into a brand-agnostic six-element smart-hardware blueprint, scenario recommendations, and MCP-accessible parser output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP physical-action flow is not production-safe physical-control software. <br>
Mitigation: Use it only for controlled local experimentation unless explicit authorization, human confirmation, truthful execution status, and safety checks are added before connecting real smart-home or facility actuators. <br>
Risk: The Chronos harvester writes action parameters and environmental state transitions to a local plaintext JSONL file. <br>
Mitigation: Review or disable JSONL logging where the data could reveal private behavior, and add access control plus retention limits before deployment. <br>
Risk: The manual includes a shell execution bridge example for a web API. <br>
Mitigation: Replace that example with a hardened integration before exposing any web API. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spacesq/s2-universal-space-parser) <br>
- [Space2.world](https://space2.world) <br>
- [S2-UHSP Whitepaper V1.0](artifact/S2-UHSP-Whitepaper-V1.0.md) <br>
- [S2 Space Architect Manual](artifact/S2_SPACE_ARCHITECT_MANUAL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON parser results, Markdown guidance, shell command examples, and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Parser output includes a six-element hardware matrix, scenario recommendations, and local JSONL causality logging when physical-action logging is invoked.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
