## Description: <br>
Generates Architecture Decision Records from architectural decisions discussed in the current session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill after design discussions to identify decisions worth documenting, confirm which ones should become ADRs, and create draft ADR markdown files for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ADRs may omit context or include draft conclusions that are not yet accepted. <br>
Mitigation: Review each generated ADR before treating it as an accepted architecture record. <br>
Risk: The workflow reads conversation and repository context to extract candidate decisions. <br>
Mitigation: Use it only in workspaces where that context is appropriate for ADR generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/skills/write-adr) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown ADR files and Markdown status summaries with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates user-confirmed ADR files under docs/adrs and reports verification status for each generated record.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
