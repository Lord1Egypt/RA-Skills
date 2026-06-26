## Description: <br>
S2 宠物守护者智能体。集成 SUNS 与 22 位 S2-DID 身份确权，提供情绪翻译与零信任硬件调控。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
S2-CLA <br>


## Use Case: <br>
Pet-care developers and evaluators can use this local agent demo to generate S2-DID pet identities, translate simulated pet and environment signals into alerts or feeding proposals, and persist local companion records. It is intended for review in a sandbox before any connection to real feeders, locks, thermostats, payment flows, or other physical systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Demo-grade physical-control proposals could be mistaken for production-ready automation. <br>
Mitigation: Keep execution sandboxed and do not connect the agent to real feeders, locks, thermostats, payment flows, or other physical systems without independent review and replacement of the demo signing flow. <br>
Risk: Local execution writes pet records and may create a simulated public key file under s2_bas_governance. <br>
Mitigation: Review file permissions and run only in a workspace where local record creation is expected. <br>
Risk: Security claims in the artifact are stronger than the implementation evidenced by the scan summary. <br>
Mitigation: Treat the skill as a local pet-monitoring demo and validate any zero-trust or hardware-control behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/spacesq/s2-pet-guardian-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Text and JSON-like proposals with local Markdown records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write pet records and simulated public key files under s2_bas_governance during local execution.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter, package.json, _meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
