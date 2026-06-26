## Description: <br>
Saves and digests resources from X/Twitter posts, LinkedIn posts, or direct URLs by extracting linked resources, fetching content, summarizing it, and appending a structured entry to a resource log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spideystreet](https://clawhub.ai/user/spideystreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to save links shared from social posts or direct URLs, summarize the referenced resources, and maintain a local Markdown resource log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches untrusted URLs through local command templates. <br>
Mitigation: Use it only with trusted public URLs and verify local URL-fetching and summarization tools before installation. <br>
Risk: The skill appends summaries and links to a persistent local resource log. <br>
Mitigation: Avoid sensitive, private-network, localhost, or unusually crafted URLs unless URL validation and safer argument handling are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spideystreet/sm-saver) <br>
- [Publisher profile](https://clawhub.ai/user/spideystreet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown resource-log entries and concise confirmation text, with shell command invocations for fetching and summarization] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends saved entries to ~/workspace/resources.md and may mark inaccessible URLs when fetching fails.] <br>

## Skill Version(s): <br>
0.0.0-pr-check (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
