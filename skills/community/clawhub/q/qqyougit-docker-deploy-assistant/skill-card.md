## Description: <br>
Docker部署助手 helps developers create Dockerfiles, docker-compose configurations, deployment scripts, CI/CD snippets, and troubleshooting guidance for containerized application delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to containerize applications, prepare production-oriented Docker and Compose assets, configure supporting services, and diagnose common container build or runtime issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or template deployment commands may affect local Docker resources, especially cleanup examples such as docker system prune -f. <br>
Mitigation: Review commands before running them, remove or gate destructive cleanup steps unless intentional, and test build, push, and restart workflows in staging before production. <br>


## Reference(s): <br>
- [Detailed Docker examples](references/details.md) <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/qqyougit-docker-deploy-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Dockerfile, YAML, shell, and configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to be reviewed and adapted before execution in a target environment.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
