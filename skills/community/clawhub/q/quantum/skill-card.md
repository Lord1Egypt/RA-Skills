## Description: <br>
Enables building and deploying quantum computing applications with Quantinuum, Guppy, Selene, and Fly.io for clinical hackathon projects, quantum web apps, cloud-deployed quantum algorithms, and frontend integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and hackathon participants use this skill to scaffold Selene/FastAPI quantum backends, deploy them to Fly.io, and connect React/Lovable frontends for clinical or general quantum-computing applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cloud deployment steps and examples can expose secrets if real API keys are placed in frontend VITE_* variables or uploaded unintentionally. <br>
Mitigation: Inspect .env files before deployment, keep real secrets backend-only, and use --skip-secrets unless you intentionally want to upload secrets to Fly.io. <br>
Risk: Public quantum API services may be overused or accessed unexpectedly without access controls. <br>
Mitigation: Add authentication, restrict CORS, apply rate limits, and review deployment settings before exposing a Selene service publicly. <br>
Risk: Clinical demos can create privacy or compliance risk if real patient data is used. <br>
Mitigation: Use only synthetic or de-identified clinical data unless an appropriate compliance plan is in place. <br>


## Reference(s): <br>
- [Guppy Guide](references/guppy_guide.md) <br>
- [Selene API](references/selene_api.md) <br>
- [Fly.io Configuration](references/flyio_config.md) <br>
- [Lovable Patterns](references/lovable_patterns.md) <br>
- [Clinical Use Cases](references/clinical-use-cases.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/arunnadarasa/quantum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell commands, configuration snippets, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May scaffold FastAPI backend code, React frontend code, Fly.io configuration, environment setup steps, and deployment commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
