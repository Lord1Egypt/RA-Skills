## Description:

Save and digest resources from social media posts (X/Twitter, LinkedIn) or any URL. Use when the user shares a tweet URL, a LinkedIn post, or any link they want to keep and understand. Extracts linked resources, fetches their content, and appends a structured entry to the resource log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spideystreet](https://clawhub.ai/user/spideystreet)

### License/Terms of Use:


## Use Case:

Developers and other agent users use this skill to save resources shared through X/Twitter posts, LinkedIn posts, or direct URLs. The skill extracts linked resources, summarizes reachable pages, and appends a structured Markdown entry to a resource log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches arbitrary URLs through shell commands and can encounter unsafe or untrusted links.

Mitigation: Validate URLs before fetching, avoid shell-string interpolation, and restrict access to internal-network addresses.

Risk: The skill persists fetched and summarized link content to a local resource log.

Mitigation: Let the user review entries before writing them and avoid saving sensitive or inaccessible content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spideystreet/skills/sm-saver)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown resource-log entries plus concise confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends saved entries to ~/workspace/resources.md and requires xurl for X/Twitter post extraction.]

## Skill Version(s):

0.0.0-pr-check (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
