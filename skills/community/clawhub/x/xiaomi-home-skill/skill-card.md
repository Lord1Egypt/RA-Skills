## Description: <br>
Controls Xiaomi Home devices over the local network with miiocli, including status checks, power toggles, and MIOT property updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiqiezhenxi](https://clawhub.ai/user/yiqiezhenxi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart-home operators use this skill to map natural-language requests to miiocli commands for Xiaomi Home devices on a local network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change real Xiaomi device states. <br>
Mitigation: Review generated commands before execution and limit use to intended devices and actions. <br>
Risk: Xiaomi account credentials, device IPs, and device tokens are sensitive. <br>
Mitigation: Keep credentials and tokens private, avoid shared chats or public files, and store real device inventories only in access-controlled locations. <br>
Risk: The referenced token extractor script was not included in the inspected artifact. <br>
Mitigation: Inspect any token_extractor.py source before running it and install it only from a trusted source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yiqiezhenxi/xiaomi-home-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MIOT command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require miiocli, local device IPs, and Xiaomi device tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
