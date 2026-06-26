## Description: <br>
Export Clawdbot skills as standalone, deployable microservices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MacStenk](https://clawhub.ai/user/MacStenk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to convert trusted Clawdbot skills into standalone FastAPI microservices for Docker, Railway, or Fly.io deployment. It generates service wrappers, deployment configuration, requirements files, environment templates, and optional LLM client code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated services may be deployed before production hardening is complete. <br>
Mitigation: Review the generated output before deployment, add authentication and rate limits, and restrict CORS for the deployed API. <br>
Risk: Copied source skill scripts may carry behavior that is inappropriate for the target service. <br>
Mitigation: Review and scan copied scripts and generated wrappers before publishing or running the service. <br>
Risk: Optional LLM integrations require provider API keys. <br>
Mitigation: Store API keys in deployment secrets and keep local environment files out of source control. <br>
Risk: Generated dependency ranges may not meet production reproducibility requirements. <br>
Mitigation: Pin and review dependencies before production builds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MacStenk/skill-exporter) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Generated project files with console status and next-step shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local skill directory with SKILL.md and scripts/; supports target platform, optional LLM provider, output directory, and API port options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
