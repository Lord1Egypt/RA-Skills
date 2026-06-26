## Description: <br>
Toggl-Optimized-V2 helps agents use Toggl Track more efficiently with direct API reporting guidance and a shell script for JSON or PDF summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex1389](https://clawhub.ai/user/alex1389) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to configure Toggl Track API access and request compact time-reporting summaries without loading unnecessary context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Toggl API token, which is sensitive credential material. <br>
Mitigation: Set TOGGL_API_TOKEN only in trusted shells, avoid committing or logging it, and rotate the token if it is exposed. <br>
Risk: The bundled report script is incomplete and may not produce a usable Toggl report without further review. <br>
Mitigation: Review and complete the client lookup and reporting logic before relying on generated summaries. <br>


## Reference(s): <br>
- [Toggl Profile Settings](https://track.toggl.com/profile) <br>
- [ClawHub skill page](https://clawhub.ai/alex1389/toggl-optimized-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and script usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON or PDF Toggl report requests through the bundled shell script.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
