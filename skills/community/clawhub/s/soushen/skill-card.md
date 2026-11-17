## Description:

SouShen Hunter is a Playwright-based Bing search and page extraction skill that returns structured search results and page element data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexian2001](https://clawhub.ai/user/hexian2001)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to run Bing searches without a search API and to inspect public web pages for links, forms, buttons, scripts, metadata, and visible content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deep analysis can visit arbitrary URLs from the user's machine and return detailed page data, including cookies and form values.

Mitigation: Use deep analysis only on public, non-sensitive pages unless URL restrictions and output filtering are added.

Risk: The browser launch configuration uses unsafe Chromium flags and anti-detection behavior.

Mitigation: Review and tighten browser flags before deployment, especially in enterprise, authenticated, internal, or sensitive browsing contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexian2001/skills/soushen)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, code, guidance]

**Output Format:** [JSON from the CLI and Python API, with shell command examples in documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search mode returns titles, URLs, snippets, sources, and result types; deep mode returns page text slices plus links, forms, buttons, scripts, metadata, and cookies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
