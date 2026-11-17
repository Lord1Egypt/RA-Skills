## Description:

Search Google via SerpAPI across Google Search, Google News, and Google Local for web, news, and local-business lookups with country and language targeting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericsantos](https://clawhub.ai/user/ericsantos)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Google web, news, and local-business searches through SerpAPI with country, language, location, and result-count controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and location strings are sent to SerpAPI.

Mitigation: Avoid submitting confidential or regulated search terms and use only approved SerpAPI accounts for sensitive work.

Risk: API-key handling needs review before installation.

Mitigation: Prefer SERPAPI_API_KEY over the --api-key flag, keep stored keys permission-restricted, and rotate keys according to local policy.

Risk: Shell-script hardening concerns were flagged by the security evidence.

Mitigation: Run the skill without privileged wrappers, avoid untrusted environment variables, and review temporary-path handling before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericsantos/skills/serpapi-search)
- [SerpAPI Search API endpoint](https://serpapi.com/search.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text search results or raw JSON, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, python3, and a SERPAPI_API_KEY credential.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
