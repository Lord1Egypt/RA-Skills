## Description: <br>
A lightweight web and community data crawling skill for local archiving, full-text search, and freshness checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and small teams use this skill to collect authorized web content or community messages into a local searchable archive and check whether archived data is fresh before relying on it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web and community archiving can collect private, unauthorized, or sensitive data. <br>
Mitigation: Use only data you are authorized to collect, prefer official APIs and public channels, avoid user tokens and private messages, and respect site terms and robots.txt. <br>
Risk: Local archives and exports may retain personal identifiers, credentials, or unnecessary message history. <br>
Mitigation: Set retention limits, exclude credentials and unnecessary user identifiers, keep exports private, and review snapshots before sharing. <br>
Risk: The skill can propose write-capable local storage and shell execution steps. <br>
Mitigation: Review generated commands before running them, keep archive operations in a constrained workspace, and require explicit confirmation for destructive or unsafe database changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-crawler-engine-free) <br>
- [Project homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command, SQL, YAML, and JSON examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local archive schemas, freshness checks, search queries, and manual execution steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
