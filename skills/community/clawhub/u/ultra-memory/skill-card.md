## Description: <br>
Ultra Memory gives AI agents local, cross-session memory for logging operations, restoring prior work, and recalling past context by keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanjingya](https://clawhub.ai/user/nanjingya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Ultra Memory to persist local task history, restore previous sessions, search prior work, and maintain project knowledge across long-running workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores substantial local cross-session memory about agent activity. <br>
Mitigation: Install only when persistent memory is desired and protect ~/.ultra-memory with restrictive local permissions. <br>
Risk: Shared environments can expose or mix memory between users or agents. <br>
Mitigation: Use scoped memory spaces for shared machines, multi-user workflows, or multiple agents. <br>
Risk: The REST server can expose memory operations if made reachable without access control. <br>
Mitigation: Configure a bearer token before exposing the REST server beyond local trusted use. <br>
Risk: Automatic hooks or multimodal extraction can persist sensitive content unintentionally. <br>
Mitigation: Enable those features only when the captured tool activity, documents, images, audio, or video are appropriate to retain. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nanjingya/ultra-memory) <br>
- [Advanced Configuration](references/advanced-config.md) <br>
- [REST API Specification](platform/openapi.yaml) <br>
- [npm Package](https://www.npmjs.com/package/ultra-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and local tool or API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and query local memory files under the configured Ultra Memory home directory.] <br>

## Skill Version(s): <br>
4.3.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
