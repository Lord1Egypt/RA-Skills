## Description: <br>
Use a self-hosted SearXNG search engine to run searches, retrieve results, and manage a local SearXNG service from CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeshunee](https://clawhub.ai/user/leeshunee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need self-hosted web search through SearXNG, including first-time setup, service control, and query execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install dependencies, clone and run SearXNG, manage a local service, and enable autostart. <br>
Mitigation: Install only when local SearXNG deployment is intended, review any sudo or service-management prompt, and enable autostart only when persistent operation is desired. <br>
Risk: Search traffic and configuration values may be exposed if the service is bound to an untrusted host, port, or endpoint. <br>
Mitigation: Keep the default local binding unless a wider network exposure is required, avoid untrusted SEARXNG_HOST, SEARXNG_PORT, and SEARXNG_SECRET values, and do not route sensitive searches through endpoints you do not control. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/leeshunee/searxng-search-cli) <br>
- [SearXNG official documentation](https://docs.searxng.org) <br>
- [SearXNG source repository](https://github.com/searxng/searxng) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI output and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include titles, URLs, and short snippets; setup guidance may include service and environment configuration.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
