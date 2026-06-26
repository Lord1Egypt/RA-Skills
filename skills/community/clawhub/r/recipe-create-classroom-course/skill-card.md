## Description: <br>
Create a Google Classroom course and invite students. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, school administrators, and Google Workspace operators use this recipe to create a Google Classroom course, invite a student, and verify enrollment through the gws command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the recipe can create a real Google Classroom course and send a real student invitation. <br>
Mitigation: Confirm the active Google Workspace account, course details, and student email before executing the gws commands. <br>
Risk: The workflow depends on the external gws tool and gws-classroom dependency. <br>
Mitigation: Install only trusted versions of the tool and dependency and use approved Google Workspace credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-create-classroom-course) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-classroom skill dependency.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata); artifact metadata version 0.22.5 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
