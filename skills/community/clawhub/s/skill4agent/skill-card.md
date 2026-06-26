## Description: <br>
Use this skill to search, read, and install skills from the skill4agent online skill library with Chinese, English, and mixed-language keyword support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[osulivan](https://clawhub.ai/user/osulivan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover relevant skills, inspect skill details, and install selected skills through either npx-based CLI commands or direct HTTPS API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installed skills may include scripts or sensitive code that can affect local files, private information, or system configuration. <br>
Mitigation: Check the returned script metadata before installation, obtain user consent for skills marked as needing attention, and recheck noted code locations after installation. <br>
Risk: Security evidence reports a suspicious review helper pattern involving nested review with sandbox bypass and broad filesystem authority. <br>
Mitigation: Review the bundle before use in privileged workspaces and keep nested review sandboxing enabled unless the user intentionally authorizes bypass behavior. <br>
Risk: CLI usage depends on Node.js, npm, npx, and the external skill4agent npm package. <br>
Mitigation: Use the direct HTTPS API option when Node.js tooling is unavailable or when avoiding npm package execution is preferred. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/osulivan/skill4agent) <br>
- [Publisher profile](https://clawhub.ai/user/osulivan) <br>
- [skill4agent source site](https://www.skill4agent.com) <br>
- [skill4agent npm package](https://www.npmjs.com/package/skill4agent) <br>
- [skill4agent API](https://skill4agent.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, HTTPS API endpoints, and JSON-oriented response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install skill files into a local .agents/skills directory when the install workflow is used.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
