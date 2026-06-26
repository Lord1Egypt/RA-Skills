## Description: <br>
Draft and fill Y Combinator SAFE templates for valuation cap, discount, MFN, and pro rata side letter fundraising documents, producing signable DOCX files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and startup operators use this skill to collect SAFE template inputs, choose an appropriate Y Combinator SAFE variant, and generate a filled DOCX for review before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote fills send financing terms and party information to the hosted Open Agreements service. <br>
Mitigation: Confirm the user is comfortable sharing those values before using Remote MCP, and offer the local CLI path for confidential fundraising terms. <br>
Risk: Generated SAFE documents can affect legal and financing outcomes. <br>
Mitigation: Have the generated document reviewed by qualified counsel before signing. <br>
Risk: The local CLI path uses shell commands and user-provided template values. <br>
Mitigation: Pin the CLI version and enforce the documented filename, field-value, temp-file, and template-name sanitization rules before execution. <br>


## Reference(s): <br>
- [ClawHub Safe Skill Page](https://clawhub.ai/stevenobiajulu/safe) <br>
- [Open Agreements](https://openagreements.org) <br>
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp) <br>
- [open-agreements npm package](https://www.npmjs.com/package/open-agreements) <br>
- [Open Agreements local CLI setup](https://github.com/open-agreements/open-agreements#use-with-claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [DOCX files, Markdown previews, and inline shell commands or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote MCP fills may return a temporary download URL; local CLI fills write a DOCX output file.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
