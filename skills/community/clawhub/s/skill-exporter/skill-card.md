## Description:

Skill Exporter exports Clawdbot skills as standalone deployable microservices, generating FastAPI wrappers, Docker and deployment configuration, requirements files, environment examples, and optional LLM client integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macstenk](https://clawhub.ai/user/macstenk)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to package existing Clawdbot skills as FastAPI microservices for Docker, Railway, or Fly.io deployment. It is intended for creating an independent API service with generated project files and optional OpenAI or Anthropic client scaffolding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated service can be compromised by malicious source-skill metadata.

Mitigation: Use the exporter only with trusted source skills and inspect generated api.py before running or deploying the service.

Risk: Source scripts can be deleted if the output path overlaps the source skill directory.

Mitigation: Choose an output directory outside the source skill directory and verify source and output paths before export.

Risk: Production secrets or API keys may be exposed or misused if added before generated code is reviewed.

Mitigation: Keep production API keys out of the generated service until the generated files have been reviewed.

Risk: Generated dependency ranges may be unsuitable for production builds.

Mitigation: Pin dependencies and review the generated requirements before production deployment.

## Reference(s):

- [Skill Exporter on ClawHub](https://clawhub.ai/macstenk/skills/skill-exporter)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated service files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates Dockerfile, docker-compose.yml, api.py, requirements.txt, .env.example, copied skill scripts, optional llm_client.py, and optional Railway or Fly.io deployment configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
