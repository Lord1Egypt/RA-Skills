## Description: <br>
Fetches Alpine Linux latest-stable minirootfs release metadata and aggregates available architectures by version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lentiancn](https://clawhub.ai/user/lentiancn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to retrieve current Alpine Linux minirootfs release URLs and summarize which CPU architectures are available for the latest stable version. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local shell scripts that contact Alpine Linux release servers and parse remote release metadata. <br>
Mitigation: Review or constrain the scripts in locked-down environments and allow network access only to the required Alpine Linux release endpoint. <br>


## Reference(s): <br>
- [Alpine Linux Latest Stable Releases](https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases) <br>
- [ClawHub Skill Page](https://clawhub.ai/lentiancn/skill-alpine) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON] <br>
**Output Format:** [JSON arrays emitted to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local shell execution with curl, jq, and yq to fetch and parse public Alpine Linux release metadata.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
