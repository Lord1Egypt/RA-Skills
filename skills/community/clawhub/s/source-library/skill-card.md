## Description: <br>
Source Library helps an OpenClaw agent capture shared URLs into a persistent local research library with structured summaries, claims, quotes, tags, cross-references, freshness tracking, and search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Don-GBot](https://clawhub.ai/user/Don-GBot) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users and developers use this skill to maintain a local, searchable source library from links they share with an agent. It is useful for personal research workflows that need saved summaries, claims, quotes, tags, connection mapping, conflict checks, and a reading queue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically retain shared URLs, summaries, claims, quotes, tags, analysis, and context in a long-lived local library. <br>
Mitigation: Avoid sharing confidential or private URLs unless they should be archived, and review or remove files under life/source when retained data is no longer appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Don-GBot/source-library) <br>
- [Publisher profile](https://clawhub.ai/user/Don-GBot) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text output, including saved local Markdown source summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent local files under life/source and data/source-queue.json in the user's workspace.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
