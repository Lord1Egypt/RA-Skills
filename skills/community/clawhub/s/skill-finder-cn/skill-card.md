## Description: <br>
Helps agents search ClawHub for relevant skills, inspect results, recommend options, and provide installation and verification commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to discover ClawHub skills that match a task, compare basic result metadata, and get commands to inspect, install, and verify selected skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing a recommended skill changes the user's OpenClaw environment and makes that skill available after the current task. <br>
Mitigation: Inspect each recommended skill before installation and only approve clawhub install for a specific skill the user trusts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/skill-finder-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and ranked skill recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawhub CLI; outputs may include search, inspect, install, list, and filesystem verification commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
