## Description: <br>
Access TDNET timely disclosures from Tokyo Stock Exchange and JPX-listed companies, including earnings, dividends, buybacks, forecast revisions, and governance changes, with search by company, stock code, date, or keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajtgjmdjp](https://clawhub.ai/user/ajtgjmdjp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and market-monitoring agents use this skill to look up public Japanese market disclosures, browse recent TDNET announcements, and retrieve company- or date-specific disclosure results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and invokes an external Python CLI package. <br>
Mitigation: Verify the tdnet-disclosure-mcp package provenance before use in sensitive environments. <br>
Risk: Disclosure search terms may be sent to the external public disclosure API used by the CLI. <br>
Mitigation: Use the skill only with public or non-sensitive search terms. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ajtgjmdjp/tdnet-disclosure-mcp) <br>
- [Publisher Profile](https://clawhub.ai/user/ajtgjmdjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed CLI can return human-readable text or JSON for disclosure queries.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
