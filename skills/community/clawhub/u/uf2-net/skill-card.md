## Description: <br>
Create, manage, and track custom short URLs with the uf2.net REST API, including custom slugs, link listing, deletion, click counts, and public stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[setdemos](https://clawhub.ai/user/setdemos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and automation agents use this skill to create and manage uf2.net short links from the command line or REST API, including custom slugs and click-count checks. It is intended for sharing public, non-sensitive URLs because shortened links and metadata are public and non-expiring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated operations require access to the user's uf2.net API key. <br>
Mitigation: Store UF2_API_KEY in a secret store, private environment variable, or OS credential manager, and avoid committing it to shared files. <br>
Risk: Created short links and their metadata are public and do not expire automatically. <br>
Mitigation: Shorten only public, non-sensitive URLs and delete links manually when they should no longer be available. <br>
Risk: The helper script builds JSON request bodies with shell string interpolation. <br>
Mitigation: Use trusted URL, slug, title, and code values unless JSON escaping and input validation are improved. <br>


## Reference(s): <br>
- [uf2.net API Reference](references/api.md) <br>
- [uf2.net Service Homepage](https://uf2.net) <br>
- [uf2.net Swagger API Docs](https://uf2.net/docs) <br>
- [uf2.net ReDoc API Docs](https://uf2.net/redoc) <br>
- [ClawHub Skill Page](https://clawhub.ai/setdemos/uf2-net) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash and curl commands plus JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses UF2_API_KEY for authenticated operations; created links are public and non-expiring.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
