## Description:

Smart web search with auto region detection and dual-tier content fetching. Works in both China and international networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agents use this skill to search the web and fetch result-page content across China and international network environments. It is suited for finding current information, tutorials, and source pages when a single known URL is not available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic searches, IP-region probes, and fetched pages may disclose queries, network location, and requested URLs to external services.

Mitigation: Use only with queries and URLs appropriate for external services, and disable automatic content fetching with --fetch=0 or --no-fetch for sensitive searches.

Risk: Unrestricted page fetching can reach private or internal network resources when run on a host with broad network access.

Mitigation: Run the skill in a sandboxed environment or restrict URL fetching and outbound network access on hosts that can reach sensitive internal services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ucsdzehualiu/skills/smart-web-search)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Node.js](https://nodejs.org)
- [Playwright Mirror](https://npmmirror.com/mirrors/playwright)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON arrays or objects containing search results, URLs, snippets, fetched page content, status, and errors; setup and verification guidance is provided as shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output is bounded by --max, --fetch, and --max-len options; default search fetches content from the top 3 results.]

## Skill Version(s):

3.2.2 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
