## Description: <br>
Fetches live lunch menus from Umeå restaurants via umealunchguide.se. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Simskii](https://clawhub.ai/user/Simskii) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up current lunch menus, prices, dietary tags, and restaurant details for Umeå restaurants. <br>

### Deployment Geography for Use: <br>
Global; content is focused on Umeå, Sweden. <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts umealunchguide.se and displays data from that external site. <br>
Mitigation: Install it only when live Umeå lunch menu lookup is desired, and treat returned restaurant and menu details as third-party public website data. <br>
Risk: External provenance metadata is unavailable for this release. <br>
Mitigation: Review the small included artifact files and the ClawHub security summary before deployment. <br>


## Reference(s): <br>
- [Umeå Lunch Guide](https://umealunchguide.se/) <br>
- [ClawHub skill page](https://clawhub.ai/Simskii/umea-lunch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [JSON from the script, typically summarized as Markdown or plain text by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports date, restaurant-name, and restaurant-list filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
