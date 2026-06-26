## Description: <br>
Generate images and videos using yino.ai for Seedream image generation, Veo video generation, and related media generation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HackerQED](https://clawhub.ai/user/HackerQED) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agents through yino.ai media generation workflows, including capability discovery, authenticated API calls, project organization, polling, and preview updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation includes a preflight command that can print the YINO_API_KEY. <br>
Mitigation: Use a non-revealing presence check for the environment variable and never display API key values in logs or chat. <br>
Risk: Prompts, uploaded media, generated outputs, and API usage may be sent to yino.ai. <br>
Mitigation: Confirm that the user trusts yino.ai and the publisher before sending prompts or files, especially for private or sensitive media. <br>
Risk: Broad activation rules may invoke the skill for general media generation requests. <br>
Mitigation: Confirm the intended yino.ai workflow before making authenticated API calls or uploading files. <br>


## Reference(s): <br>
- [Yino.ai ClawHub release](https://clawhub.ai/HackerQED/yino-ai) <br>
- [Yino.ai API key settings](https://yino.ai/settings) <br>
- [Project & Preview Knowledge](references/project-preview.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a YINO_API_KEY and may produce links to generated media, project previews, and status responses.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
