## Description:

Access TDNET timely disclosures from Tokyo Stock Exchange listed companies, including earnings, dividends, buybacks, forecast revisions, and governance changes, without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajtgjmdjp](https://clawhub.ai/user/ajtgjmdjp)

### License/Terms of Use:


## Use Case:

External users, developers, and financial analysts use this skill to retrieve and search Japan stock market corporate disclosure announcements by company, stock code, keyword, or date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external Python package is installed by package name and is not pinned to a reviewed version.

Mitigation: Use a reviewed pinned version or hash-locked install in a sandboxed environment.

Risk: Financial disclosure results may be incomplete, stale, or unsuitable as the only basis for decisions.

Mitigation: Verify important disclosures against official TDNET or exchange sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajtgjmdjp/skills/tdnet-disclosure-mcp)
- [Publisher profile](https://clawhub.ai/user/ajtgjmdjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying command-line tool can return JSON when invoked with its JSON output option.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
