## Description:

Generates a gamified three-node travel itinerary H5 page for a user-provided city using FlyAI travel search results, AI-written narrative copy, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongweisong1999](https://clawhub.ai/user/hongweisong1999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a city name into an interactive travel-game page with three itinerary nodes, narrative story text, FlyAI-sourced product links, and a local preview workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External travel product names, images, and links are inserted into generated HTML and may be untrusted.

Mitigation: Review generated pages before sharing, validate URLs, and ensure text is safely escaped before publishing.

Risk: The workflow depends on an unpinned FlyAI skill and CLI.

Mitigation: Install FlyAI only from a trusted source, review the installed version before use, and avoid automatic runtime installation.

Risk: Private travel plans or preferences could be exposed if a generated page is deployed publicly.

Mitigation: Use local-only preview by default and remove private details before intentionally publishing a page.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongweisong1999/skills/travel-city-game)
- [FlyAI dependency skill](https://clawhub.ai/yealexchen/flyai)
- [FlyAI API key portal](https://flyai.open.fliggy.com/)

## Skill Output:

**Output Type(s):** [Text, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON data structures, and generated HTML file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires preinstalled flyai CLI, python3, node, and a local HTTP preview server for generated HTML.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
