## Description:

Unload your cognitive baggage. Drop ideas anywhere, find the signal later.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to turn a local second-brain markdown ledger into parsed atoms, intent-based clusters, tensions, emerging signals, and a visual graph for exploring recurring ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private notes and may send the atom corpus to the configured LLM gateway.

Mitigation: Use only notes appropriate for persistent local storage and LLM processing, and keep the gateway host set to 127.0.0.1 or localhost unless a remote endpoint is intentionally approved.

Risk: Gateway and optional messaging credentials are stored locally and could expose private capture channels if mishandled.

Mitigation: Protect local credential files, rotate gateway and messaging tokens, and use dedicated private Slack or Telegram channels with clear retention rules.

Risk: Automated ingestion can capture more personal or third-party content than intended.

Mitigation: Limit ingestion to dedicated channels or labels, review channel membership and retention settings, and avoid connecting broad inboxes or shared spaces without consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highnoonoffice/skills/second-brain-visualizer)
- [Project homepage](https://github.com/highnoonoffice/hno-skills)
- [Setup Guide](references/setup.md)
- [Install Guide](references/install.md)
- [Ingestion Guide](references/ingestion.md)
- [Parser](references/parser.js)
- [Clustering Engine](references/cluster.js)
- [Visualizer Component](references/component.tsx)
- [Sample Atom Ledger](references/sample-ledger.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with JavaScript, TypeScript, shell commands, and JSON schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local atom JSON, cluster JSON, and a React/D3 visualizer component when the supplied scripts and component are installed by the user.]

## Skill Version(s):

1.6.3 (source: server release evidence; artifact frontmatter lists 1.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
