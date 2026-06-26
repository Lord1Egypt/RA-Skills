## Description: <br>
urlgo helps agents control a browser through a CLI for opening pages, capturing screenshots, reading page content, clicking, typing, and running JavaScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use urlgo to operate a local browser through CDP when they need to inspect web pages, capture screenshots, extract page content, or perform supervised browser interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables powerful browser-control actions including click, type, and JavaScript evaluation. <br>
Mitigation: Supervise browser actions and review intended targets before execution. <br>
Risk: The skill depends on an external urlgo executable. <br>
Mitigation: Verify where the executable comes from before installing or running the skill. <br>
Risk: Browser automation can act on sensitive authenticated pages. <br>
Mitigation: Avoid using the skill on sensitive authenticated pages unless that access is intended, and close the background browser when finished. <br>


## Reference(s): <br>
- [ClawHub skill page: urlgo](https://clawhub.ai/fslong520/urlgo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Code] <br>
**Output Format:** [Markdown with inline shell commands, file paths, and browser action results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce page snapshots, screenshot files, and JavaScript evaluation results through the urlgo CLI.] <br>

## Skill Version(s): <br>
6.5.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
