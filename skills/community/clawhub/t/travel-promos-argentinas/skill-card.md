## Description: <br>
Consulta promociones de viajes desde Argentina mediante Anduin Promos API y ayuda a filtrar vuelos, hoteles, paquetes y otras ofertas por categoria, destino, fecha o score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ferminrp](https://clawhub.ai/user/ferminrp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel-focused agents use this skill to fetch public Argentine travel promotions, summarize availability, and filter or rank offers by category, destination, recency, or score. It is informational only and does not automate bookings or purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts anduin.ferminrp.com and may process returned data with local curl and jq commands. <br>
Mitigation: Review commands before execution and allow outbound access only to the disclosed API host when using the skill. <br>
Risk: Returned promotion links and availability are third-party content that may change or become unavailable. <br>
Mitigation: Verify offer terms, availability, and booking details directly with the provider before acting on any promotion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ferminrp/travel-promos-argentinas) <br>
- [Anduin Promos API OpenAPI](https://anduin.ferminrp.com/docs/openapi.json) <br>
- [Anduin Promos API endpoint](https://anduin.ferminrp.com/api/v1/promos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and tables with optional curl and jq commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public JSON from one disclosed API and formats filtered results locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
