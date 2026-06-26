## Description: <br>
Videoinu platform skill - manage projects via Graphs, upload and download files, chat with AI Agents, and run Workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[everfirdev](https://clawhub.ai/user/everfirdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Videoinu projects from an agent, including graph management, file transfer, agent sessions, and workflow execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Videoinu access token and project data. <br>
Mitigation: Install only when the publisher and integration are trusted, avoid hardcoding access keys, and upload only files intended for Videoinu. <br>
Risk: Direct downloads can send the access token when fetching file URLs. <br>
Mitigation: Avoid direct downloads from untrusted URLs and prefer downloads from known graph assets. <br>
Risk: The agent chat script can auto-approve tool actions. <br>
Mitigation: Avoid --auto-approve unless the graph and requested agent actions are low-risk. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/everfirdev/videoinu) <br>
- [Videoinu Platform](https://videoinu.com) <br>
- [Videoinu Login](https://videoinu.com/login) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Videoinu access key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
