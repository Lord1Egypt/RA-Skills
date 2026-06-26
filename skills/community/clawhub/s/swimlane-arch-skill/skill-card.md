## Description: <br>
Swimlane Arch helps agents generate editable Draw.io XML for horizontal or vertical swimlane diagrams and layered system architecture diagrams from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leslietong2046-ship-it](https://clawhub.ai/user/leslietong2046-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, product teams, developers, and workflow owners use this skill to turn process or architecture descriptions into editable diagrams for business flows, government approval processes, cross-team handoffs, and system architecture design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional ProcessOn/PingCode export can send diagram content to a third-party cloud service. <br>
Mitigation: Leave PROCESSON_API_KEY unset for local-only Draw.io output, and only enable cloud export for data approved for that service. <br>
Risk: Generated .drawio files may contain sensitive business process or system architecture details. <br>
Mitigation: Review generated files and storage locations before sharing or uploading diagrams outside the local workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leslietong2046-ship-it/swimlane-arch-skill) <br>
- [Swimlane Horizontal Template](artifact/references/swimlane-template.xml) <br>
- [Swimlane Vertical Template](artifact/references/swimlane-vertical-template.xml) <br>
- [Architecture Template](artifact/references/arch-template.xml) <br>
- [diagrams.net](https://app.diagrams.net) <br>
- [PingCode Graph API](https://open.pingcode.com/v1/graph) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Files, Configuration, Guidance] <br>
**Output Format:** [Draw.io XML in .drawio files, with concise user guidance and an optional ProcessOn/PingCode cloud link when configured.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to local .drawio generation; optional cloud export requires PROCESSON_API_KEY.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release evidence; artifact frontmatter lists 1.1.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
