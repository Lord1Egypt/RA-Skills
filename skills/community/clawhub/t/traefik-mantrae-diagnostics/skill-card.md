## Description: <br>
Inspect and troubleshoot Traefik reverse proxies via read-only API, dashboard, logs, and config checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naamah75](https://clawhub.ai/user/naamah75) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect Traefik runtime state, Mantrae-managed dynamic configuration, logs, routers, services, middlewares, entrypoints, and TLS hints while diagnosing reverse proxy issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials and broad authenticated access to the Mantrae management API, while the security summary says the advertised read-only boundary is not enforced. <br>
Mitigation: Install only in a trusted operations environment and use a least-privilege read-only Mantrae token instead of administrator credentials. <br>
Risk: Custom RPC paths or custom request messages could be used for write-like operations outside the intended diagnostics workflow. <br>
Mitigation: Use only the documented read-oriented methods unless a change has explicit approval, a fresh backup, and a confirmed operational need. <br>
Risk: Disabling TLS verification with --insecure or curl -k can expose credentials or API data during diagnostics. <br>
Mitigation: Avoid --insecure and curl -k except for an explicitly approved break-glass diagnostic. <br>
Risk: Traefik raw data, support dumps, and access logs may expose routing details, configuration, long OIDC URLs, or state parameters. <br>
Mitigation: Summarize findings and avoid reposting full sensitive dumps or query strings unless explicitly required for the incident. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/naamah75/traefik-mantrae-diagnostics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive operational observations; summaries should avoid exposing credentials, raw support dumps, long OIDC URLs, or full query strings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
