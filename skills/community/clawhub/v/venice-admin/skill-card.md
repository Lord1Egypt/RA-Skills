## Description:

Venice AI account administration - check balance, view usage history, and manage API keys. Requires an Admin API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabrinaaquino](https://clawhub.ai/user/sabrinaaquino)

### License/Terms of Use:


## Use Case:

Developers and Venice AI account administrators use this skill to inspect account balance, review usage history, and list API-key metadata from Venice Admin API endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill process uses a Venice Admin API key that can access billing information and API-key metadata.

Mitigation: Use a minimally scoped admin key if available, protect VENICE_API_KEY, avoid broad privileged shells, and use inference-only keys for production inference workloads.

Risk: The skill relies on uv to install the httpx dependency declared in inline script metadata.

Mitigation: Pin or preinstall reviewed dependencies before use when dependency supply-chain control is required.

## Reference(s):

- [ClawHub Venice Admin skill page](https://clawhub.ai/sabrinaaquino/skills/venice-admin)
- [Venice AI](https://venice.ai)
- [Venice AI API documentation](https://docs.venice.ai)
- [PEP 723 inline script metadata](https://peps.python.org/pep-0723/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, CSV]

**Output Format:** [Markdown guidance with shell commands; script output is JSON by default, with CSV available for usage history.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and VENICE_API_KEY; usage history supports currency, date range, pagination, sort order, format, and output-file options.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
