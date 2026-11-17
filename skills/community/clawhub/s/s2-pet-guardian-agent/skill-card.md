## Description:

S2 宠物守护者智能体。集成 SUNS 与 22 位 S2-DID 身份确权，提供情绪翻译与零信任硬件调控。

This skill is for research and development only.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

S2-CLA

## Use Case:

External developers and pet-care experimenters use this skill to generate local pet identity records, translate simulated pet state into human-readable status, and create signed-authorization proposals before any physical feeding action. It should be treated as a local research or development aid until the authorization and privacy controls identified by security review are fixed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardware authorization claims may overstate the current trust boundary because the code path can create signing keys, overwrite the public-key trust file, and verify only part of a proposed action.

Mitigation: Keep the skill in local research or development use, do not connect it to real feeders or other hardware gateways, protect the public-key trust file from writes, sign every security-relevant proposal field, and add token expiry and replay protection.

Risk: Local pet records may contain sensitive household or animal-care data without clear retention controls.

Mitigation: Define local retention, deletion, and access-control policies before using generated pet logs outside a private test environment.

Risk: Health-related status text could be mistaken for veterinary diagnosis.

Mitigation: Use the skill only for observation and alerting, and require qualified veterinary review for medical decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-pet-guardian-agent)
- [README.md](README.md)
- [LICENSE.md](LICENSE.md)
- [pet_chronos_dashboard.json](visualizations/pet_chronos_dashboard.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON-like proposals, Python code paths, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local pet companion records under s2_bas_governance/pets and expects public-key material under s2_bas_governance/keys for authorization checks.]

## Skill Version(s):

1.2.1 (source: SKILL.md frontmatter, package.json, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
