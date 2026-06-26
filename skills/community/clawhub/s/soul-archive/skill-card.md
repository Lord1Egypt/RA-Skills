## Description: <br>
Soul Archive is a local-first personality persistence and agentic memory skill that extracts persona data from conversations, stores it as plaintext JSON, and produces prompts, context summaries, recall warnings, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dqsjqian](https://clawhub.ai/user/dqsjqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain a local persona archive, inject concise user context into AI sessions, recall prior work patterns, warn on repeated failure modes, and generate personality reports from saved local data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can build an automatic, long-term plaintext local profile of the user. <br>
Mitigation: Review config.json before use, avoid storing secrets or highly sensitive personal details, and delete or edit local JSON files when data should not persist. <br>
Risk: Auto extraction, context injection, and reflection are enabled by default and may capture or reuse personal details beyond the user's immediate intent. <br>
Mitigation: Disable auto_extract, auto_context_inject, and auto_reflect for manual-only operation, and keep sensitive-topic confirmation enabled. <br>
Risk: Generated prompts, reports, or context summaries may be sent to an external AI provider depending on the host agent or platform. <br>
Mitigation: Treat generated prompts and reports as sensitive data and review the privacy behavior of the agent or platform before sharing them. <br>


## Reference(s): <br>
- [Soul Archive ClawHub Release](https://clawhub.ai/dqsjqian/soul-archive) <br>
- [README](README.md) <br>
- [Privacy](PRIVACY.md) <br>
- [Multi-device Sync](docs/multi-device-sync.md) <br>
- [Extraction Prompts](references/extraction_prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration] <br>
**Output Format:** [Markdown, JSON, plaintext prompts, shell command output, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local persona summaries, role-play prompts, memory recall results, warning text, configuration guidance, and report files.] <br>

## Skill Version(s): <br>
3.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
