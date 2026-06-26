## Description: <br>
Persistent memory for repeated browser work that loads relevant notes before an agent revisits sites or flows, then saves durable site knowledge after the task finishes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[littleyier](https://clawhub.ai/user/littleyier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to recall reusable site notes before repeated browser automation tasks and write back durable lessons afterward. It is most useful when the same websites, selectors, routes, or interaction patterns are revisited across tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses shared browser memory across projects, which can expose durable notes from one task to another. <br>
Mitigation: Use separate SITE_MEMORY_HOME paths for sensitive projects and review stored notes regularly. <br>
Risk: The bundled browser automation can control logged-in Chrome tabs through live debugging access. <br>
Mitigation: Use a separate low-privilege browser profile for automation and avoid sensitive tabs and accounts. <br>
Risk: An untrusted SITE_MEMORY_CDP_SCRIPT value could redirect browser control through unexpected code. <br>
Mitigation: Do not set SITE_MEMORY_CDP_SCRIPT to an untrusted file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/littleyier/site-memory) <br>
- [site-memory skill instructions](artifact/SKILL.md) <br>
- [Bundled chrome-cdp README](artifact/vendor/chrome-cdp-skill/README.md) <br>
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON prompt payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reads markdown memory files under the configured site-memory runtime root.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
