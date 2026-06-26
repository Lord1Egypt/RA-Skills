## Description: <br>
Enables building and deploying quantum computing applications with Quantinuum, Guppy, Selene, and Fly.io for clinical or healthcare projects, quantum-powered web apps, cloud deployment of quantum algorithms, and user-facing quantum result interfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold, deploy, and connect quantum computing applications that combine Quantinuum or emulator execution, a Selene FastAPI backend, Fly.io hosting, and a Lovable or React frontend. It is especially tailored for clinical and healthcare examples such as drug discovery, treatment optimization, patient stratification, and trial randomization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help deploy healthcare-oriented cloud services that may become public persistent services. <br>
Mitigation: Review the generated service before deployment, add backend authentication and rate limits, restrict CORS, and lock down admin or metrics endpoints. <br>
Risk: Clinical workflows may accidentally use sensitive health data or send it to quantum or cloud backends. <br>
Mitigation: Use only synthetic or de-identified clinical data unless a compliance plan is in place. <br>
Risk: Secrets can be mishandled, especially if exposed through frontend environment variables or deployment configuration. <br>
Mitigation: Inspect environment files before deployment, keep secrets out of VITE_* frontend variables, and prefer skipping secret upload unless it is required. <br>


## Reference(s): <br>
- [Quantinuumclaw Skill Page](https://clawhub.ai/arunnadarasa/quantinuumclaw) <br>
- [Guppy Quantum Programming Guide](references/guppy_guide.md) <br>
- [Selene API Reference](references/selene_api.md) <br>
- [Fly.io Configuration for Quantum Workloads](references/flyio_config.md) <br>
- [Lovable Frontend Patterns for Quantum Apps](references/lovable_patterns.md) <br>
- [Clinical Use Cases for Quantinuum / Guppy / Selene](references/clinical-use-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code and shell command snippets; generated project files when helper scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes backend, deployment, and frontend scaffolding patterns for quantum web applications.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
