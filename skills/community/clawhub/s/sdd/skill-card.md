## Description: <br>
Scenario-Driven Detection helps agents inspect web apps, source projects, and APIs for scenario-level logic defects, verify expected behavior, and propose or apply fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kimky1122](https://clawhub.ai/user/kimky1122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to crawl or inspect applications, infer expected user-flow behavior, detect logic defects that do not necessarily crash, and produce a Markdown report with findings and fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can crawl authenticated applications and may handle session credentials or cookies. <br>
Mitigation: Use staging environments and least-privilege test accounts, avoid production credentials, and confirm the exact target before running. <br>
Risk: The skill may perform state-changing browser actions, write reports, edit code, or create commits while verifying and fixing logic defects. <br>
Mitigation: Require manual approval before state-changing clicks, file writes, code edits, or commits, and review all generated reports and changes before sharing or merging. <br>
Risk: Inferred expectations can misclassify intended product behavior as a defect. <br>
Mitigation: Treat uncertain findings and proposed fixes as review items, validate behavior with product owners, and run the existing test suite before relying on changes. <br>


## Reference(s): <br>
- [Inference Rules](references/inference-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kimky1122/sdd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with scenario findings, verification results, fix proposals, and optional code edits or commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a report file and apply fixes when source code is available; URL-only mode produces fix guidance instead of direct code changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
