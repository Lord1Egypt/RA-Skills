## Description: <br>
Create scheduled research-paper alerts using OpenAlex and OpenClaw cron. Use to subscribe to journals, conferences, or research topics; list/update/cancel subscriptions; test real OpenAlex queries; and push concise daily Chinese summaries of newly matched papers. Designed for topic monitoring such as AD/MCI, dynamic functional connectivity, rs-fMRI, graph neural networks, and medical imaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjuncher](https://clawhub.ai/user/zjuncher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and research teams use this skill to maintain scheduled alerts for new papers by topic, journal, or conference, then receive concise Chinese summaries of matching OpenAlex results. It is suited for recurring topic monitoring rather than one-off literature reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local subscription state and create or remove OpenClaw cron jobs. <br>
Mitigation: Ask for confirmation before creating or deleting scheduled jobs, verify timezone and recipient details, and review generated commands before execution. <br>
Risk: Recipient identifiers are local user data and generated subscription files may contain sensitive routing details. <br>
Mitigation: Keep generated data/*.json files out of published artifacts and avoid storing API keys, tokens, cookies, or private channel credentials in the skill folder. <br>
Risk: Full-access autoreview modes or trusted-maintainer workflows can change code, services, GitHub state, or ClawHub moderation state. <br>
Mitigation: Install only in a trusted development or maintainer environment and consider disabling full-access autoreview mode with --no-yolo or AUTOREVIEW_YOLO=0 for untrusted repositories. <br>


## Reference(s): <br>
- [Research Paper Push on ClawHub](https://clawhub.ai/zjuncher/research-paper-push) <br>
- [OpenAlex API](https://api.openalex.org) <br>
- [OpenAlex Works endpoint](https://api.openalex.org/works) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and concise Chinese paper-summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local subscription JSON state and register or remove OpenClaw cron jobs when the user asks for scheduling changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
