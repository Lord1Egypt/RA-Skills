## Description: <br>
Use this skill to find, explore, and install new skills from the Zerone Skill Market. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zerone-Agent](https://clawhub.ai/user/Zerone-Agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to browse the Zerone Skill Market, inspect skill compatibility, fetch installation instructions, and install selected skills after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Zerone's marketplace and may fetch third-party installation instructions that can change over time. <br>
Mitigation: Review fetched installation instructions and target skill contents before approving any install action. <br>
Risk: Installed skills persist under the local skills directory and may alter future agent behavior. <br>
Mitigation: Require explicit user confirmation before installation and restrict privileged filesystem or network actions unless the marketplace maintainer is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zerone-Agent/skill-market) <br>
- [Zerone Skill Market API](https://api.zerone.market/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from the marketplace helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch live marketplace listings, compatibility details, and installation instructions from Zerone before any user-approved install action.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
