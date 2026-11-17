## Description:

Performs web research and data extraction through URL fetching, main-text extraction, browser rendering, crawling, and local scripting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrherojack](https://clawhub.ai/user/mrherojack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to research web content in constrained network environments by fetching URLs, extracting readable text, rendering JavaScript-heavy pages, crawling same-site links, and scripting follow-up processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary URL fetching and browser rendering could expose local or internal data.

Mitigation: Restrict URLs to public http/https destinations, block private and local network ranges, and bound downloads and crawl limits.

Risk: Local script execution can increase the impact of unsafe or unreviewed automation.

Mitigation: Run the skill in an isolated environment and require explicit user approval before creating or executing new local programs.

Risk: Headless Chrome rendering without sandbox isolation can expand browser-based attack surface.

Mitigation: Keep browser rendering sandboxed or containerized when processing untrusted pages.

## Reference(s):

- [Super Lobster ClawHub page](https://clawhub.ai/mrherojack/skills/super-lobster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line outputs such as JSON, extracted text, HTML previews, and rendered DOM text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch arbitrary URLs, render pages in headless Chrome, crawl same-site links, and execute local scripts when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
