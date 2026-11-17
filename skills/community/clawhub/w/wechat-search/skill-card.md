## Description:

Search WeChat Official Account articles using OpenClaw's web search, Tavily API, and web fetch capabilities with compliance-focused design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixsonwang](https://clawhub.ai/user/jixsonwang)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to search public WeChat Official Account articles and return recent article metadata through OpenClaw web search, Tavily, or direct web fetch fallbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and fetched content may be exposed to third-party search or fetch providers.

Mitigation: Run the skill only where sharing those queries with Brave, Tavily, OpenClaw web tools, and fetched sites is acceptable.

Risk: The skill invokes unbundled external helper code with a broad process environment.

Mitigation: Install only after review, restrict child-process environment variables, and avoid running with unrelated cloud tokens or sensitive credentials available.

Risk: The documentation claims compliance controls that the security evidence says may be overstated.

Mitigation: Validate URL hostname handling, robots and rate-limit behavior, and provider-specific terms before production use.

Risk: Runtime dependencies are not pinned to exact versions.

Mitigation: Pin and review dependencies before deploying the skill in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jixsonwang/skills/wechat-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Text, JSON, or Markdown search results with article titles, URLs, snippets, and account metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to five results, supports a maximum-results option, brief output, configuration file path, date filters in the documented interface, and search strategy selection in the documented interface.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
