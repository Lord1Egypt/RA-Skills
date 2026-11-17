## Description:

Perform web searches using various search engines and APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roryyu](https://clawhub.ai/user/roryyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a documented pattern for reading web page content with Jina Reader and running keyword searches through Exa. The published 0.1.1 artifact is documentation-only, so referenced runtime scripts and package files should be supplied or restored before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs and search queries may be sent to Jina Reader or Exa, which can expose secret tokens in URLs, private internal links, or confidential research terms.

Mitigation: Avoid using secret-bearing URLs, private internal links, or confidential search terms unless sharing those inputs with those services is acceptable.

Risk: The published artifact is documentation-only and may not run as described because referenced scripts and package files are absent.

Mitigation: Verify or restore the runtime scripts, package metadata, and dependencies before deploying or invoking the described Node commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roryyu/skills/websearch-free-skill)
- [Jina Reader API](https://r.jina.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown documentation with JavaScript and bash examples; described runtime outputs are JSON or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Published artifact contains documentation only and requires node and npm if the described scripts are restored.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
