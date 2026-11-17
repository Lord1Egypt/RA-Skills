## Description:

Use this skill to fetch TAAPI.IO indicator data for crypto or stocks, including fast single-indicator requests and bulk/multi-construct queries for agentic trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and trading workflow builders use this skill to retrieve TAAPI.IO technical indicators for crypto, stocks, and ETFs through repeatable CLI commands and JSON payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TAAPI secrets can be exposed through direct request URLs, command arguments, or retained error logs.

Mitigation: Prefer TAAPI_SECRET in a session-scoped environment and use bulk or multi POST flows where practical; rotate revocable secrets if logs may have captured them.

Risk: Unofficial TAAPI base URLs can receive secrets and request payloads.

Mitigation: Use the default https://api.taapi.io endpoint unless a deliberate override is required and acknowledged with TAAPI_ALLOW_UNOFFICIAL_BASE_URL=1 or --allow-unofficial-base-url.

Risk: Live smoke tests send real network requests with TAAPI credentials.

Mitigation: Run live smoke tests only in an isolated session with a revocable TAAPI_SECRET and avoid environments with retained command or output logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oscraters/skills/taapi)
- [TAAPI homepage](https://taapi.io/)
- [TAAPI documentation](https://taapi.io/documentation/)
- [TAAPI direct integration](https://taapi.io/documentation/integration/direct/)
- [TAAPI bulk integration](https://taapi.io/documentation/integration/post-rest-bulk/)
- [TAAPI multiple constructs](https://taapi.io/documentation/multiple-constructs/)
- [TAAPI rate limits](https://taapi.io/documentation/rate-limits/)
- [TAAPI indicators](https://taapi.io/indicators/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with bash commands and JSON payload examples; CLI responses are JSON or raw text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for live requests, TAAPI_SECRET for authenticated calls, and jq for the multi command.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
