## Description:

Work with the WordPress REST API for route discovery, authentication, reads and writes, core endpoint selection, and custom namespace inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:


## Use Case:

Developers and site maintainers use this skill to inspect live WordPress REST routes, choose authentication models, select core endpoints, and design or review custom REST endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Application passwords can be exposed if credentials are pasted directly into shell commands or retained in shell history.

Mitigation: Use test or narrowly scoped WordPress application passwords, avoid placing real credentials directly in shell history, and rotate any credential that may have been exposed.

Risk: Authenticated calls to non-HTTPS targets can expose credentials or API data in transit.

Mitigation: Prefer HTTPS-only WordPress targets for authenticated REST API inspection and writes.

Risk: Authenticated calls with absolute route URLs may target a different origin than the site argument.

Mitigation: Use site-relative routes for authenticated calls unless same-origin HTTPS behavior is enforced before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matthewxmurphy/skills/wordpress-rest-api)
- [Auth And Discovery](references/auth-and-discovery.md)
- [Core Endpoints](references/core-endpoints.md)
- [Custom Route Rules](references/custom-route-rules.md)
- [WordPress REST API reference](https://developer.wordpress.org/rest-api/reference/)
- [WordPress REST API authentication overview](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/)
- [Application Passwords integration guide](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/#basic-authentication-with-application-passwords)
- [Routes and endpoints handbook](https://developer.wordpress.org/rest-api/extending-the-rest-api/routes-and-endpoints/)
- [Adding custom endpoints](https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-custom-endpoints/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, REST route examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST route URLs, curl commands, JSON response summaries, authentication guidance, and implementation review notes.]

## Skill Version(s):

0.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
