## Description: <br>
Operate Reflectt teams via reflectt-node and reflectt-cloud: tasks, inbox, presence, shipping, and operator workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryancampbell](https://clawhub.ai/user/ryancampbell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Reflectt to coordinate team work by pulling tasks, reading inbox and mentions, updating presence, posting chat messages, and publishing shipping updates through a local Reflectt API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends and retrieves team coordination data through a local Reflectt API. <br>
Mitigation: Use it only with a trusted Reflectt local API and confirm the endpoint before running commands. <br>
Risk: Task IDs, inbox content, commit hashes, shipping notes, and chat messages can contain sensitive project information. <br>
Mitigation: Redact or minimize sensitive details before posting updates to shared channels. <br>


## Reference(s): <br>
- [Reflectt documentation](https://reflectt.ai) <br>
- [Reflectt app](https://app.reflectt.ai) <br>
- [ClawHub skill page](https://clawhub.ai/ryancampbell/reflectt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Reflectt API endpoint by default; outputs may include task IDs, inbox content, chat messages, commit hashes, and shipping notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
