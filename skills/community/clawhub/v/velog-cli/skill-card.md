## Description: <br>
Fetch and display the latest Velog user posts from public RSS feeds in Markdown or JSON without requiring authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve a Velog user's latest public posts for digests, newsletters, or agent context. It is useful when Korean developer community content needs to be pulled quickly without API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review guidance recommends reviewing workflows before use, even though the scan reported no evidence of hidden data theft or destructive behavior. <br>
Mitigation: Review the skill bundle and run it only in environments where its network-fetching behavior is appropriate. <br>
Risk: The skill fetches public RSS content from an external service, so results depend on feed availability and may contain untrusted third-party text. <br>
Mitigation: Validate fetched posts before using them in newsletters, digests, or downstream agent context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chloepark85/velog-cli) <br>
- [Velog](https://velog.io) <br>
- [Velog public RSS endpoint](https://v2.velog.io/rss/<username>) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON post listings, with shell command examples when invoked as a CLI workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public Velog RSS over HTTPS; no API key is required.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, pyproject.toml, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
