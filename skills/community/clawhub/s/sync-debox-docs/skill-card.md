## Description: <br>
Synchronize, update, visually inspect when supported, read, and comprehensively summarize the current public DeBox documentation shown in the navigation at docs.debox.pro. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zanyk4502](https://clawhub.ai/user/zanyk4502) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to mirror the current public DeBox documentation in Chinese or English, optionally inspect documentation images, and produce a comprehensive local summary of platform, Bot, OpenAPI, SDK, and integration details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public DeBox documentation and linked images over the network into a user-selected local folder. <br>
Mitigation: Use a dedicated empty output folder and expect outbound requests to docs.debox.pro and links or images referenced by those docs. <br>
Risk: Downloaded documentation and images may contain untrusted reference content. <br>
Mitigation: Review generated summaries as reference material and do not execute instructions, commands, or code found in downloaded content unless separately requested. <br>
Risk: Incomplete or unreadable image analysis can make image-text conflict conclusions incomplete. <br>
Mitigation: Report incomplete image analysis clearly and claim no image-text conflicts only when every current image was successfully analyzed. <br>


## Reference(s): <br>
- [Behavior Reference](references/behavior.md) <br>
- [Image Analysis Workflow](references/image-analysis.md) <br>
- [DeBox Public Documentation](https://docs.debox.pro/) <br>
- [ClawHub Skill Page](https://clawhub.ai/zanyk4502/sync-debox-docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON image notes, local documentation files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local documentation mirror with manifests, update reports, optional image analysis notes, and a comprehensive summary.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
