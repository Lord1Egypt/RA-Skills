## Description: <br>
Verifica la posicion de una palabra clave para un dominio especifico en Google usando la API de ValueSERP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jorgejaramillo](https://clawhub.ai/user/jorgejaramillo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SEO practitioners, marketers, and agents use this skill to check where a target domain ranks for a keyword in Google results, with optional country, language, and page-depth settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ValueSERP API key and sends searched keywords, domains, country, and language settings to ValueSERP. <br>
Mitigation: Use an approved, scoped API key and confirm users are comfortable sharing those query details with ValueSERP before running checks. <br>
Risk: Broad or accidental searches can consume API quota or create unexpected costs. <br>
Mitigation: Use explicit domain, keyword, country, language, and page-depth settings, and monitor ValueSERP usage. <br>


## Reference(s): <br>
- [ValueSERP Search API documentation](https://www.valueserp.com/docs/search-api/overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code] <br>
**Output Format:** [Markdown response summarizing JSON rank-check results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses VALUESERP_API_KEY and defaults to Google Colombia with Spanish language results unless changed.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
