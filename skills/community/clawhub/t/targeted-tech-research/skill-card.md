## Description: <br>
Performs in-depth, vendor-specific technical research on products or solutions, producing structured hardware, software, co-design, and benchmarking analysis with clear fact, derivation, and gap labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[outdog-hwh](https://clawhub.ai/user/outdog-hwh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical analysts use this skill to research a specific vendor, product or solution model, and application scenario, then produce a structured technical breakdown grounded in public sources and marked derivations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs public web research and may trigger dynamic browsing for selected technical or patent sites. <br>
Mitigation: Use it only where public-source research is appropriate, and review gathered sources and generated claims before relying on the report. <br>
Risk: Local evidence, execution metadata, or audit artifacts may retain sensitive information if users provide confidential PDFs, patents, or business documents. <br>
Mitigation: Avoid providing confidential material unless retention is acceptable, and review or delete generated evidence and metadata after use. <br>


## Reference(s): <br>
- [Step Prompts](references/prompts.md) <br>
- [Execution Rules and Checklists](references/rules.md) <br>
- [Dynamic Sites Whitelist](references/dynamic_sites_whitelist.json) <br>
- [Technical Research Report Template](assets/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with source annotations, tables, optional appendices, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs distinguish public facts, derived content, and missing information; optional audit artifacts and execution metadata may be retained locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
