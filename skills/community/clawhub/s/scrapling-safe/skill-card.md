## Description:

Scrapling Safe helps agents scrape and extract publicly accessible web content using HTTP requests, browser-backed fetching, and selector-based extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linshuikeji](https://clawhub.ai/user/linshuikeji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to collect data from public web pages, extract content with CSS or XPath selectors, and export results for downstream review or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact any URL the agent is given.

Mitigation: Use it in an isolated environment and avoid private, internal, or sensitive URLs.

Risk: The skill can write scrape results under the user's home directory.

Mitigation: Choose a dedicated output folder and review generated files before reuse.

Risk: The security scan found that the safety claims are not enforced strongly enough for the network and file-writing authority used by the skill.

Mitigation: Review the skill before deployment and prefer pinned dependencies or a reviewed lockfile.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linshuikeji/skills/scrapling-safe)
- [ClawHub Publisher Profile](https://clawhub.ai/user/linshuikeji)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI examples and optional JSON, TXT, or Markdown scrape outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be written under the user's home directory when an output path is supplied.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
