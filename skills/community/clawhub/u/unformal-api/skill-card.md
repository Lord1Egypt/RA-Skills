## Description: <br>
Create conversational Pulses that replace static forms, surveys, intake emails, feedback requests, interviews, lead qualification, onboarding questionnaires, and customer research with AI-led conversations that return structured data, transcripts, and aggregate insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonasboury](https://clawhub.ai/user/jonasboury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and customer-facing teams use this skill to create and manage Unformal Pulses for surveys, research interviews, lead qualification, intake, onboarding, feedback, and respondent analytics through the Unformal API or CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Unformal API key and may handle sensitive respondent, applicant, employee, customer, transcript, quote, or research data. <br>
Mitigation: Use a dedicated, revocable API key, keep it out of prompts and shared logs, collect data only with appropriate consent, and limit exports or forwarding to trusted destinations. <br>
Risk: The skill instructs agents to install or update global tooling and refresh the skill from a remote URL. <br>
Mitigation: Manually approve npm installs and curl-based updates, review downloaded content before use, and avoid automatic self-updates in managed environments. <br>
Risk: The skill can create, publish, update, delete, export, and webhook Unformal Pulse data. <br>
Mitigation: Require explicit approval for POST, PATCH, DELETE, export, and webhook actions, and verify Pulse recipients, webhook URLs, and exported files before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jonasboury/unformal-api) <br>
- [Publisher profile](https://clawhub.ai/user/jonasboury) <br>
- [Unformal website](https://unformal.ai) <br>
- [Unformal API Reference](https://unformal.ai/docs/api) <br>
- [Unformal Integration Guide](https://unformal.ai/integrate) <br>
- [Unformal llms.txt](https://unformal.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, curl examples, JSON request and response examples, and configuration instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Unformal share links, API payloads, CLI commands, exports, transcripts, structured respondent data, aggregate insights, analytics summaries, and webhook configuration guidance.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
