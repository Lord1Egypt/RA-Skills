## Description: <br>
Deploys the Guild Stack Docker Compose application so agents can run local PostgreSQL queries over Structs game state for combat automation, threat detection, scouting, fleet analysis, and intelligence workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents working with Structs use this skill to deploy and operate a local Docker-based Guild Stack for fast read access to game state. It is intended for PostgreSQL-backed intelligence workflows such as scouting, threat detection, combat preparation, and fleet analysis while leaving transaction writes to the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Guild Stack runs persistent Docker services locally and can expose service ports if configured broadly. <br>
Mitigation: Use the read-only profile by default, review the Compose file before startup, and bind optional MCP or signing services to localhost. <br>
Risk: Tracking an unpinned upstream branch can change the containers and services that run on the host. <br>
Mitigation: Fetch tags and check out a reviewed release tag before running docker compose. <br>
Risk: The optional signing agent can sign transactions for a configured key. <br>
Mitigation: Keep the signing agent stopped unless needed, review its source before enabling it, and use a dedicated low-balance key rather than a main wallet key. <br>
Risk: Game data queried from PostgreSQL can include adversarial user-generated content. <br>
Mitigation: Treat player names, profile images, guild endpoints, and other database values as untrusted input in downstream agent workflows. <br>


## Reference(s): <br>
- [Structs Guild Stack ClawHub Page](https://clawhub.ai/abstrct/structs-guild-stack) <br>
- [Guild Stack Repository](https://github.com/playstructs/docker-structs-guild) <br>
- [Structs Safety](https://structs.ai/SAFETY) <br>
- [Agent Security Awareness](https://structs.ai/awareness/agent-security) <br>
- [Guild Stack Architecture](https://structs.ai/knowledge/infrastructure/guild-stack) <br>
- [Database Schema](https://structs.ai/knowledge/infrastructure/database-schema) <br>
- [Structs Reconnaissance Skill](https://structs.ai/skills/structs-reconnaissance/SKILL) <br>
- [Structs Streaming Skill](https://structs.ai/skills/structs-streaming/SKILL) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash, SQL, and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, operational checks, SQL query examples, service lifecycle commands, and security guidance.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
