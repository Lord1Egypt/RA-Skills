## Description: <br>
Conducts deep research on a user-provided topic with YouMind, producing a comprehensive cited report, key findings, and actionable insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DophinL](https://clawhub.ai/user/DophinL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to run YouMind deep research from an agent session. The skill returns a concise summary and a link to the full cited report saved in the user's YouMind board. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and generated reports are sent to and saved in the user's YouMind account. <br>
Mitigation: Install only if YouMind is trusted for the intended research content, and avoid submitting sensitive topics that should not leave the local environment. <br>
Risk: The skill requires a YOUMIND_API_KEY and access to the YouMind CLI. <br>
Mitigation: Configure the API key through environment or OpenClaw configuration and never paste it into chat; verify the CLI is installed before use. <br>
Risk: Broad trigger phrases such as "investigate" may invoke the skill when the user intended a local analysis. <br>
Mitigation: Confirm the research topic and intent before starting the YouMind workflow when the request is ambiguous. <br>
Risk: Deep research can run for several minutes and depends on remote service completion. <br>
Mitigation: Warn users about the expected 1-5 minute wait, use background polling when supported, and stop polling after the documented timeout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DophinL/youmind-deep-research) <br>
- [YouMind CLI package](https://www.npmjs.com/package/@youmind-ai/cli) <br>
- [YouMind Skills gallery](https://youmind.com/skills?utm_source=youmind-deep-research) <br>
- [Setup](references/setup.md) <br>
- [Long-running tasks](references/long-running-tasks.md) <br>
- [Error handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, status updates, links, and concise key findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the YouMind CLI, YOUMIND_API_KEY, network access to YouMind, and polling for long-running research tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
