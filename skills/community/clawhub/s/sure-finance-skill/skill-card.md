## Description: <br>
Sure Finance API skill. Use when the user wants personal finance insights, account and transaction operations, tags/categories management, imports, or chat workflows in Sure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[secondport](https://clawhub.ai/user/secondport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and finance operators use this skill to query and manage Sure Finance accounts, transactions, categories, tags, imports, and chat workflows through the Sure API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify sensitive Sure Finance records through authenticated API calls. <br>
Mitigation: Use a scoped API key stored in environment variables, verify SURE_BASE_URL before requests, and review create, update, delete, and import operations before sending them. <br>
Risk: Optional self-hosting workflows download compose and environment files before running Docker services. <br>
Mitigation: Inspect downloaded compose and environment files before use, and run self-hosting steps only when explicitly requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/secondport/sure-finance-skill) <br>
- [Publisher profile](https://clawhub.ai/user/secondport) <br>
- [OpenClaw Compatibility Guide](docs/openclaw-compatibility.md) <br>
- [Sure API Playbooks](docs/api-playbooks.md) <br>
- [Self-Hosting Quickstart](docs/self-hosting-quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise API workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl requests, JSON payload examples, financial summaries, and redacted operational guidance.] <br>

## Skill Version(s): <br>
0.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
