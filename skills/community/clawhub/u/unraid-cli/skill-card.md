## Description: <br>
TypeScript CLI for Unraid Server GraphQL API. 12 command groups for system, arrays, disks, containers, VMs, shares, logs, and diagnostics. Built for humans and AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ingodibella](https://clawhub.ai/user/ingodibella) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and AI agents use this skill to inspect and manage Unraid servers through the ucli command-line interface. It supports health checks, resource summaries, array and disk inspection, container and VM operations, shares, logs, services, network status, and diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses UNRAID_API_KEY to access an Unraid server. <br>
Mitigation: Treat the API key as a secret, avoid exposing diagnostics output unless secrets are redacted, and prefer isolated profiles or explicit host and API-key settings for automation. <br>
Risk: The CLI can perform lifecycle or destructive server actions. <br>
Mitigation: Run read-only inspection commands first, require explicit identifiers for mutations, use --yes only in deliberate automation paths, and re-fetch state after changes. <br>
Risk: The skill depends on the external npm package unraid-cli. <br>
Mitigation: Install only when the npm package and repository are trusted for the target environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ingodibella/unraid-cli) <br>
- [Artifact-declared project homepage](https://github.com/Ingodibella/unraid-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers ucli JSON output with --quiet, --fields, --filter, and --sort for agent-readable results.] <br>

## Skill Version(s): <br>
0.4.0 (source: server-resolved release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
