## Description: <br>
Provides a local Python console for initializing SUNS/S2-DID identity data, recording interaction text, updating a five-dimensional personality matrix, generating profile reports, and exporting a persistent Sour.md prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators can use this skill to run a local personality and memory experiment for OpenClaw-style agents, including identity setup, interaction logging, personality-matrix updates, and prompt export. It is best treated as a local behavior-shaping tool rather than a security sandbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw interaction text and profile data are stored on disk. <br>
Mitigation: Avoid entering secrets or sensitive personal information, and review or delete ./s2_consciousness_data when the memory experiment is no longer needed. <br>
Risk: Interaction text may be sent to a localhost OpenAI-compatible LLM service during analysis. <br>
Mitigation: Use only a trusted local endpoint and confirm its model, logging, and retention behavior before processing sensitive text. <br>
Risk: The generated Sour.md file is intended to persistently alter future agent behavior. <br>
Mitigation: Review Sour.md before loading it into OpenClaw and remove or edit instructions that are unsuitable for the deployment. <br>
Risk: The skill presents physical isolation and safety concepts that are not a real sandbox or enforcement boundary. <br>
Mitigation: Do not grant physical actuator or privileged system access based on this skill's claims; use independent access controls and runtime isolation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-silicon-soul-os) <br>
- [Publisher profile](https://clawhub.ai/user/spacesq) <br>
- [Project homepage](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration] <br>
**Output Format:** [Terminal text, local JSON data files, and generated Markdown prompt file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores profile and interaction data under ./s2_consciousness_data and may call a localhost OpenAI-compatible LLM endpoint for analysis.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
