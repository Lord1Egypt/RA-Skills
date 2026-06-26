## Description: <br>
Use this skill when a user wants a trust decision before installing from a skill URL, marketplace, or GitHub repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likw99](https://clawhub.ai/user/likw99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use TrustSkills to make a quick source-provenance decision before installing a skill from a URL, marketplace, or GitHub repository. It helps distinguish trusted distribution roots from unsupported or unverified third-party sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Trusted result could be mistaken for a full safety review of the specific skill artifact. <br>
Mitigation: Treat the result as a first-pass source check only, then review the artifact, permissions, maintainer account, and update path before installing. <br>


## Reference(s): <br>
- [ClawHub TrustSkills release page](https://clawhub.ai/likw99/trustskills) <br>
- [TrustSkills hosted SKILL.md](https://trustskills.app/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown decision summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a source trust verdict, supporting root, safest known install path, and remaining risk.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
