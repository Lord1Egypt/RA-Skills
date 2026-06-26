## Description: <br>
Creates and manages AI-generated YouTube scripts, metadata, thumbnails, and publishing schedules through the Teleskopiq GraphQL API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nethunter](https://clawhub.ai/user/nethunter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, content teams, and developer agents use this skill to draft YouTube scripts with production tags, generate metadata and thumbnail ideas, and schedule videos in a connected Teleskopiq account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send API credentials and script content to any endpoint configured through TELESKOPIQ_ENDPOINT. <br>
Mitigation: Leave TELESKOPIQ_ENDPOINT unset for the default hosted service, or set it only to a trusted HTTPS endpoint; use limited or revocable API keys where possible. <br>
Risk: Full-flow, schedule, and urgent scheduling commands can change publishing schedules in the connected Teleskopiq account. <br>
Mitigation: Review the target script, date, time, and urgent flag before running scheduling commands, especially on shared or production channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nethunter/teleskopiq) <br>
- [Teleskopiq homepage](https://teleskopiq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Teleskopiq content outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TELESKOPIQ_API_KEY; can create or update scripts, metadata, thumbnails, and schedules in the connected account.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
